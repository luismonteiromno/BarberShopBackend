from datetime import datetime, timedelta

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


def get_available_times_for_day(day, date):
    working_start = datetime.combine(date, day.start)
    working_end = datetime.combine(date, day.end_time)
    pause_start = datetime.combine(date, day.pause_time) if day.pause_time else None
    pause_end = datetime.combine(date, day.end_pause_time) if day.end_pause_time else None

    available_times_list = []

    current_time = working_start
    time_interval = timedelta(hours=1)

    while current_time.time() < working_end.time():
        is_within_pause = (
                pause_start and pause_end and
                pause_start.time() <= current_time.time() < pause_end.time()
        )

        if not is_within_pause:
            available_times_list.append(current_time.strftime('%H:%M'))

        current_time += time_interval

    return available_times_list
