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
from package.window.base_win import BaseWin  # ウィンドウの基本クラス


class OutputWin(BaseWin):
    """出力画面クラス

    Args:
        BaseWin (BaseWin): ウィンドウの基本クラス
    """

    def __init__(self):
        """コンストラクタ 初期設定"""
        # todo 初期設定
        super().__init__()

    def get_layout(self):
        """ウィンドウレイアウト作成処理

        Returns:
            layout(list): ウィンドウのレイアウト
        """
        # レイアウト指定
        layout = [
            [sg.Text("出力画面")],
            [
                sg.Text("ocr_soft"),
                sg.Input(
                    key="-ocr_soft-",  # 識別子
                    disabled=True,  # 入力不可
                    default_text=self.user_setting.get_setting("ocr_soft"),  # デフォルト
                ),
            ],
            [
                sg.Text("translation_soft"),
                sg.Input(
                    key="-translation_soft-",  # 識別子
                    disabled=True,  # 入力不可
                    default_text=self.user_setting.get_setting("translation_soft"),  # デフォルト
                ),
            ],
            [
                sg.Push(),  # 右に寄せる
                sg.Button("戻る", key="-back-"),  # 戻るボタン
            ],
        ]
        return layout  # レイアウト

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

    # todo イベント処理記述


# ! デバッグ用
if __name__ == "__main__":
    win_instance = OutputWin()
