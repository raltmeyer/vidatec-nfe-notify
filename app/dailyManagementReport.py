import os
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from classDatabaseQueries import DatabaseQueries
import mysql.connector
from mysql.connector import errorcode

host = os.getenv('MYSQL_HOST')
database = os.getenv('MYSQL_DB')
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASS')


def send_email(to_email, subject, content):
    message = Mail(
        from_email=os.getenv('SENDGRID_FROM_EMAIL'),
        to_emails=to_email,
        subject=subject,
        html_content=content
    )
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(f"Email sent to {to_email} with status code {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")


######
# Main

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Daily Management Report has started.")


db = DatabaseQueries(host=host, database=database, user=user, password=password)
db.connect()

# get info

total_nfe_count = db.count_total_nfes_this_month()
logging.info(f"Total NFe This Month: {total_nfe_count}")

cancelled_nfe_count = db.count_canceled_nfes_this_month()
logging.info(f"Total NFe This Month: {cancelled_nfe_count}")

unpaid_nfe_count = db.count_unpaid_nfes_this_month()
logging.info(f"Unpaid NFe This Month: {unpaid_nfe_count}")

paid_nfe_count = db.count_paid_nfes_this_month()
logging.info(f"Paid NFe This Month: {paid_nfe_count}")

# email details
to_email = "rogerio@altmeyer.com.br; joaomartins@vidatecambiental.com.br; faturamento@vidatecambiental.com.br; financeiro@vidatecambiental"  # Replace with the recipient's email address
subject = "vidatec-nfe-notifica: Relatório Diário de Gerenciamento"
html_report = f"""
<html>
<head>
    <title>Relatório Gerencial Diário</title>
</head>
<body>
    <h1>Relatório Gerencial Diário</h1>
    <hr>
    <p><h2>Totais de cobranças geradas no mês corrente:</H2></p>
    <p><strong>+ NFe geradas com cobrança:</strong> {total_nfe_count}</p>
    <br><strong>- NFe canceladas:</strong> {cancelled_nfe_count}</br>
    <br><strong>- Total NFe ativas:</strong> {total_nfe_count - cancelled_nfe_count}</br>

    <hr>
    <p><strong>NFe não pagos esse mês:</strong> {unpaid_nfe_count}</p>
    <br><strong>NFe já pagos esse mês:</strong> {paid_nfe_count}</br>
    <hr>
</body>
</html>
"""

logging.info("Sending email report...")
#logging.info(html_report)
send_email(to_email, subject, html_report)

logging.info("Daily Management Report has finished.")
db.disconnect()