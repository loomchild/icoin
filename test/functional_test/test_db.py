from nose.tools import *
from . import *
from icoin.core.db import db
from icoin.core.model import Page


class TestDB:

    def setUp(self):
        clean_db()
    
    def test_db(self):
        page = Page("http://icoin.io/test")
        db.session.add(page)
        db.session.commit()

        pages = db.session.query(Page).all()
        eq_([page], pages)


