# ! デバッグ用
import sys  # システム関連
import os  # ディレクトリ関連
import threading  # スレッド

if __name__ == "__main__":
    src_path = os.path.dirname(__file__) + "\..\.."  # パッケージディレクトリパス
    sys.path.append(src_path)  # モジュール検索パスを追加
    print(src_path)

import PySimpleGUI as sg  # GUI

from package.fn import Fn  # 自作関数クラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from package.window.base_win import BaseWin  # ウィンドウの基本クラス

from package.thread.get_key_event_thread import GetKeyEventThread  # キーイベントの取得処理を行うスレッドクラス


class KeySettingWin(BaseWin):
    """キー設定画面クラス

    Args:
        BaseWin (BaseWin): ウィンドウの基本クラス
    """

    def __init__(self):
        """コンストラクタ 初期設定"""
        # 継承元のコンストラクタを呼び出す
        super().__init__()

    def get_layout(self):
        """ウィンドウレイアウト作成処理

        Returns:
            layout(list): ウィンドウのレイアウト
        """
        # キーバインド設定情報の辞書
        self.key_binding_info_list = self.user_setting.get_setting("key_binding_info_list")

        # キーバインド設定のレイアウト
        key_binding_layout = []
        # キーバインド設定情報の走査
        for key_binding_info in self.key_binding_info_list:
            key_binding_layout.append(
                [
                    sg.Text(
                        key_binding_info["text"],
                    ),
                    sg.Button(
                        button_text=key_binding_info["key_name"],
                        size=(20, 1),
                        key=key_binding_info["gui_key"],
                    ),
                ]
            )
        # レイアウト指定
        layout = [
            [sg.Text("キー設定画面")],
            [key_binding_layout],
            [
                sg.Push(),  # 右に寄せる
                sg.Button("確定", key="-confirm-"),  # 変更ボタン
                sg.Button("戻る", key="-back-"),  # 戻るボタン
            ],
        ]
        return layout  # レイアウト

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
            enable_close_attempted_event=True,  # タイトルバーの[X]ボタン押下時にイベントが返される
            metadata={
                "is_key_input_waiting_state": False,  # キー入力待ち状態かどうか
                "is_exit": False,  # ウィンドウを閉じるかどうか
            },
        )
        return window  # GUIウィンドウ設定

    def event_start(self):
        """イベント受付開始処理
        指定したボタンが押された時などのイベント処理内容
        終了処理が行われるまで繰り返す
        """

        # キーバインド設定のイベントのリスト
        key_binding_event_list = [
            key_binding_info["gui_key"] for key_binding_info in self.key_binding_info_list
        ]

        # 終了処理が行われるまで繰り返す
        while not self.window.metadata["is_exit"]:
            # 実際に画面が表示され、ユーザーの入力待ちになる
            event, values = self.window.read()

            # Fn.time_log("event=", event, "values=", values)
            # プログラム終了イベント処理
            if event == "-WINDOW CLOSE ATTEMPTED-":  # 閉じるボタン押下,Alt+F4イベントが発生したら
                self.window_close()  # プログラム終了イベント処理

            if not self.window.metadata["is_key_input_waiting_state"]:
                # キー入力待ち状態でないなら
                # 確定ボタン押下イベント
                if event == "-confirm-":
                    # 更新する設定の取得
                    update_setting = self.get_update_setting(self.key_binding_info_list)
                    self.user_setting.save_setting_file(update_setting)  # 設定をjsonファイルに保存

                # 確定ボタン押下イベント
                elif event == "-back-":
                    self.transition_target_win = "TranslationWin"  # 遷移先ウィンドウ名
                    self.window_close()  # プログラム終了イベント処理

                # キー設定ボタン押下イベント
                elif event in key_binding_event_list:
                    # 設定変更対象のキー名
                    setting_target_key = event
                    # キー設定ボタンテキスト変更
                    self.window[event].update(text="キーを入力")
                    # キー入力待ち状態かどうか
                    self.window.metadata["is_key_input_waiting_state"] = True
                    # キーイベントを取得するスレッド作成
                    thread = threading.Thread(
                        # スレッド名
                        name="入力キー名取得スレッド",
                        # スレッドで実行するメソッド
                        target=lambda: GetKeyEventThread.run(
                            self.window,  # Windowオブジェクト
                            setting_target_key,  # 設定変更対象のキー名
                        ),
                        daemon=True,  # メインスレッド終了時に終了する
                    )
                    # スレッド開始
                    thread.start()

            else:
                # キー入力待ち状態なら
                # キー押下イベント
                if event == "-keyboard_event-":
                    # 設定変更対象のキー名
                    setting_target_key = values["-keyboard_event-"]["setting_target_key"]
                    key_name = values["-keyboard_event-"]["key_name"]  # 押下されたキー名
                    scan_code = values["-keyboard_event-"]["scan_code"]  # 押下されたスキャンコード

                    # スキャンコード重複チェック処理
                    # 他のキーバインド設定のスキャンコードリスト作成
                    key_binding_scan_code_list = []
                    # キーバインド設定の走査
                    for key_binding_info in self.key_binding_info_list:
                        # 設定を変更するキー以外なら
                        if key_binding_info["gui_key"] != setting_target_key:
                            key_binding_scan_code_list.append(key_binding_info["scan_code"])
                    # スキャンコードが他と重複していないなら
                    if scan_code not in key_binding_scan_code_list:
                        # キー入力待ち状態かどうか
                        self.window.metadata["is_key_input_waiting_state"] = False
                        # キー設定ボタンのテキスト更新
                        self.window[setting_target_key].update(text=key_name)

                        # 変更前のキーバインド設定の取得
                        old_key_binding_info = Fn.search_dict_in_list(
                            self.key_binding_info_list, "gui_key", setting_target_key
                        )

                        # 更新するキーバインド設定の作成
                        new_key_binding_info = old_key_binding_info
                        new_key_binding_info["key_name"] = key_name
                        new_key_binding_info["scan_code"] = scan_code

                        # キーバインド設定リストの更新箇所の要素番号の取得
                        update_index = self.key_binding_info_list.index(old_key_binding_info)

                        # キーバインド設定リストの更新
                        self.key_binding_info_list[update_index] = new_key_binding_info

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
        update_setting["key_binding_info_list"] = values

        # 更新する設定
        return update_setting


# ! デバッグ用
if __name__ == "__main__":
    win_instance = KeySettingWin()
