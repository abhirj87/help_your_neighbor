import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from_email = 'help.your.neighbor.covid.crisis@gmail.com'


def send_email(to_emails, subject, html_content):
    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=html_content)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
        print(e.message)
