# ! デバッグ用
import sys  # システム関連
import os  # ディレクトリ関連

if __name__ == "__main__":
    src_path = os.path.dirname(__file__) + "\..\.."  # パッケージディレクトリパス
    sys.path.append(src_path)  # モジュール検索パスを追加
    print(src_path)

import PySimpleGUI as sg  # GUI
import pyautogui as pag  # マウスやキーボードを操作

from package.fn import Fn  # 自作関数クラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from package.system_setting import SystemSetting  # ユーザーが変更不可の設定クラス
from package.window.base_win import BaseWin  # ウィンドウの基本クラス

from package.drag_area_getter import DragAreaGetter  # ドラッグした領域の座標を取得するクラス


class ShootingSettingWin(BaseWin):
    """撮影設定画面クラス

    Args:
        BaseWin (BaseWin): ウィンドウの基本クラス
    """

    def __init__(self):
        """コンストラクタ 初期設定"""
        # 継承元のコンストラクタを呼び出す
        super().__init__()
        # todo 初期設定
        # 撮影範囲の座標情報の辞書
        self.ss_region_info_dict = {
            "left": {
                "text": "左上x座標",
                "key": "-ss_left_x-",
                "value": self.user_setting.get_setting("ss_left_x"),
            },
            "top": {
                "text": "左上y座標",
                "key": "-ss_top_y-",
                "value": self.user_setting.get_setting("ss_top_y"),
            },
            "right": {
                "text": "右下x座標",
                "key": "-ss_right_x-",
                "value": self.user_setting.get_setting("ss_right_x"),
            },
            "bottom": {
                "text": "右下y座標",
                "key": "-ss_bottom_y-",
                "value": self.user_setting.get_setting("ss_bottom_y"),
            },
        }

        # ウィンドウ開始処理
        self.start_win()

    def get_layout(self):
        """ウィンドウレイアウト作成処理

        Returns:
            layout(list): ウィンドウのレイアウト
        """
        # ウィンドウのテーマを設定
        sg.theme(self.user_setting.get_setting("window_theme"))

        # 撮影範囲表示テキストの作成
        ss_region_text = ""
        # 撮影範囲情報取得
        for ss_region_info in self.ss_region_info_dict.values():
            ss_region_text += ss_region_info["text"] + " : " + str(ss_region_info["value"]) + "\n"

        # 末尾の改行を削除
        ss_region_text = ss_region_text.rstrip("\n")

        # レイアウト指定
        layout = [
            [sg.Text("表示設定画面")],
            [
                sg.Frame(
                    title="翻訳間隔(秒)",
                    layout=[
                        [
                            sg.Input(
                                key="-translation_interval_sec-",
                                enable_events=True,
                                size=(5, 1),
                                default_text=self.user_setting.get_setting(
                                    "translation_interval_sec"
                                ),
                            ),
                        ],
                    ],
                )
            ],
            [
                sg.Frame(
                    title="撮影座標",
                    layout=[
                        # 撮影範囲設定ボタン
                        [sg.Button("撮影範囲設定", key="-set_ss_region-")],
                        # 撮影範囲表示テキスト
                        [sg.Text(text=ss_region_text, key="-ss_region_text-")],
                    ],
                )
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

            # ! デバッグログ
            if event != "__TIMEOUT__":
                Fn.time_log(event, values)

            # プログラム終了イベント処理
            if event == "-WINDOW CLOSE ATTEMPTED-":  # 閉じるボタン押下,Alt+F4イベントが発生したら
                self.window_close()  # プログラム終了イベント処理

            # 確定ボタン押下イベント
            elif event == "-confirm-":
                update_setting = values  # 更新する設定
                update_setting = self.get_update_setting(values)  # 更新する設定の取得
                self.user_setting.save_setting_file(update_setting)  # 設定をjsonファイルに保存

            # 確定ボタン押下イベント
            elif event == "-back-":
                self.transition_target_win = "TranslationWin"  # 遷移先ウィンドウ名
                self.window_close()  # プログラム終了イベント処理

            # 撮影範囲設定ボタン押下イベント
            elif event == "-set_ss_region-":
                # 撮影範囲設定ボタン押下イベント処理
                self.set_ss_region_event()

    def get_ss_region_text(self):
        """撮影範囲表示テキストの取得

        Returns:
            ss_region_text(str): 撮影範囲表示テキスト
        """

        # 撮影範囲表示テキストの作成
        ss_region_text = ""
        # 撮影範囲情報取得
        for ss_region_info in self.ss_region_info_dict.values():
            ss_region_text += ss_region_info["text"] + " : " + str(ss_region_info["value"]) + "\n"

        # 末尾の改行を削除
        ss_region_text = ss_region_text.rstrip("\n")
        return ss_region_text  # 撮影範囲表示テキスト

    def set_ss_region_event(self):
        """撮影範囲設定ボタン押下イベント処理"""
        # ドラッグした領域の座標を取得する
        now_ss_region = DragAreaGetter.run()

        # 撮影範囲の座標情報の更新
        for region_key in ["left", "top", "right", "bottom"]:
            self.ss_region_info_dict[region_key]["value"] = now_ss_region[region_key]

        # 撮影範囲表示テキストの取得
        ss_region_text = self.get_ss_region_text()
        # 撮影範囲表示テキストの更新
        self.window["-ss_region_text-"].update(value=ss_region_text)

    def get_update_setting(self, values):
        """更新する設定の取得

        Args:
            values (dict): 各要素の値の辞書
        Returns:
            update_setting (dict): 更新する設定の値の辞書
        """
        # 更新する設定
        update_setting = {}
        # キー名の両端のハイフンを取り除く
        update_setting["translation_interval_sec"] = int(
            values["-translation_interval_sec-"]
        )  # 翻訳間隔(秒)
        # 撮影範囲の左側x座標
        update_setting["ss_left_x"] = int(self.ss_region_info_dict["left"]["value"])
        # 撮影範囲の上側y座標
        update_setting["ss_top_y"] = int(self.ss_region_info_dict["top"]["value"])
        # 撮影範囲の右側x座標
        update_setting["ss_right_x"] = int(self.ss_region_info_dict["right"]["value"])
        # 撮影範囲の下側y座標
        update_setting["ss_bottom_y"] = int(self.ss_region_info_dict["bottom"]["value"])
        # 更新する設定
        return update_setting


# ! デバッグ用
if __name__ == "__main__":
    win_instance = ShootingSettingWin()
