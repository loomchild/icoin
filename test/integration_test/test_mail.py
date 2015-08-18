from time import sleep
from icoin import app
from icoin.core.mail import mail, send

class TestMail:

    def test_send_sync(self):    
        with app.app_context(), mail.record_messages() as outbox:
            send("test@test.com", "subjectnow", "test", async=False)

            assert len(outbox) == 1
            assert outbox[0].subject == "subjectnow"
    
    def test_send_async(self):    
        with app.app_context(), mail.record_messages() as outbox:
            send("test@test.com", "subject", "test")
            
            # message is not sent immediately
            assert len(outbox) == 0

            sleep(0.1)

            assert len(outbox) == 1
            assert outbox[0].subject == "subject"

