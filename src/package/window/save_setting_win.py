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


class SaveSettingWin(BaseWin):
    """保存設定画面クラス

    Args:
        BaseWin (BaseWin): ウィンドウの基本クラス
    """

    def __init__(self):
        """コンストラクタ 初期設定"""
        # 継承元のコンストラクタを呼び出す
        super().__init__()
        # todo 初期設定
        # ウィンドウ開始処理
        self.start_win()

    def get_layout(self):
        """ウィンドウレイアウト作成処理

        Returns:
            layout(list): ウィンドウのレイアウト
        """
        # ウィンドウのテーマを設定
        sg.theme(self.user_setting.get_setting("window_theme"))
        # レイアウト指定
        layout = [
            [
                sg.Text(text="最大保存容量(MB)", size=(14, 1)),
                sg.Input(
                    key="-max_file_size_mb-",  # 識別子
                    enable_events=True,  # テキストボックスの変更をイベントとして受け取れる
                    size=(6, 1),  # 要素のサイズ=(文字数, 行数)
                    default_text=self.user_setting.get_setting("max_file_size_mb"),  # デフォルト
                ),
            ],
            [
                sg.Text(text="最大保存枚数", size=(14, 1)),
                sg.Input(
                    key="-max_file_count-",  # 識別子
                    enable_events=True,  # テキストボックスの変更をイベントとして受け取れる
                    size=(6, 1),  # 要素のサイズ=(文字数, 行数)
                    default_text=self.user_setting.get_setting("max_file_count"),  # デフォルト
                ),
            ],
            [
                sg.Text(text="最大保存期間(日)", size=(14, 1)),
                sg.Input(
                    key="-max_file_retention_days-",  # 識別子
                    enable_events=True,  # テキストボックスの変更をイベントとして受け取れる
                    size=(6, 1),  # 要素のサイズ=(文字数, 行数)
                    default_text=self.user_setting.get_setting("max_file_retention_days"),  # デフォルト
                ),
            ],
            [
                sg.Push(),  # 右に寄せる
                sg.Button("確定", key="-confirm-"),  # 変更ボタン
                sg.Button("戻る", key="-back-"),  # 戻るボタン
            ],
        ]
        return layout  # レイアウト

    def event_start(self):
        """イベント受付開始処理
        指定したボタンが押された時などのイベント処理内容
        終了処理が行われるまで繰り返す
        """
        # 終了処理が行われるまで繰り返す
        while not self.window.metadata["is_exit"]:
            # 実際に画面が表示され、ユーザーの入力待ちになる
            event, values = self.window.read()

            Fn.time_log("event=", event, "values=", values)
            # プログラム終了イベント処理
            if event == "-WINDOW CLOSE ATTEMPTED-":  # 閉じるボタン押下,Alt+F4イベントが発生したら
                self.window_close()  # プログラム終了イベント処理

            # 確定ボタン押下イベント
            elif event == "-confirm-":
                update_setting = self.get_update_setting(values)  # 更新する設定の取得
                self.user_setting.save_setting_file(update_setting)  # 設定をjsonファイルに保存

            # 確定ボタン押下イベント
            elif event == "-back-":
                self.transition_target_win = "TranslationWin"  # 遷移先ウィンドウ名
                self.window_close()  # プログラム終了イベント処理

    # todo イベント処理記述
    def get_update_setting(self, values):
        """更新する設定の取得

        Args:
            values (dict): 各要素の値の辞書
        Returns:
            update_setting (dict): 更新する設定の値の辞書
        """

        # 更新する設定
        update_setting = {}
        # 最大保存容量(MB)
        update_setting["max_file_size_mb"] = int(values["-max_file_size_mb-"])
        # 最大保存枚数
        update_setting["max_file_count"] = int(values["-max_file_count-"])
        # 最大保存期間(日)
        update_setting["max_file_retention_days"] = int(values["-max_file_retention_days-"])

        # 更新する設定
        return update_setting


# ! デバッグ用
if __name__ == "__main__":
    win_instance = SaveSettingWin()
