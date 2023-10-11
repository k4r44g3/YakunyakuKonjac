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

class OutputWin:
    """メインウィンドウクラス"""

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

    def make_win(self):
        """GUIウィンドウ作成処理

        Returns:
            window(sg.Window): GUIウィンドウ設定
        """

        # レイアウト指定
        layout = [
            [sg.Text("出力画面")],
             [
                sg.Text("ocr_soft"),
                sg.Input(
                    key="-ocr_soft-",  # 識別子
                    disabled=True, # 入力不可
                    default_text=self.user_setting.get_setting("ocr_soft"),  # デフォルト
                ),
            ],
            [
                sg.Text("translation_soft"),
                sg.Input(
                    key="-translation_soft-",  # 識別子
                    disabled=True, # 入力不可
                    default_text=self.user_setting.get_setting("translation_soft"),  # デフォルト
                ),
            ],
            [
                sg.Push(),  # 右に寄せる
                sg.Button("戻る", key="-back-"),  # 戻るボタン
            ],
        ]
        # GUIウィンドウ設定を返す
        return sg.Window(
            title="test",  # ウィンドウタイトル
            layout=layout,  # レイアウト指定
            resizable=True,  # ウィンドウサイズ変更可能
            location=(50, 50),  # ウィンドウ位置
            size=(300, 300),  # ウィンドウサイズ
            finalize=True,  # 入力待ち までの間にウィンドウを表示する
            return_keyboard_events=True,  # Trueの場合、キー押下がイベントとして処理される
        )

    def event_start(self):
        """イベント受付開始処理
        指定したボタンが押された時などのイベント処理内容
        終了処理が行われるまで繰り返す
        """
        while True:  # 終了処理が行われるまで繰り返す
            # 実際に画面が表示され、ユーザーの入力待ちになる
            event, values = self.window.read()

            Fn.time_log("event=", event, "values=", values)
            # プログラム終了イベント処理
            if event == sg.WIN_CLOSED:  # 右上の閉じるボタン押下イベント または メニューの終了ボタン押下イベントが発生したら
                self.exit_event()  # イベント終了処理
                break  # イベント受付終了

            # 確定ボタン押下イベント
            elif event == "-back-":
                Fn.time_log("メイン画面に遷移")
                self.transition_target_win = "TranslationWin"  # 遷移先ウィンドウ名
                self.exit_event()  # イベント終了処理
                break  # イベント受付終了

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


# ! デバッグ用
if __name__ == "__main__":
    win_instance = OutputWin()
