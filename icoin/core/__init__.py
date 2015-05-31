from . import config
from . import db

def init():
    config.init()
    db.init()

