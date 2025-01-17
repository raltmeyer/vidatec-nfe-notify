#################################
# Vida Tecnologia Ambiental
# Rogerio Altmeyer - 2025
#################################

import os
import logging
from classSendGridEmail import SendGridEmail
from classLoggerConfig import LoggerConfig

LoggerConfig.configure_logging()

to_email = "rogerio@altmeyer.com.br"  
subject = "vidatec-nfe-notify: Test Email via SendGrid"
content = "<strong>This is a vidatec-nfe-notify test email sent using SendGrid.</strong>"
email_sender = SendGridEmail()
email_sender.send_email("rogerio@altmeyer.com.br", subject, content)
