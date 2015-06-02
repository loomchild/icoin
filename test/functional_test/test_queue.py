from time import sleep
from nose.tools import *
from . import clean_db
from icoin.core.queue import pq

class TestQueue:

    def setUp(self):
        clean_db()
    
    def test_queue(self):
        queue = pq['test']
        
        queue.put({"k1" : "v1"})
        queue.put({"k2" : "v2", "k3" : ["v3.1", "v3.2"]})
        
        task1 = queue.get()
        eq_("v1", task1.data["k1"])

        task2 = queue.get()
        eq_("v2", task2.data["k2"])
        eq_(["v3.1", "v3.2"], task2.data["k3"])

        eq_(None, queue.get())

