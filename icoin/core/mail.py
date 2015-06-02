from flask import render_template
from flask.ext.mail import Mail, Message
from icoin import app


mail = Mail()

def init():
    mail.init_app(app)

def send(recipient, subject, template, **kwargs):
    message = Message(subject, recipients=[recipient])
    message.body = render_template("mail/" + template + ".txt", **kwargs)
    mail.send(message)

