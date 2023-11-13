import time
import threading
from wrapt_timeout_decorator import *
class Test3:
    @timeout(dec_timeout=100)
    def main():
        for i in range(1, 10):
            time.sleep(100)
            print("{} seconds have passed".format(i))