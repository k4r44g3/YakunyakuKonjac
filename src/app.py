from fn import Fn  # 自作関数クラス
from debug import Debug  # デバッグ用クラス
from screenshot_capture import ScreenshotCapture  # スクリーンショット撮影機能関連のクラス
from character_recognition import CharacterRecognition  # 文字認識機能関連のクラス
from text_translation import TextTranslation  # 翻訳機能関連のクラス
from translation_image import TranslationImage  # オーバーレイ翻訳画像作成機能関連のクラス


Fn.time_log("システム開始")

# 保存ファイル名(現在日時)の取得
file_name = Fn.get_now_file_name()

# スクショ撮影機能
screenshot_image = ScreenshotCapture.get_screenshot()  # スクショ撮影
ss_file_path = ScreenshotCapture.save_screenshot(screenshot_image, file_name)  # スクショ保存
Fn.time_log("スクショ撮影")


# デバック用
ss_file_path = Debug.ss_file_path  # スクショ画像パス


# 文字認識機能
text_data_dict = CharacterRecognition.get_text_data_dict(ss_file_path)  # 画像からテキスト情報を取得
text_before_list = text_data_dict["text_list"]  # 翻訳前テキストリストの取得
text_region_list = text_data_dict["text_region_list"]  # テキスト範囲のリストの取得
CharacterRecognition.save_text_before(text_before_list, file_name)  # 翻訳前テキストをファイルに保存
Fn.time_log("文字取得")


# デバック用
# text_before_list = Debug.text_before_list  # 翻訳前テキストリスト
# text_region_list = Debug.text_region_list  # テキスト範囲のリスト


# 翻訳機能
text_after_list = TextTranslation.get_text_after_list(text_before_list)  # 翻訳後テキストリストの取得
TextTranslation.save_text_after(text_after_list, file_name)  # 翻訳後テキストをファイルに保存
Fn.time_log("翻訳")


# デバック用
# text_after_list = Debug.text_after_list  # 翻訳後テキストリスト

# 翻訳画像作成機能
overlay_translation_image = TranslationImage.get_overlay_translation_image(
    ss_file_path, text_after_list, text_region_list
)  # 翻訳後画像作成

overlay_translation_image_path = TranslationImage.save_overlay_translation_image(
    overlay_translation_image, file_name
)  # 翻訳後画像保存

Fn.time_log("画像作成")
