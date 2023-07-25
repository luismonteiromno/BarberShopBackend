from barbershop import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import sentry_sdk
import smtplib


def send_email(email, subject, body):
    try:
        # create message object instance
        msg = MIMEMultipart()

        message = body

        msg['From'] = settings.EMAIL_FROM
        msg['To'] = email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'html'))

        # create server
        server = smtplib.SMTP(settings.EMAIL_HOST + ": " + settings.EMAIL_PORT.__str__())

        server.starttls()

        # Login Credentials for sending the mail
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string ())

        server.quit()

        return 200

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return 500
