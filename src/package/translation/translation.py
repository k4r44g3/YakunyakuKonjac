# ! デバッグ用
import sys  # システム関連
import os  # ディレクトリ関連

if __name__ == "__main__":
    src_path = os.path.dirname(__file__) + "\..\.."  # パッケージディレクトリパス
    sys.path.append(src_path)  # モジュール検索パスを追加

from package.fn import Fn  # 自作関数クラス
from package.debug import Debug  # デバッグ用クラス
from package.translation.screenshot_capture import ScreenshotCapture  # スクリーンショット撮影機能関連のクラス
from package.translation.character_recognition import CharacterRecognition  # 文字認識機能関連のクラス
from package.translation.text_translation import TextTranslation  # テキスト翻訳機能関連のクラス
from package.translation.translation_image import TranslationImage  # オーバーレイ翻訳画像作成機能関連のクラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス


class Translation:
    """翻訳機能関連のクラス"""

    def save_history():
        """翻訳前,結果を履歴に保存する

        Returns:
            image_path(tuple(screenshot_image,overlay_translation_image)): 翻訳前、後画像のパス
                - screenshot_image(str): 翻訳前画像のパス
                - overlay_translation_image(str): 翻訳後画像のパス
        """
        Fn.time_log("システム開始")

        user_setting = UserSetting()  # ユーザ設定のインスタンス化

        # 保存ファイル名(現在日時)の取得
        file_name = Fn.get_now_file_name()

        # スクショ撮影機能
        screenshot_image = ScreenshotCapture.get_screenshot(user_setting)  # スクショ撮影
        ss_file_path = ScreenshotCapture.save_screenshot(screenshot_image, file_name)  # スクショ保存
        Fn.time_log("スクショ撮影")

        # ! デバック用
        # ss_file_path = Debug.ss_file_path  # スクショ画像パス

        # 文字認識機能
        text_data_dict = CharacterRecognition.get_text_data_dict(
            user_setting, ss_file_path
        )  # 画像からテキスト情報を取得
        text_before_list = text_data_dict["text_list"]  # 翻訳前テキストリストの取得
        text_region_list = text_data_dict["text_region_list"]  # テキスト範囲のリストの取得
        CharacterRecognition.save_text_before(text_before_list, file_name)  # 翻訳前テキストをファイルに保存
        Fn.time_log("文字取得")

        # ! デバック用
        # text_before_list = Debug.text_before_list  # 翻訳前テキストリスト
        # text_region_list = Debug.text_region_list  # テキスト範囲のリスト

        # 翻訳機能
        text_after_list = TextTranslation.get_text_after_list(
            user_setting, text_before_list
        )  # 翻訳後テキストリストの取得
        TextTranslation.save_text_after(text_after_list, file_name)  # 翻訳後テキストをファイルに保存
        Fn.time_log("翻訳")

        # ! デバック用
        # text_after_list = Debug.text_after_list  # 翻訳後テキストリスト

        # 翻訳画像作成機能
        overlay_translation_image = TranslationImage.get_overlay_translation_image(
            ss_file_path, text_after_list, text_region_list
        )  # 翻訳後画像作成

        overlay_translation_image_path = TranslationImage.save_overlay_translation_image(
            overlay_translation_image, file_name
        )  # 翻訳後画像保存

        Fn.time_log("画像作成")

        image_path = (ss_file_path, overlay_translation_image_path)  # 翻訳前、後画像のパスの取得
        return image_path  # 翻訳前、後画像のパス


# ! デバッグ用
if __name__ == "__main__":
    Translation.save_history()
