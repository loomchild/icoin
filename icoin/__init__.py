from flask import Flask

app = Flask(__name__)

from .core import bootstrap

bootstrap.init()

from .api import api

app.register_blueprint(api)

from .gui import gui

app.register_blueprint(gui)


