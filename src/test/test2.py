import time
import threading
from wrapt_timeout_decorator import *

from test3 import Test3

class Test:
    @staticmethod
    @timeout(dec_timeout=100)
    def main():
        for i in range(1, 10):
            time.sleep(100)
            print("{} seconds have passed".format(i))

    @staticmethod
    def run():
        try:
            Test3.main()
            print("完了")
        except TimeoutError as e:
            print("エラー", e)


if __name__ == "__main__":
    try:
        thread = threading.Thread(
            name="スレッド作成スレッド",
            target=Test.run,
            daemon=True,
        )
        thread.start()
        print("正常")
    except TimeoutError as e:
        print("エラー")
