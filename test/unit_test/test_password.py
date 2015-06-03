from nose.tools import *

from icoin.core.model import User


def test_password_setter():
    user = User("jane@bountyfunding.org", "Jane", 'cat')
    assert user.password_hash is not None

@raises(AttributeError)
def test_no_password_getter():
    user = User("jane@bountyfunding.org", "Jane", 'cat')
    user.password

def test_password_verification():
    user = User("jane@bountyfunding.org", "Jane", 'cat')
    assert user.verify_password('cat')
    assert user.verify_password('dog') == False

def test_password_salts_are_random():
    user1 = User("jane@bountyfunding.org", "Jane", 'cat')
    user2 = User("john@bountyfunding.org", "John", 'cat')
    assert user1.password_hash != user2.password_hash

def test_empty_password():
    user = User("jane@bountyfunding.org", "Jane", None)
    assert user.verify_password('cat') == False
    assert user.verify_password('') == False
    assert user.verify_password(None) == False

