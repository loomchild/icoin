from werkzeug.security import generate_password_hash, check_password_hash


class User:
    
    def __init__(self, email, name, password=None):
        self.email = email
        self.name = name
        self.password = password

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.user_id)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        if password == None:
            self.password_hash = None
        else:
            self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        if password == None or self.password_hash == None:
            return False
        return check_password_hash(self.password_hash, password)


class Page:

    def __init__(self, url):
        self.url = url
        self.domain = 'unknown'

