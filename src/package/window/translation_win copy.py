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
        self.transition_target_win = None  # 遷移先ウィンドウ名
        print(Debug.overlay_translation_image_path)
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
                    # expand_x = True, #  Trueの場合、要素はx方向に自動的に拡大
                    # expand_y = True, #  Trueの場合、要素はy方向に自動的に拡大
                ),
            ],
            # todo 画像表示
            [  # リサイズした翻訳後の画像表示
                sg.Column(
                    [
                        [
                            sg.Image(
                                # filename=SystemSetting.image_after_directory_path + "20231005_142830_721.png",
                                source=Debug.overlay_translation_image_path,  # リサイズした翻訳後画像の保存先パス
                                key="-after_image-",  # 識別子
                                enable_events=True,  # イベントを取得する
                                subsample=4,  # 画像縮小率 サイズ/n
                                metadata={
                                    "source": Debug.overlay_translation_image_path,  # リサイズした翻訳後画像の保存先パス
                                    "subsample": 4,  # 画像のサイズを縮小する量
                                },  # メタデータ
                            ),
                        ],
                    ],
                    size=(400, 225),  # 表示サイズ
                    scrollable=True,  # スクロールバーの有効化
                    background_color="#888",  # 背景色
                ),
            ],
            [
                # リサイズした翻訳前の画像表示
                sg.Column(
                    [
                        [
                            sg.Image(
                                # filename=SystemSetting.image_after_directory_path + "20231005_142830_721.png",
                                source=Debug.ss_file_path,  # リサイズした翻訳前画像の保存先パス
                                key="-before_image-",  # 識別子
                                enable_events=True,  # イベントを取得する
                                subsample=4,  # 画像のサイズを縮小する量
                                # メタデータ
                                metadata={
                                    "source": Debug.ss_file_path,  # リサイズした翻訳前画像の保存先パス
                                    "subsample": 4,  # 画像のサイズを縮小する量
                                },
                            ),
                        ],
                    ],
                    size=(400, 225),  # 表示サイズ
                    scrollable=True,  # スクロールバーの有効化
                    background_color="#888",  # 背景色
                ),
            ],
            # [
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
            # size=(
            #     UserSetting.window_width,
            #     UserSetting.window_height,
            # ),
            finalize=True,  # 入力待ち までの間にウィンドウを表示する
            return_keyboard_events=True,  # Trueの場合、キー押下がイベントとして処理される
        )

    def event_start(self):
        """イベント受付開始処理
        指定したボタンが押された時などのイベント処理内容
        終了処理が行われるまで繰り返す
        """
        print(self.window["-after_image-"].get_size())
        self.window["-after_image-"].metadata["default_size"] = self.window[
            "-after_image-"
        ].get_size()

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

            # 画像クリックイベント
            elif event == "-after_image-" or event == "-before_image-":
                self.image_size_change(event)

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

    def image_size_change(self, key):
        """画像縮小率の変更

        Args:
            key (str): 要素識別子
        """
        # デフォルトの画像サイズ
        default_size = self.window[key].metadata["default_size"]

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

        print(new_subsample, default_size, [data * 4 / new_subsample for data in default_size])
        new_size = (default_size[0] * (4 // new_subsample), default_size[1] * (4 // new_subsample))
        print(default_size, new_size)
        # メタデータ更新
        self.window[key].metadata["subsample"] = new_subsample

        # 要素の更新
        self.window[key].update(
            source=self.window[key].metadata["source"],  # ファイル名
            subsample=new_subsample,  # 画像縮小率
            size=new_size,
        )


# ! デバッグ用
if __name__ == "__main__":
    win_instance = TranslationWin()
