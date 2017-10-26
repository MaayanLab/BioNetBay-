from flask_mail import Message
from bionetbay import mail

def send_email(subject, recipients, html_body):#, html_body):
    msg = Message(subject, sender='support@bionetbay.com', recipients=recipients)
    # msg.body = body
    msg.html = html_body
    mail.send(msg)
