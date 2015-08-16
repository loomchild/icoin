from flask.ext.security import UserMixin


class User(UserMixin):
    
    def __init__(self, name, email, password, active, roles):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
    
    @property
    def id(self):
        return self.user_id

    @property
    def roles(self):
        return []

    @roles.setter
    def roles(self, role):
        pass

class Page:

    def __init__(self, url):
        self.url = url
        self.domain = 'unknown'

class Pledge:
    
    def __init__(self, user, page, amount):
        self.user = user
        self.page = page
        self.amount = amount

class Claim:

    def __init__(self, user, page):
        self.user = user
        self.page = page

