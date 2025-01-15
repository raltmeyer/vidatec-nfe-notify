import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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

if __name__ == "__main__":
    to_email = "rogerio@altmeyer.com.br"  # Replace with the recipient's email address
    subject = "vidatec-nfe-notify: Test Email via SendGrid"
    content = "<strong>This is a vidatec-nfe-notify test email sent using SendGrid.</strong>"
    send_email(to_email, subject, content)