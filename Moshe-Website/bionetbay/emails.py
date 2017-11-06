from flask_mail import Message
from bionetbay import mail, app
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, html_body):#, html_body):
    msg = Message(subject, sender='support@bionetbay.com', recipients=recipients)
    # msg.body = body
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
