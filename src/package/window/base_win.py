# ! デバッグ用
import sys  # システム関連
import os  # ディレクトリ関連

if __name__ == "__main__":
    src_path = os.path.dirname(__file__) + "\..\.."  # パッケージディレクトリパス
    sys.path.append(src_path)  # モジュール検索パスを追加
    print(src_path)

import PySimpleGUI as sg  # GUI

from package.fn import Fn  # 自作関数クラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス


class BaseWin:
    """ウィンドウの基本クラス"""

    def __init__(self):
        """コンストラクタ 初期設定"""
        # todo 初期設定
        self.user_setting = UserSetting()  # ユーザ設定のインスタンス化
        self.transition_target_win = None  # 遷移先ウィンドウ名
        self.start_win()  # ウィンドウ開始処理

    def start_win(self):
        """ウィンドウ開始処理"""
        Fn.time_log("ウィンドウ開始")  # ログ出力
        self.window = self.make_win()  # GUIウィンドウ作成処理
        self.window.finalize()  # GUIウィンドウ表示
        self.event_start()  # イベント受付開始処理(終了処理が行われるまで繰り返す)

    def get_layout(self):
        """ウィンドウレイアウト作成処理

        Returns:
            layout(list): ウィンドウのレイアウト
        """

    def make_win(self):
        """GUIウィンドウ作成処理

        Returns:
            window(sg.Window): GUIウィンドウ設定
        """
        # GUIウィンドウ設定
        window = sg.Window(
            title="test",  # ウィンドウタイトル
            layout=self.get_layout(),  # レイアウト指定
            resizable=True,  # ウィンドウサイズ変更可能
            # location=(50, 50),  # ウィンドウ位置
            # size=(300, 300),  # ウィンドウサイズ
            finalize=True,  # 入力待ち までの間にウィンドウを表示する
            return_keyboard_events=True,  # Trueの場合、キー押下がイベントとして処理される
            enable_close_attempted_event = True # タイトルバーの[X]ボタン押下時にイベントが返される
        )
        return window  # GUIウィンドウ設定

    def event_start(self):
        """イベント受付開始処理
        指定したボタンが押された時などのイベント処理内容
        終了処理が行われるまで繰り返す
        """

    def exit_event(self):
        """イベント終了処理"""
        # todo 終了設定(保存など)
        self.end_win()  # ウィンドウ終了処理

    def end_win(self):
        """ウィンドウ終了処理"""
        Fn.time_log("ウィンドウ終了")  # ログ出力
        self.window.close()  # ウィンドウを閉じる

    def get_transition_target_win(self):
        """遷移先ウィンドウ名の取得

        Returns:
            transition_target_win(str): 遷移先ウィンドウ名
        """
        return self.transition_target_win

    # todo イベント処理記述
    def get_update_setting(self, values):
        """更新する設定の取得

        Args:
            values (dict): 入力フォームの値の辞書
        Returns:
            update_setting (dict): 更新する設定の値の辞書
        """