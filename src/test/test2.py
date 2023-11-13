import keyboard
import threading

class KeyboardListener:
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.timer = None
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, event):
        # キーボードイベントが発生したときの処理
        print(f"Key pressed: {event.name}")
        # タイマーをリセット
        if self.timer is not None:
            self.timer.cancel()
        self.timer = threading.Timer(self.timeout, self.stop_listener)
        self.timer.start()

    def stop_listener(self):
        # リスナーを停止する処理
        print("No keyboard event occurred. Stopping listener.")
        self.listener.stop()

# リスナーを起動し、10秒間キーボードイベントがなければ停止する
keyboard_listener = KeyboardListener(timeout=10)
