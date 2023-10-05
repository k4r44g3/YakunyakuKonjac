import os  # ディレクトリ管理

from fn import Fn  # 自作関数クラス
from screenshot_capture import ScreenshotCapture  # スクリーンショット撮影機能関連のクラス
from character_recognition import CharacterRecognition  # 文字認識機能関連のクラス
from translation import Translation  # 翻訳機能関連のクラス


Fn.time_log("システム開始")

# 保存ファイル名(現在日時)の取得
file_name = Fn.get_now_file_name()

# スクショ撮影機能
screenshot_image = ScreenshotCapture.get_screenshot()  # スクショ撮影
ss_file_path = ScreenshotCapture.save_screenshot(screenshot_image, file_name)  # スクショ保存
Fn.time_log("スクショ撮影")

# デバック用
ss_file_path = os.path.dirname(__file__) + "/test/image_before.jpg"  # スクショ画像をテスト用に変更

# 文字認識機能
text_data_dict = CharacterRecognition.get_text_data_dict(ss_file_path)  # 画像からテキスト情報を取得
text_before_list = text_data_dict["text_list"]  # 翻訳前テキストリストの取得
region_list = text_data_dict["region_list"]  # テキスト範囲のリストの取得
CharacterRecognition.save_text_before(text_before_list, file_name)  # 翻訳前テキストをファイルに保存
Fn.time_log("文字取得")

# 翻訳機能
text_after_list = Translation.get_text_after_list(text_before_list)  # 翻訳後テキストリストの取得
Translation.save_text_after(text_after_list, file_name)  # 翻訳後テキストをファイルに保存
Fn.time_log("翻訳")
