import uuid
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper
from sqlalchemy.dialects.postgresql import UUID
from flask.ext.migrate import Migrate

from icoin import app
from .model import User, Page, Pledge, Claim


db = SQLAlchemy()

def init():
    url = get_url(app.config["DB_USER"], app.config["DB_PASSWORD"], 
        app.config["DB_HOST"], app.config["DB_PORT"], app.config["DB_NAME"])
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    
    db.init_app(app)
    # See http://piotr.banaszkiewicz.org/blog/2012/06/29/flask-sqlalchemy-init_app/, option 2
    db.app = app

    migrate = Migrate(app, db)

def create(name):
    "Create database if it does not exist"
    url = get_url(app.config["DB_USER"], app.config["DB_PASSWORD"], 
        app.config["DB_HOST"], app.config["DB_PORT"], "postgres")
 
    engine = create_engine(url)
    with engine.connect() as conn:
 
        result = conn.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname='{}'"
            .format(name))
        if result.first():
            return False
        
        conn.execute("COMMIT")
        conn.execute("CREATE DATABASE {}".format(name))

    return True

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




user_table = db.Table('user',
    db.Column('user_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    db.Column('email', db.String(256), nullable=False),
    db.Column('name', db.String(128), nullable=False),
    db.Column('password_hash', db.String(128), nullable=True)
)

db.Index('idx_user_email', user_table.c.email, unique=True)

mapper(User, user_table)


page_table = db.Table('page', 
    db.Column('page_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    db.Column('url', db.String(4096), nullable=False),
    db.Column('domain', db.String(256), nullable=False),
)

db.Index('idx_page_url', page_table.c.url, unique=True)

mapper(Page, page_table)


pledge_table = db.Table('pledge', 
    db.Column('pledge_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    db.Column('user_id', UUID(as_uuid=True), 
        db.ForeignKey(user_table.c.user_id), nullable=False),
    db.Column('page_id', UUID(as_uuid=True), 
        db.ForeignKey(page_table.c.page_id), nullable=False),
    db.Column('amount', db.Integer(), nullable=False),
)

mapper(Pledge, pledge_table, properties={
    'user': db.relationship(User, lazy="joined"),
    'page': db.relationship(Page, lazy="joined"),
})


claim_table = db.Table('claim', 
    db.Column('claim_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    db.Column('user_id', UUID(as_uuid=True), 
        db.ForeignKey(user_table.c.user_id), nullable=False),
    db.Column('page_id', UUID(as_uuid=True), 
        db.ForeignKey(page_table.c.page_id), nullable=False),
)

mapper(Claim, claim_table, properties={
    'user': db.relationship(User, lazy="joined"),
    'page': db.relationship(Page, lazy="joined"),
})

