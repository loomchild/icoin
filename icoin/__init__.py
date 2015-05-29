from flask import Flask

app = Flask(__name__)

from .gui import gui

app.register_blueprint(gui)

app.config['SECRET_KEY'] = 'B0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

