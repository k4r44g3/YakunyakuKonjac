import json  # jsonファイルの読み書き
import os  # ディレクトリ関連

from package.fn import Fn  # 自作関数クラス
from package.system_setting import SystemSetting  # ユーザーが変更不可の設定クラス


class UserSetting:
    """ユーザーが変更可能の設定クラス"""

    # デフォルトの設定
    default_user_setting = {
        "ss_left_x": 0,  # SS範囲の左側x座標
        "ss_top_y": 0,  # SS範囲の上側y座標
        "ss_right_x": 1280,  # SS範囲の右側x座標
        "ss_bottom_y": 720,  # SS範囲の下側y座標
        "ocr_soft": "Amazon Textract",  # OCRソフト
        "translation_soft": "Amazon Translate",  # 翻訳ソフト
        "source_language_code": "en",  # 翻訳元言語
        "target_language_code": "ja",  # 翻訳先言語
        "window_left_x": 0,  # ウィンドウの左側x座標
        "window_top_y": 0,  # ウィンドウの上側y座標
        "window_width": 800,  # ウィンドウの横幅
        "window_height": 600,  # ウィンドウの縦幅
        "translation_interval_sec": 20,  # 翻訳間隔
        "image_width_max": 300,  # 表示画像サイズの最大の横幅
        "image_height_max": 300,  # # 表示画像サイズの最大の縦幅
    }

    # デフォルトの設定の更新
    default_user_setting.update(
        {
            "ss_width": abs(
                default_user_setting["ss_right_x"] - default_user_setting["ss_left_x"]
            ),  # SS範囲の横幅
            "ss_height": abs(
                default_user_setting["ss_bottom_y"] - default_user_setting["ss_top_y"]
            ),  # SS範囲の縦幅
            # スクリーンショット撮影範囲(left, top, width, height)
            "ss_region": (
                default_user_setting["ss_left_x"],  # SS範囲の左側x座標
                default_user_setting["ss_top_y"],  # SS範囲の上側y座標
                abs(
                    default_user_setting["ss_right_x"] - default_user_setting["ss_left_x"]
                ),  # SS範囲の横幅
                abs(
                    default_user_setting["ss_bottom_y"] - default_user_setting["ss_top_y"]
                ),  # SS範囲の縦幅
            ),
        }
    )

    def __init__(self):
        """コンストラクタ 初期設定"""
        self.setting = self.load_setting_file()  # 設定ファイルを読み込む

    def get_setting(self, key):
        """設定を取得する

        Args:
            key(str): 設定辞書のキー

        Returns:
            setting(str): 設定辞書の値

        """
        return self.setting[key]  # 設定辞書の値

    def get_all_setting(self):
        """設定を全て取得する

        Returns:
            setting(dict): 設定
        """
        return self.setting  # 設定

    def create_setting_file(self):
        """設定ファイルを新規作成して辞書として返す

        Returns:
            default_setting(dict): デフォルトの設定
        """
        setting_file_path = SystemSetting.setting_file_path # 設定ファイルのパス
        default_setting = self.default_user_setting  # デフォルトの設定の取得
        with open(file=setting_file_path, mode="w") as f:  # ファイルを開く(書き込み)
            json.dump(obj=default_setting, fp=f, indent=2)  # ファイルの新規作成
        return default_setting  # デフォルト設定を戻り値に指定

    def load_setting_file(self):
        """設定ファイルを読み込み辞書として返す
        設定ファイルが存在しない場合は新規作成する

        Returns:
            setting(dict): 読み込んだ設定
        """
        setting_file_path = SystemSetting.setting_file_path # 設定ファイルのパス

        # 設定ファイルの読み込み処理（ファイルが存在しないなら新規作成）
        if os.path.isfile(setting_file_path):  # ファイルが存在するなら
            # ファイルが存在するなら読み込む
            with open(setting_file_path, "r") as f:  # ファイルを開く(読み込み)
                setting = json.load(f)  # ファイルを読み込む
        else:
            # ファイルが存在しないなら新規作成して読み込む
            Fn.time_log("設定ファイルが存在しません。作成します。")
            setting = self.create_setting_file()  # デフォルトを戻り値に指定
        return setting  # 設定を戻り値に指定

    def save_setting_file(self, update_setting):
        """現在の設定を更新して、jsonファイルに保存する

        Args:
            update_setting (dict): 更新する設定
        """

        setting_file_path = SystemSetting.setting_file_path # 設定ファイルのパス
        format_update_setting = self.remove_hyphens_from_keys(update_setting)  # 更新する設定の両端のハイフンを取り除く
        self.setting.update(format_update_setting)  # 現在の設定を更新

        with open(setting_file_path, "w") as f:  # ファイルを開く(書き込み)
            json.dump(obj=self.setting, fp=f, indent=2)  # ファイルに読み込む

    def remove_hyphens_from_keys(self, input_dict):
        """キー名の両端のハイフンを取り除いた辞書を返す。

        Args:
            input_dict (dict): ハイフンを取り除く対象の辞書。
        Returns:
            format_dict: ハイフンを取り除いた辞書。
        """
        print(input_dict)
        format_dict = {}  # 空辞書の作成
        for key, value in input_dict.items():  # 辞書の各キーと値で捜査
            # キーの両端にハイフンが含まれる場合、ハイフンを取り除く
            if key[0] == key[-1] == "-":
                key = key[1:-1]  # ハイフンを取り除く
            format_dict[key] = value  # 辞書の追加
        return format_dict  # ハイフンを取り除いた辞書
