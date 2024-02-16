import os  # ディレクトリ関連
import sys  # システム関連

# import random
from typing import Any, Dict, List, Optional, Tuple, Union  # 型ヒント

# from PIL import Image

#! デバッグ用
if __name__ == "__main__":
    src_path = os.path.join(os.path.dirname(__file__), "..", "..")  # パッケージディレクトリパス
    sys.path.append(src_path)  # モジュール検索パスを追加

from package.debug import Debug  # デバッグ用クラス
from package.error_log import ErrorLog  # エラーログに関するクラス
from package.fn import Fn  # 自作関数クラス
from package.global_status import GlobalStatus  # グローバル変数保存用のクラス
from package.system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス
from package.translation.character_recognition import CharacterRecognition  # 文字認識機能関連のクラス
from package.translation.screenshot_capture import ScreenshotCapture  # スクリーンショット撮影機能関連のクラス
from package.translation.text_translation import TextTranslation  # テキスト翻訳機能関連のクラス
from package.translation.translation_image import TranslationImage  # オーバーレイ翻訳画像作成機能関連のクラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス


class Translation:
    """翻訳機能関連のクラス"""

    def save_tmp_history() -> Dict[str, Union[bool, Optional[str]]]:
        """翻訳前, 結果画像を一時保存する

        Returns:
            result(dict[file_name, is_error, error_name, error_text]) : 保存ファイル名とエラー情報の辞書
                - file_name(str): 保存ファイル名(撮影日時)
                - is_error(bool) : エラーが発生したかどうか
                - exception(Optional[Exception]): 発生した例外オブジェクト
        """
        # Fn.time_log("翻訳開始")

        # ウィンドウオブジェクトの取得
        window = GlobalStatus.win_instance.window

        user_setting = UserSetting()  # ユーザ設定のインスタンス化

        # 保存ファイルのベース名(撮影日時)の取得
        file_base_name = Fn.get_now_file_base_name()

        # 拡張子の取得
        file_extension = SystemSetting.image_file_extension

        # ファイル名の取得
        file_name = file_base_name + file_extension

        # スクショ撮影機能
        screenshot_image = ScreenshotCapture.get_screenshot(user_setting)  # スクショ撮影
        ss_file_path = ScreenshotCapture.save_screenshot(screenshot_image, file_name)  # スクショ保存

        # Fn.time_log(f"スクショ撮影 {file_name}")

        # ! デバック用
        # ss_file_path = Debug.ss_file_path  # スクショ画像パス
        # ss_file_path = os.path.join(Debug.debug_directory_path, "image_before.png")  # スクショ画像パス
        # # スクショ画像を開く
        # with Image.open(ss_file_path) as screenshot_image:
        #     ss_file_path = ScreenshotCapture.save_screenshot(screenshot_image, file_name)  # スクショ保存

        # 文字認識機能
        # 画像からテキスト情報を取得
        text_data_dict = CharacterRecognition.get_text_data_dict(user_setting, ss_file_path)
        text_before_list = text_data_dict["text_list"]  # 翻訳前テキストリストの取得
        text_region_list = text_data_dict["text_region_list"]  # テキスト範囲のリストの取得
        # Fn.time_log(f"文字取得 {file_name}")

        # 翻訳ウィンドウが閉じられているなら
        if window.was_closed():
            return {
                "file_name": file_name,  # 保存ファイル名(撮影日時)
                "is_error": False,  # エラーが発生したかどうか
                "exception": None,  # エラークラス
            }

        # ! デバック用
        # test_int = random.randint(100, 1000 * 5)
        # Fn.time_log(f"{file_name}, 認識, sleep:{test_int}")
        # Fn.sleep(test_int)
        # text_before_list = Debug.text_before_list  # 翻訳前テキストリスト
        # text_region_list = Debug.text_region_list  # テキスト範囲のリスト

        # 翻訳機能
        # 翻訳後テキストリストとエラー情報の取得
        text_translation_result = TextTranslation.get_text_after_list(user_setting, text_before_list)

        # 翻訳処理でエラーが発生していないなら
        if not text_translation_result["is_error"]:
            text_after_list = text_translation_result["text_after_list"]

        # 翻訳処理でエラーが発生したなら
        else:
            return {
                "file_name": file_name,  # 保存ファイル名(撮影日時)
                "is_error": True,  # エラーが発生したかどうか
                "exception": text_translation_result["exception"],  # エラークラス
            }

        # Fn.time_log(f"翻訳 {file_name}")

        # ! デバック用
        # test_int = random.randint(100, 1000 * 5)
        # Fn.time_log(f"{file_name}, 翻訳, sleep:{test_int}")
        # Fn.sleep(test_int)
        # text_after_list = Debug.text_after_list  # 翻訳後テキストリスト
        # text_after_list = text_before_list  # 翻訳後テキストリスト

        # 翻訳画像作成機能
        # 翻訳後画像作成
        overlay_translation_image = TranslationImage.get_overlay_translation_image(
            user_setting, ss_file_path, text_after_list, text_region_list
        )
        # 翻訳後画像保存
        overlay_translation_image_path = TranslationImage.save_overlay_translation_image(
            overlay_translation_image, file_name
        )

        # Fn.time_log(f"画像作成 {file_name}")

        # ! デバッグ用
        # overlay_translation_image.show()  # 画像表示

        # Fn.time_log("翻訳終了")

        return {
            "file_name": file_name,  # 保存ファイル名(撮影日時)
            "is_error": False,  # エラーが発生したかどうか
            "exception": None,  # エラークラス
        }


# ! デバッグ用
if __name__ == "__main__":
    # AWSの設定ファイルのパスの設定
    os.environ["AWS_CONFIG_FILE"] = SystemSetting.aws_config_file_path
    # AWSの認証情報ファイルのパスの設定
    os.environ["AWS_SHARED_CREDENTIALS_FILE"] = SystemSetting.aws_credentials_file_path
    # 翻訳前, 結果画像を一時保存する
    image_path = Translation.save_tmp_history()
