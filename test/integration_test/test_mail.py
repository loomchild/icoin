from time import sleep
from nose.tools import *
from icoin import app
from icoin.core.mail import mail, send

class TestMail:

    def test_send_sync(self):    
        with app.app_context(), mail.record_messages() as outbox:
            send("test@test.com", "subjectnow", "test", async=False)

            eq_(1, len(outbox))
            eq_("subjectnow", outbox[0].subject)
    
    def test_send_async(self):    
        with app.app_context(), mail.record_messages() as outbox:
            send("test@test.com", "subject", "test")
            
            # message is not sent immediately
            eq_(0, len(outbox))

            sleep(0.1)

            eq_(1, len(outbox))
            eq_("subject", outbox[0].subject)

