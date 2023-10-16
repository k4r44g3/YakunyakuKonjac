# ! デバッグ用
import sys  # システム関連
import os  # ディレクトリ関連

if __name__ == "__main__":
    src_path = os.path.dirname(__file__) + "\..\.."  # パッケージディレクトリパス
    sys.path.append(src_path)  # モジュール検索パスを追加
    print(src_path)

import PySimpleGUI as sg  # GUI

from package.fn import Fn  # 自作関数クラス
from package.debug import Debug  # デバッグ用クラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from package.system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス
from package.translation.translation import Translation  # 翻訳機能関連のクラス

# from package.window.window import Window  # 翻訳機能関連のクラス


class TranslationWin:
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

        # 最新の翻訳後画像名の取得
        now_image_name = Fn.get_max_file_name(SystemSetting.image_after_directory_path)

        # 最新の翻訳画像パスの取得
        if now_image_name != ".gitkeep":
            # 履歴が存在するなら最新の画像パスを取得
            now_after_image_path = (
                SystemSetting.image_after_directory_path + now_image_name
            )  # 翻訳後画像の保存先パス
            now_before_image_path = (
                SystemSetting.image_before_directory_path + now_image_name
            )  # 翻訳前画像の保存先パス
        else:
            # 履歴が存在しないならデフォルトの画像パスを取得
            now_after_image_path = Debug.overlay_translation_image_path  # 翻訳後画像の保存先パス
            now_before_image_path = Debug.ss_file_path  # 翻訳前画像の保存先パス

        # todo ウィンドウのテーマの設定

        # メニューバー設定
        menuber = [
            ["設定 (&C)", ["設定 (&O)::menu_setting::", "---", "終了 (&X)::menu_exit::"]],
            [
                "入力 (&I)",
                ["入力画面 (&I)::menu_input::"],
            ],
            [
                "出力 (&O)",
                ["出力画面 (&O)::menu_output::"],
            ],
        ]

        # レイアウト指定
        layout = [
            [[sg.Menu(menuber, key="-menu-")]],  # メニューバー
            [
                # 自動翻訳用トグルボタン
                sg.Button(
                    button_text="翻訳",  # ボタンテキスト
                    key="-translation_toggle-",  # 識別子
                    size=(4 * 5, 2 * 2),  # サイズ(フォントサイズ)(w,h)
                    # expand_x = True, #  Trueの場合、要素はx方向に自動的に拡大
                    # expand_y = True, #  Trueの場合、要素はy方向に自動的に拡大
                ),
            ],
            [
                # 翻訳前の画像表示
                sg.Column(
                    [
                        [
                            sg.Image(
                                # filename=SystemSetting.image_after_directory_path + "20231005_142830_721.png",
                                source=now_before_image_path,  # 翻訳前画像の保存先パス
                                key="-before_image-",  # 識別子
                                enable_events=True,  # イベントを取得する
                                subsample=1,  # 画像のサイズを縮小する量
                                # メタデータ
                                metadata={
                                    "source": now_before_image_path,  # 翻訳前画像の保存先パス
                                    "subsample": 1,  # 画像のサイズを縮小する量
                                },
                            ),
                        ],
                    ],
                    size=(400, 225),  # 表示サイズ
                    scrollable=True,  # スクロールバーの有効化
                    background_color="#888",  # 背景色
                ),
            ],
            [  # 翻訳後の画像表示
                sg.Column(
                    [
                        [
                            sg.Image(
                                # filename=SystemSetting.image_after_directory_path + "20231005_142830_721.png",
                                source=now_after_image_path,  # 翻訳後画像の保存先パス
                                key="-after_image-",  # 識別子
                                enable_events=True,  # イベントを取得する
                                subsample=1,  # 画像縮小率 サイズ/n
                                metadata={
                                    "source": now_after_image_path,  # 翻訳後画像の保存先パス
                                    "subsample": 1,  # 画像のサイズを縮小する量
                                },  # メタデータ
                            ),
                        ],
                    ],
                    size=(400, 225),  # 表示サイズ
                    scrollable=True,  # スクロールバーの有効化
                    background_color="#888",  # 背景色
                ),
            ],
        ]
        # GUIウィンドウ設定を返す
        return sg.Window(
            title=SystemSetting.app_name,  # ウィンドウタイトル
            layout=layout,  # レイアウト指定
            resizable=True,  # ウィンドウサイズ変更可能
            # ウィンドウ位置
            location=(
                self.user_setting.get_setting("window_left_x"),
                self.user_setting.get_setting("window_top_y"),
            ),
            # ウィンドウサイズ
            # size=(
            # self.user_setting.get_setting("window_width"),
            # self.user_setting.get_setting("window_height")
            # ),
            finalize=True,  # 入力待ち までの間にウィンドウを表示する
            return_keyboard_events=True,  # Trueの場合、キー押下がイベントとして処理される
        )

    def event_start(self):
        """イベント受付開始処理
        指定したボタンが押された時などのイベント処理内容
        終了処理が行われるまで繰り返す
        """

        # todo ウィンドウ初期設定
        # 画像縮小率の変更
        self.image_size_change("-after_image-")
        self.image_size_change("-before_image-")

        while True:  # 終了処理が行われるまで繰り返す
            # 実際に画面が表示され、ユーザーの入力待ちになる
            event, values = self.window.read()

            # Fn.time_log(event, values)
            # プログラム終了イベント処理
            if event == sg.WIN_CLOSED:  # 右上の閉じるボタン押下イベントが発生したら
                self.exit_event()  # イベント終了処理
                break  # イベント受付終了

            # 自動翻訳ボタン押下イベント
            elif event == "-translation_toggle-":
                Fn.time_log("自動翻訳ボタン押下イベント開始")
                self.translate()  # 翻訳処理

            # 画像クリックイベント
            elif event == "-after_image-" or event == "-before_image-":
                self.image_size_change(event)  # 画像縮小率の変更

            # メニューバーの設定押下イベント
            elif "::menu_input::" in event:
                Fn.time_log("入力画面に遷移")
                self.transition_target_win = "InputWin"  # 遷移先ウィンドウ名
                self.exit_event()  # イベント終了処理
                break  # イベント受付終了

            # メニューバーの設定押下イベント
            elif "::menu_output::" in event:
                Fn.time_log("出力画面に遷移")
                self.transition_target_win = "OutputWin"  # 遷移先ウィンドウ名
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

    def translate(self):
        """翻訳処理"""
        image_path = Translation.save_history()  # 翻訳する

        ss_file_path, overlay_translation_image_path = image_path  # 翻訳前、後画像のパスの取得

        for key in ("-after_image-", "-before_image-"):
            # メタデータ更新
            if key == "-after_image-":
                self.window[key].metadata["source"] = overlay_translation_image_path
            else:
                self.window[key].metadata["source"] = ss_file_path

            # 要素の更新
            self.window[key].update(
                source=self.window[key].metadata["source"],  # ファイル名
                subsample=self.window[key].metadata["subsample"],  # 画像縮小率
            )

    def image_size_change(self, key):
        """画像縮小率の変更

        Args:
            key (str): 要素識別子
        """
        # 画像縮小率の取得 サイズ/n
        subsample = self.window[key].metadata["subsample"]

        # 変更する画像縮小率の取得・変更
        new_subsample = None
        if subsample == 1:
            new_subsample = 4
        elif subsample == 2:
            new_subsample = 1
        elif subsample == 4:
            new_subsample = 2

        # メタデータ更新
        self.window[key].metadata["subsample"] = new_subsample

        # 要素の更新
        self.window[key].update(
            source=self.window[key].metadata["source"],  # ファイル名
            subsample=self.window[key].metadata["subsample"],  # 画像縮小率
        )


# ! デバッグ用
if __name__ == "__main__":
    win_instance = TranslationWin()
