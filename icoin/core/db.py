import uuid
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper
from sqlalchemy.dialects.postgresql import UUID
from flask.ext.migrate import Migrate

from icoin import app
from .model import Page


db = SQLAlchemy()

def init():
    url = get_url(app.config["DB_USER"], app.config["DB_PASSWORD"], 
        app.config["DB_HOST"], app.config["DB_PORT"], app.config["DB_NAME"])
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    
    db.init_app(app)
    # See http://piotr.banaszkiewicz.org/blog/2012/06/29/flask-sqlalchemy-init_app/, option 2
    db.app = app

    migrate = Migrate(app, db)

def get_url(user, password, host, port, name):
    string = "postgresql://"
    
    if user: 
        string += user
        if password:
            string += ":" + password
        string += "@"

    if host:
        string += host

    if port:
        string += ":" + port

    if name:
        string += "/" + name

    return string


page_table = db.Table('page', 
    db.Column('page_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    db.Column('url', db.String(4096), nullable=False),
    db.Column('domain', db.String(256), nullable=False),
)

mapper(Page, page_table)

