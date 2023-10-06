import os  # ファイル操作
from decimal import Decimal  # 固定小数点

from fn import Fn  # 自作関数クラス
from debug import Debug  # デバッグ用クラス
import pyautogui as pag  # スクショ撮影
import PySimpleGUI as sg  # GUI
from user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス

from translation import Translation # 翻訳機能関連のクラス




class TranslationWin:
    """メインウィンドウクラス"""

    def __init__(self):
        """コンストラクタ 初期設定"""
        # スクショ関連設定
        self.is_enable_SS = False  # スクショを撮るかどうか　スクショ用フラグ
        self.start()  # ウィンドウ処理を開始する

    def start(self):
        """ウィンドウ開始処理"""
        self.window = self.make_win()  # GUIウィンドウを作成
        self.window.finalize()  # GUIウィンドウ表示
        self.event_start()  # GUIのボタン入力受付処理(終了処理が行われるまで繰り返して状態保存)

    def end(self):
        """ウィンドウ終了処理"""


    def make_win(self):
        """GUIウィンドウを作成する"""

        # todo ウィンドウのテーマの設定
        # sg.theme()

        # todo メニューバー設定
        # menuber = []

        # レイアウト指定
        layout = [
             # todo メニューバー
            # [sg.Menu(menuber, key="-menu-")],
            [
                # 翻訳用トグルボタン
                sg.Button(
                    "開始",
                    key="-translation_toggle-",
                    expand_x=True,
                    expand_y=True,
                )
            ],
        ]
        # GUIウィンドウ設定を返す
        return sg.Window(
            title=SystemSetting.app_name, # ウィンドウタイトル
            layout=layout, # レイアウト指定
            resizable=True,  # ウィンドウサイズ変更可能
            location=(
                UserSetting.window_left_x,
                UserSetting.window_top_y,
            ),  # ウィンドウ位置
            size=(
                UserSetting.window_width,
                UserSetting.window_height,
            ),  # ウィンドウサイズ
            finalize=True,  # window.read() までの間にウィンドウを表示できる
            return_keyboard_events=True,  # Trueの場合、キーボードイベントが windows.read() で返ってくる
        )

    def translate(self):
        """翻訳メソッド"""
        Translation.save_history() # 翻訳する

    def exit_event(self):
        """プログラム終了イベント処理"""
        self.is_enable_SS = False  # スクショ撮影フラグをoff
        Fn.time_log("終了")  # ログ出力
        self.end()  # ウィンドウ終了処理
        self.state = "exit"  # 現在のウィンドウ終了時にシステム終了するよう保存


    # def screenshot_start_stop_event(self):
    #     """SS自動撮影開始/停止イベントの処理"""
    #     self.is_enable_SS = not self.is_enable_SS  # スクショを撮るかどうかのスクショ用フラグ切り替え  開始/停止の切り替え
    #     # SS自動撮影開始/停止イベントの処理
    #     if self.is_enable_SS:  # 開始するなら
    #         # 開始処理
    #         self.window["-screen_shot_toggle-"].update(
    #             text="停止 (" + SystemSetting.screenshot_start_stop_key_text + ")"
    #         )  # ボタンテキスト更新
    #         self.screen_shot()  # スクショ撮影
    #     else:  # 停止するなら
    #         # 停止処理
    #         self.window["-screen_shot_toggle-"].update(
    #             text="開始 (" + SystemSetting.screenshot_start_stop_key_text + ")"
    #         )  # ボタンテキスト更新

    # def screenshot_start_stop_event(self):
    #     """SS自動撮影開始/停止イベントの処理"""
    #     self.is_enable_SS = not self.is_enable_SS  # スクショを撮るかどうかのスクショ用フラグ切り替え  開始/停止の切り替え
    #     # SS自動撮影開始/停止イベントの処理
    #     if self.is_enable_SS:  # 開始するなら
    #         # 開始処理
    #         self.window["-screen_shot_toggle-"].update(
    #             text="停止 (" + SystemSetting.screenshot_start_stop_key_text + ")"
    #         )  # ボタンテキスト更新
    #         self.screen_shot()  # スクショ撮影
    #     else:  # 停止するなら
    #         # 停止処理
    #         self.window["-screen_shot_toggle-"].update(
    #             text="開始 (" + SystemSetting.screenshot_start_stop_key_text + ")"
    #         )  # ボタンテキスト更新

    # def timeout_event(self):
    #     """タイムアウト処理(一定間隔SS撮影,ウィンドウ範囲保存)"""
    #     self.window_range = [self.window.current_location(), self.window.size]  # ウィンドウ範囲保存
    #     if self.is_enable_SS:  # SS自動撮影を開始しているなら
    #         self.screen_shot()  # スクショ撮影

    def event_start(self):
        """イベント受付メソッド
        指定したボタンが押された時などのイベント処理内容
        """
        while True:  # 終了処理が行われるまで繰り返す
            # 実際に画面が表示され、ユーザーの入力待ちになる  SS撮影間隔(0.1秒刻み)間入力が無いとタイムアウト
            event, values = self.window.read(
                timeout=UserSetting.translation_interval_sec * 1000,
                timeout_key="-timeout-",
            )

            # if event != "-timeout-":  # タイムアウトで無いなら
            #     Fn.time_log("event: ", event, "    values: ", values)  # ログ出力

            # プログラム終了イベント処理
            if (
                event == sg.WIN_CLOSED or "::menu_exit::" in event
            ):  # 右上の閉じるボタン押下イベント または メニューの終了ボタン押下イベントが発生したら
                self.exit_event()  # プログラム終了イベント処理
                break  # イベント受付終了

            # # 設定ウィンドウ遷移処理
            # if "::menu_UserSetting::" in event:  # メニューバーの設定押下イベントが発生したら
            #     self.menu_UserSetting_event()  # 設定ウィンドウ遷移処理
            #     break  # イベント受付終了

            # # SS自動撮影開始/停止イベントの処理
            # if (
            #     event == "-screen_shot_toggle-" or event == SystemSetting.screenshot_start_stop_key
            # ):  # スクショ用トグルボタン押下イベント 又は SS自動撮影開始/停止キー押下イベントが発生したら
            #     self.screenshot_start_stop_event()  # SS自動撮影開始/停止イベントの処理

            # # タイムアウト処理(一定間隔SS撮影,ウィンドウ範囲保存)
            # if event == "-timeout-":  # タイムアウトイベントが発生したなら
            #     self.timeout_event()  # タイムアウト処理(一定間隔SS撮影,ウィンドウ範囲保存)