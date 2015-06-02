from . import config
from . import db
from . import mail

def init():
    config.init()
    db.init()
    mail.init()

