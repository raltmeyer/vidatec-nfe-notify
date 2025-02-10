#################################
# Vida Tecnologia Ambiental
# Rogerio Altmeyer - 2025
#################################

import os
import logging
from classDatabaseQueries import DatabaseQueries
from classSendGridEmail import SendGridEmail
from classLoggerConfig import LoggerConfig
from classBoletosTable import BoletosTable

######
# Main

LoggerConfig.configure_logging()

db = DatabaseQueries()
db.connect()
boletosTable = BoletosTable()


# get info
total_nfe_count = db.count_total_nfes_this_month()
cancelled_nfe_count = db.count_canceled_nfes_this_month()
unpaid_nfe_count = db.count_unpaid_nfes_this_month()
paid_nfe_count = db.count_paid_nfes_this_month()
boletos_due_in_3_days = db.count_boletos_by_date(-3)
boletos_due_today = db.count_boletos_by_date(0)
boletos_due_5_days_ago = db.count_boletos_by_date(-5)


logging.info(f"Total NFe This Month: {total_nfe_count}")
logging.info(f"Total NFe This Month: {cancelled_nfe_count}")
logging.info(f"Unpaid NFe This Month: {unpaid_nfe_count}")
logging.info(f"Paid NFe This Month: {paid_nfe_count}")
logging.info(f"Email com vencimentos em 3 dias: {boletos_due_in_3_days}")
logging.info(f"Email com vencimento hoje: {boletos_due_today}")
logging.info(f"Email ja vencidos a 5 dias: {boletos_due_5_days_ago}")

# email details
subject = "vidatec-nfe-notifica: Relatório Gerencial Diário"
html_report = f"""
<html>
<head>
    <title>Relatório Gerencial Diário</title>
</head>
<body>
    <h1>Relatório Gerencial Diário</h1>
    <hr>
    <p><h2>Totais de cobranças (boletos/carteira) geradas no mês corrente:</H2></p>
    <br><strong>NFe geradas com cobrança:</strong> {total_nfe_count}</br>
    <br><strong>NFe canceladas:</strong> {cancelled_nfe_count}</br>
    <br><strong>Total NFe ativas:</strong> {total_nfe_count - cancelled_nfe_count}</br>

    <hr>
    <p><h2>Status de pagamentos:</H2></p>
    <br><strong>NFe não pagas:</strong> {unpaid_nfe_count}</br>
    <br><strong>NFe já pagas:</strong> {paid_nfe_count}</br>
    <hr>

    <hr>
    <br><strong>Total de email com vencimentos em 3 dias:</strong> {boletos_due_in_3_days}</br>
    <br><strong>Total de email com vencimento hoje:</strong> {boletos_due_today}</br>
    <br><strong>Total de email vencidos a 5 dias:</strong> {boletos_due_5_days_ago}</br>
    <hr>

    <hr>
    <p><h2>Boletos vencendo em 3 dias:</H2></p>
    {boletosTable.clientesVencimentoByAddDate(-5)}

</body>
</html>
"""
logging.info(html_report)

logging.info("Sending email report...")
#email_sender = SendGridEmail()
#email_sender.send_email("rogerio@altmeyer.com.br", subject, html_report)
#email_sender.send_email("joaomartins@vidatecambiental.com.br", subject, html_report)
#email_sender.send_email("faturamento@vidatecambiental.com.br", subject, html_report)

logging.info("Daily Management Report has finished.")
db.disconnect()
