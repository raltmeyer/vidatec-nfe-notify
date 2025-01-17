#################################
# Vida Tecnologia Ambiental
# Rogerio Altmeyer - 2025
#################################

import os
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class SendGridEmail:
    def __init__(self):
        self.from_email = os.getenv('SENDGRID_FROM_EMAIL')
        self.api_key = os.getenv('SENDGRID_API_KEY')

    def send_email(self, to_email, subject, content):
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject=subject,
            html_content=content
        )
        try:
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            logging.info(f"Email sent to {to_email} with status code {response.status_code}")
        except Exception as e:
            logging.error(f"Error sending email: {e}")