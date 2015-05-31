from nose.tools import *
from . import *
import icoin
from icoin.core.db import db
from icoin.core.model import Page


class TestDB:

    def setup(self):
        self.app = icoin.app.test_client()
        clean_db()
    
    def test_db(self):
        page = Page("http://icoin.io/test")
        db.session.add(page)
        db.session.commit()

        pages = db.session.query(Page).all()
        eq_([page], pages)


