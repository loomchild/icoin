from time import sleep
from nose.tools import *
from icoin.core.queue import task, wait


class TestQueue:

    def setUp(self):
        self.data = None

    def func(self, a, b):
        self.data = (a, b)

    def test_queue(self):
        task(self.func, 1, b=2)

        sleep(0.1)

        eq_((1,2), self.data)

