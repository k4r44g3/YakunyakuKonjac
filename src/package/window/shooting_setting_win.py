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


class ShootingSettingWin(BaseWin):
    """撮影設定画面クラス

    Args:
        BaseWin (BaseWin): ウィンドウの基本クラス
    """

    def __init__(self):
        """コンストラクタ 初期設定"""
        # todo 初期設定
        # 継承元のコンストラクタを呼び出す
        super().__init__()

    def get_layout(self):
        """ウィンドウレイアウト作成処理

        Returns:
            layout(list): ウィンドウのレイアウト
        """
        # 撮影範囲の座標レイアウト
        ss_region_layout = [
            [
                sg.Text("撮影範囲の左上x座標"),
                sg.Input(
                    key="-ss_left_x-",
                    enable_events=True,
                    size=(5, 1),
                    default_text=self.user_setting.get_setting("ss_left_x"),
                ),
            ],
            [
                sg.Text("撮影範囲の左上y座標"),
                sg.Input(
                    key="-ss_top_y-",
                    enable_events=True,
                    size=(5, 1),
                    default_text=self.user_setting.get_setting("ss_top_y"),
                ),
            ],
            [
                sg.Text("撮影範囲の右下x座標"),
                sg.Input(
                    key="-ss_right_x-",
                    enable_events=True,
                    size=(5, 1),
                    default_text=self.user_setting.get_setting("ss_right_x"),
                ),
            ],
            [
                sg.Text("撮影範囲の右下y座標"),
                sg.Input(
                    key="-ss_bottom_y-",
                    enable_events=True,
                    size=(5, 1),
                    default_text=self.user_setting.get_setting("ss_bottom_y"),
                ),
            ],
        ]
        # レイアウト指定
        layout = [
            [sg.Text("表示設定画面")],
            [
                sg.Frame(
                    title="説明",
                    layout=[[sg.Text("F8を押すと左上座標が、\nF9を押すと右下座標が\n現在のマウス座標から\n自動で適用されます。")]],
                )
            ],
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
            [],
            [
                sg.Frame(
                    title="現在マウス座標",
                    layout=[[sg.Text(text="(100,200)", key="-mouse_position_text-")]],
                )
            ],  # マウス座標の表示を追加
            [sg.Frame(title="撮影座標", layout=ss_region_layout)],
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
        while True:  # 終了処理が行われるまで繰り返す
            # 実際に画面が表示され、ユーザーの入力待ちになる 一定時間でタイムアウト処理
            event, values = self.window.read(timeout=SystemSetting.event_timeout_ms)

            # ! デバッグログ
            if event != "__TIMEOUT__":
                Fn.time_log(event, values)

            # プログラム終了イベント処理
            if event == "-WINDOW CLOSE ATTEMPTED-":  # 閉じるボタン押下,Alt+F4イベントが発生したら
                self.exit_event()  # イベント終了処理
                break  # イベント受付終了

            # 確定ボタン押下イベント
            elif event == "-confirm-":
                Fn.time_log("設定確定")
                update_setting = values  # 更新する設定
                update_setting = self.get_update_setting(values)  # 更新する設定の取得
                self.user_setting.save_setting_file(update_setting)  # 設定をjsonファイルに保存

            # 確定ボタン押下イベント
            elif event == "-back-":
                Fn.time_log("メイン画面に遷移")
                self.transition_target_win = "TranslationWin"  # 遷移先ウィンドウ名
                self.exit_event()  # イベント終了処理
                break  # イベント受付終了

            # タイムアウト処理
            elif event == "__TIMEOUT__":
                self.timeout_event()  # タイムアウトイベント

    # todo イベント処理記述
    def timeout_event(self):
        """タイムアウトイベント処理"""
        # マウス位置のメッセージ更新
        self.window["-mouse_position_text-"].update((pag.position()[0], pag.position()[1]))

    def get_update_setting(self, values):
        """更新する設定の取得

        Args:
            values (dict): 入力フォームの値の辞書
        Returns:
            update_setting (dict): 更新する設定の値の辞書
        """
        # 更新する設定
        update_setting = {}
        # キー名の両端のハイフンを取り除く
        update_setting["translation_interval_sec"] = int(
            values["-translation_interval_sec-"]
        )  # 翻訳間隔(秒)
        update_setting["ss_left_x"] = int(values["-ss_left_x-"])  # 撮影範囲の左側x座標
        update_setting["ss_top_y"] = int(values["-ss_top_y-"])  # 撮影範囲の上側y座標
        update_setting["ss_right_x"] = int(values["-ss_right_x-"])  # 撮影範囲の右側x座標
        update_setting["ss_bottom_y"] = int(values["-ss_bottom_y-"])  # 撮影範囲の下側y座標
        # 更新する設定
        return update_setting


# ! デバッグ用
if __name__ == "__main__":
    win_instance = ShootingSettingWin()
