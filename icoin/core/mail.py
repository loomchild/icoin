from flask import render_template
from flask.ext.mail import Mail, Message
from icoin import app
from icoin.core.queue import task


mail = Mail()

def init():
    mail.init_app(app)

def send(recipient, subject, template, async=True, **kwargs):
    message = create_message(recipient, subject, template, **kwargs)
    if async:
        task(send_message, app, message)
    else:
        send_message(app, message)

def send_message(app, message):
    with app.app_context():
        mail.send(message)

def create_message(recipient, subject, template, **kwargs):
    message = Message(subject, recipients=[recipient])
    message.body = render_template("mail/" + template + ".txt", **kwargs)
    return message
