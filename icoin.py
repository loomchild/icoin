#!/usr/bin/env python3

from waitress import serve
from flask.ext.script import Manager, Shell
from flask.ext.migrate import MigrateCommand

from icoin import app
from icoin import core
from icoin.core import model
from icoin.core.db import db

manager = Manager(app, with_default_commands=False)

@manager.command
def server():
    "Run the server"
    serve(app, host=app.config["HOST"], port=app.config["PORT"], 
            threads=app.config["THREADS"])

def make_shell_context():
    return dict(app=app, db=db, model=model)
manager.add_command("shell", Shell(make_context=make_shell_context))

manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    core.init()
    manager.run()
