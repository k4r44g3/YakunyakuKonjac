import os  # ディレクトリ関連
import sys  # システム関連
from typing import Any, Dict, List, Optional, Tuple, Union  # 型ヒント

import PySimpleGUI as sg  # GUI

#! デバッグ用
if __name__ == "__main__":
    src_path = os.path.join(os.path.dirname(__file__), "..", "..")  # パッケージディレクトリパス
    sys.path.append(src_path)  # モジュール検索パスを追加

from package.fn import Fn  # 自作関数クラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from package.window.base_win import BaseWin  # ウィンドウの基本クラス


class DisplaySettingWin(BaseWin):
    """表示設定画面クラス

    Args:
        BaseWin (BaseWin): ウィンドウの基本クラス
    """

    def __init__(self):
        """コンストラクタ 初期設定"""
        # 継承元のコンストラクタを呼び出す
        super().__init__()
        # todo 初期設定
        # 翻訳画面の要素を表示するかどうかの辞書の取得
        self.translation_element_visible_dict = self.user_setting.get_setting("translation_element_visible_dict")
        # ウィンドウ開始処理
        self.start_win()

    def get_layout(self):
        """ウィンドウレイアウト作成処理

        Returns:
            layout(list): ウィンドウのレイアウト
        """
        # ウィンドウのテーマを設定
        sg.theme(self.user_setting.get_setting("window_theme"))

        # 翻訳画面の要素を表示するかどうかのチェックボックスのテキストリストの取得
        translation_element_visible_checkbox_text_list = ["翻訳ボタン", "自動翻訳ボタン", "履歴選択ボックス", "翻訳前画像", "翻訳後画像"]

        # 翻訳画面の要素を表示するかどうかのチェックボックス一覧のレイアウト
        translation_element_visible_layout = []

        # チェックボックスの個数分走査
        for i in range(len(translation_element_visible_checkbox_text_list)):
            # 翻訳画面の要素を表示するかどうかの辞書のキーの取得
            dict_key = list(self.translation_element_visible_dict.keys())[i]
            # 翻訳画面の要素を表示するかどうかのチェックボックス一覧のレイアウトにチェックボックスを追加する
            translation_element_visible_layout.append(
                [
                    # 翻訳画面の要素を表示するかどうかのチェックボックス
                    sg.Checkbox(
                        text=translation_element_visible_checkbox_text_list[i],
                        key=f"-{dict_key}-",
                        default=self.translation_element_visible_dict[dict_key],  # 初期状態
                        enable_events=True,  # イベントを取得する
                    ),
                ]
            )

        # レイアウト指定
        layout = [
            [
                sg.Frame(
                    title="表示する要素",
                    layout=translation_element_visible_layout,  #  翻訳画面の要素を表示するかどうかのチェックボックス一覧のレイアウト
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
        # チェックボックスのイベントのキーリストの取得
        checkbox_event_key_list = [f"-{key}-" for key in list(self.translation_element_visible_dict.keys())]

        while not self.window.metadata["is_exit"]:  # 終了処理が行われるまで繰り返す
            # 実際に画面が表示され、ユーザーの入力待ちになる
            event, values = self.window.read()

            Fn.time_log("event=", event, "values=", values)

            # 共通イベントの処理が発生したら
            if self.base_event(event, values):
                continue

            # 確定ボタン押下イベント
            elif event == "-confirm-":
                print(values)
                update_setting = self.get_update_setting(values)  # 更新する設定の取得
                self.user_setting.save_setting_file(update_setting)  # 設定をjsonファイルに保存
                # # 翻訳画面に遷移する処理
                self.transition_to_translation_win()

            # 戻るボタン押下イベント
            elif event == "-back-":
                # 翻訳画面に遷移する処理
                self.transition_to_translation_win()

            # チェックボックス押下イベント
            elif event in checkbox_event_key_list:
                # チェックボックス押下イベント処理
                self.checkbox_event(values, checkbox_event_key_list)

    # todo イベント処理記述
    def get_update_setting(self, values):
        """更新する設定の取得

        Args:
            values (dict): 各要素の値の辞書
        Returns:
            update_setting (dict): 更新する設定の値の辞書
        """

        # 更新する設定
        update_setting = {
            # 翻訳画面の要素を表示するかどうかの辞書
            "translation_element_visible_dict": {
                "translation_button_visible": values["-translation_button_visible-"],  # 翻訳ボタン
                "toggle_auto_translation_visible": values["-toggle_auto_translation_visible-"],  # 自動翻訳ボタン
                "history_file_time_list_visible": values["-history_file_time_list_visible-"],  # 履歴選択ボックス
                "image_before_visible": values["-image_before_visible-"],  # 翻訳前画像
                "image_after_visible": values["-image_after_visible-"],  # 翻訳跡画像
            }
        }

        # 更新する設定
        return update_setting

    def checkbox_event(self, values: Dict[str, Any], checkbox_event_key_list: List[str]) -> None:
        """チェックボックス押下イベント処理

        Args:
            values (dict[str, Any]): 各要素の値の辞書
            checkbox_event_key_list (list[str]): チェックボックスのイベントのキーリスト
        """
        # チェックボックスのキーで走査
        for checkbox_event_key in checkbox_event_key_list:
            # チェックされているなら
            if values[checkbox_event_key]:
                # 更新ボタンを入力可能に変更
                self.window["-confirm-"].update(disabled=False)
                break
            # 更新ボタンを入力不可に変更
            self.window["-confirm-"].update(disabled=True)


# ! デバッグ用
if __name__ == "__main__":
    win_instance = DisplaySettingWin()
