from . import config
from . import db
from . import mail
from . import queue

def init():
    config.init()
    db.init()
    queue.init()
    mail.init()

