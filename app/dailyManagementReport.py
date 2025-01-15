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
unpaid_boletos_count = db.count_unpaid_boletos_this_month()
logging.info(f"Unpaid Boletos This Month: {unpaid_boletos_count}")

paid_boletos_count = db.count_paid_boletos_this_month()
logging.info(f"Paid Boletos This Month: {paid_boletos_count}")

# email details
to_email = "rogerio@altmeyer.com.br"  # Replace with the recipient's email address
subject = "vidatec-nfe-notifica: Relatório Diário de Gerenciamento"
html_report = f"""
<html>
<head>
    <title>Daily Management Report</title>
</head>
<body>
    <h1>Daily Management Report</h1>
    <p><strong>Boletos não pagos esse mês:</strong> {unpaid_boletos_count}</p>
    <p><strong>Boletos já pagos esse mês:</strong> {paid_boletos_count}</p>
</body>
</html>
"""

logging.info("Sending email report...")
send_email(to_email, subject, html_report)

logging.info("Daily Management Report has finished.")
db.disconnect()