import os
import smtplib

from email.mime.text import MIMEText


def send_email(text: str):
    msg = MIMEText('')
    email_account = os.getenv('GMAIL_ACCOUNT')
    me = email_account
    you = email_account
    msg['Subject'] = text
    msg['From'] = me
    msg['To'] = you

    smtp = smtplib.SMTP('smtp.gmail.com', port=587)
    smtp.starttls()
    smtp.login(email_account, os.getenv('GMAIL_PASSWORD'))
    smtp.sendmail(me, [you], msg.as_string())
    smtp.quit()
