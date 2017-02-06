import logging

import boto3
from flask import render_template

from config import ADMINS
from .decorators import async


logger = logging.getLogger(__name__)

ses = boto3.client('ses')

@async
def send_async_mail(sender, recipients, subject, body_text, body_html):
    response = ses.send_email(
        Source=sender,
        Destination={'ToAddresses': recipients},
        Message={
            'Subject': {'Data': subject},
            'Body': {
                'Text': {'Data': body_text},
                'Html': {'Data': body_html}
            }
        }
    )
    print(response)


def follower_notification(followed, follower):
    send_async_mail(sender=ADMINS[0],
              #recipients=[followed.email],
              recipients=[ADMINS[0]],
              subject="[microblog] %s is now following your!" % follower.nickname,
              body_text=render_template("follower_email.txt",
                                        user=followed, follower=follower),
              body_html=render_template("follower_email.html",
                                        user=followed, follower=follower))
