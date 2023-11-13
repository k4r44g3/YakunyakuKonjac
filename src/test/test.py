import multiprocessing
import time


def mytest():
    print("Start")
    for i in range(1, 10):
        time.sleep(100)
        print("{} seconds have passed".format(i))


if __name__ == "__main__":
    # 関数をプロセスとして実行
    p = multiprocessing.Process(target=mytest)
    p.start()

    # 5秒後にタイムアウト
    p.join(5)

    if p.is_alive():
        print("mytest is not finished within 5 seconds")
        p.terminate()  # プロセスを強制終了
        p.join()
