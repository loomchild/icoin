from nose.tools import *
from icoin import app
from icoin.core.mail import mail, send

class TestMail:

    def test_send(self):    
        with app.app_context(), mail.record_messages() as outbox:
            send("test@test.com", "subject", "test")

            eq_(1, len(outbox))
            eq_("subject", outbox[0].subject)
