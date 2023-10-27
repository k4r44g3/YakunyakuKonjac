import os  # ディレクトリ関連
import threading

from package.fn import Fn  # 自作関数クラス
from package.debug import Debug  # デバッグ用クラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from package.system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス


class TranslateTimingThread:
    """自動翻訳のタイミングを取得するスレッドクラス"""

    def run(user_setting, window):
        """自動翻訳のタイミングを取得
        Args:
            user_setting(UserSetting): ユーザーが変更可能の設定
            window(sg.Window): Windowオブジェクト
        """
        # 翻訳間隔(秒)の取得
        translation_interval_sec = user_setting.get_setting("translation_interval_sec")

        while (
            # ウィンドウが閉じているかどうか
            not (window.was_closed())
            # 自動翻訳トグルボタンがオンかどうか
            and window["-translation_toggle-"].metadata["is_toggle_on"]
        ):
            # ウィンドウが開いてあるかつ、自動翻訳トグルボタンがオンなら
            # スレッドから、翻訳イベントを送信
            key = "-translate_thread_start-"
            value = None
            window.write_event_value(key, value)

            # 一時停止
            Fn.sleep(translation_interval_sec * 1000)
