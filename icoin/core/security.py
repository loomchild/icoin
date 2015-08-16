from uuid import UUID
from flask_security import Security
from flask_security.datastore import SQLAlchemyDatastore, UserDatastore
from flask_security.forms import RegisterForm
from wtforms import StringField
from wtforms.validators import Required, Length, Regexp
from icoin import app
from .model import User
from .db import db
from .config import DefaultConfig
 

security = Security()

def init():
    app.config['SECURITY_REGISTERABLE'] = True
    app.config['SECURITY_CONFIRMABLE'] = True
    app.config['SECURITY_PASSWORD_HASH'] = "bcrypt"
    
    # Update all salts with SECRET_KEY if they are not set
    secret_key = app.config['SECRET_KEY']
    for salt in ('SECURITY_PASSWORD_SALT', 'SECURITY_CONFIRM_SALT', 
            'SECURITY_RESET_SALT', 'SECURITY_LOGIN_SALT', 
            'SECURITY_REMEMBER_SALT'):
        app.config[salt] = app.config.get(salt, secret_key)

    app.config['SECURITY_EMAIL_SENDER'] = app.config['MAIL_DEFAULT_SENDER']

    security.init_app(app, IcoinUserDatastore(),
            confirm_register_form=IcoinRegisterForm)


class IcoinUserDatastore(SQLAlchemyDatastore, UserDatastore):
    
    def __init__(self):
        SQLAlchemyDatastore.__init__(self, db)
        UserDatastore.__init__(self, User, None)

    def get_user(self, identifier):
        if isinstance(identifier, UUID):
            user = db.session.query(User).get(identifier)
        else:
            user = db.session.query(User).filter_by(email=identifier).first()
        return user

    def find_user(self, **kwargs):
        if "id" in kwargs:
            kwargs["user_id"] = kwargs["id"]
            del kwargs["id"]
        user = db.session.query(User).filter_by(**kwargs).first()
        return user

    def find_role(self, role):
        return None

class IcoinRegisterForm(RegisterForm):
    
    name = StringField('Name', validators=[Required(), Length(1, 64), 
            Regexp(r'^[A-Za-z0-9_\- ]+$', 0, 'Name must have only letters, numbers, spaces, dots, dashes or underscores')])
