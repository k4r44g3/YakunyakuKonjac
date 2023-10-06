import os  # ファイル操作
from decimal import Decimal  # 固定小数点

from fn import Fn  # 自作関数クラス
from debug import Debug  # デバッグ用クラス
import pyautogui as pag  # スクショ撮影
import PySimpleGUI as sg  # GUI
from user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス

from translation import Translation  # 翻訳機能関連のクラス


class TranslationWin:
    """メインウィンドウクラス"""

    def __init__(self):
        """コンストラクタ 初期設定"""
        # todo 初期設定
        self.is_event_exists = True  # イベントが存在するかどうか
        self.transition_target_win = None  # 遷移先ウィンドウ名
        self.start_win()  # ウィンドウ開始処理

    def start_win(self):
        """ウィンドウ開始処理"""
        Fn.time_log("ウィンドウ開始")  # ログ出力
        self.window = self.make_win()  # GUIウィンドウ作成処理
        self.window.finalize()  # GUIウィンドウ表示
        self.event_start()  # イベント受付開始処理(終了処理が行われるまで繰り返す)

    def make_win(self):
        """GUIウィンドウ作成処理"""

        # todo ウィンドウのテーマの設定

        # todo メニューバー設定

        # レイアウト指定
        layout = [
            # todo メニューバー
            [
                # 自動翻訳用トグルボタン
                sg.Button(
                    button_text="翻訳",  # ボタンテキスト
                    key="-translation_toggle-",  # 識別子
                    size=(4 * 5, 2 * 2),  # サイズ(フォントサイズ)(w,h)
                    expand_x = True, #  Trueの場合、要素はx方向に自動的に拡大
                    expand_y = True, #  Trueの場合、要素はy方向に自動的に拡大

                ),
            ],
            # todo 画像表示
            # [  # 画像表示
            #     sg.Image(
            #         filename=SystemSetting.image_after_directory_path + "20231005_142830_721.png",
            #         key="-image-",
            #         size=(300,200),  # サイズ(px)(w,h)
            #     ),
            # ],
        ]
        # GUIウィンドウ設定を返す
        return sg.Window(
            title=SystemSetting.app_name,  # ウィンドウタイトル
            layout=layout,  # レイアウト指定
            resizable=True,  # ウィンドウサイズ変更可能
            # ウィンドウ位置
            location=(
                UserSetting.window_left_x,
                UserSetting.window_top_y,
            ),
            # ウィンドウサイズ
            size=(
                UserSetting.window_width,
                UserSetting.window_height,
            ),
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

            Fn.time_log(event, values)
            # プログラム終了イベント処理
            if event == sg.WIN_CLOSED:  # 右上の閉じるボタン押下イベントが発生したら
                self.is_end_system = True  # システムを終了させるかどうか
                self.exit_event()  # イベント終了処理
                break  # イベント受付終了

            # 自動翻訳ボタン押下イベント
            elif event == "-translation_toggle-":
                Fn.time_log("自動翻訳ボタン押下イベント開始")
                self.translate()  # 翻訳処理

    def exit_event(self):
        """イベント終了処理"""
        # todo 終了設定(保存など)
        self.end_win()  # ウィンドウ終了処理

    def end_win(self):
        """ウィンドウ終了処理"""
        Fn.time_log("ウィンドウ終了")  # ログ出力

    # todo イベント処理記述

    def translate(self):
        """翻訳処理"""
        Translation.save_history()  # 翻訳する


# ! デバッグ用
if __name__ == "__main__":
    win_instance = TranslationWin()
