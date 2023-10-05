import pyautogui  # スクショ撮影
import boto3  # AWSのAIサービス

from PIL import Image  # 画像処理
import os  # ディレクトリ管理

from fn import Fn  # 自作関数クラス
from user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス


def get_screenshot():
    """スクリーンショットの撮影

    Returns:
        Image: スクショ画像
    """
    ss_region = UserSetting.ss_region  # SS撮影範囲

    screenshot_image = pyautogui.screenshot(region=ss_region)  # スクショ撮影

    return screenshot_image  # スクショ画像


def save_screenshot(screenshot_image, file_name):
    """スクリーンショットの保存
    Args:
        screenshot_image(Image): スクショ画像
        file_name(src): ファイル名(現在日時)
    Returns:
        ss_file_path(str): スクショ画像のファイルパス
    """
    directory_path = SystemSetting.image_before_directory_path  # 翻訳前画像のディレクトリパス
    file_extension = SystemSetting.image_file_extension  # 拡張子
    ss_file_path = directory_path + file_name + file_extension  # ファイルパス(絶対参照)

    screenshot_image.save(ss_file_path)  # スクショ画像保存

    return ss_file_path  # スクショファイルパス


def get_text_data_dict(ss_file_path):
    """画像からテキスト情報を取得
    Args:
        textract(Textract): Textractサービスクライアント
        ss_file_path(src): スクショ画像のファイルパス
    Returns:
        text_data_dict(List[text_list,region_list]): テキスト情報リスト
            - text_list(List[text(str)]) : テキスト内容のリスト
            - region_list(List[Left:int, Top:int, Width:int, Height:int]): テキスト範囲のリスト
    """
    ocr_soft = UserSetting.ocr_soft  # OCRソフト

    # OCRソフトによって分岐
    if ocr_soft == "Amazon Textract":  # OCRソフトがAmazonなら
        textract = boto3.client("textract", "us-east-1")  # Textractサービスクライアントを作成

        text_list = []  # テキスト内容のリスト
        region_list = []  # テキスト範囲のリスト

        image_in = Image.open(ss_file_path)  # 入力画像のファイルを読み込む
        w, h = image_in.size  # 画像サイズを取得

        with open(ss_file_path, "rb") as file:  # 画像ファイルを開く
            result = textract.detect_document_text(Document={"Bytes": file.read()})  # 文字列を検出

        for block in result["Blocks"]:  # 検出されたブロックを順番に処理
            if block["BlockType"] == "LINE":  # ブロックタイプが行かどうかを調べる
                box = block["Geometry"]["BoundingBox"]  # バウンディングボックスを取得

                # テキスト範囲の取得
                left = int(box["Left"] * w)  # テキスト範囲の左上x座標
                top = int(box["Top"] * h)  # テキスト範囲の左上y座標
                width = int(box["Width"] * w)  # テキスト範囲の横幅
                height = int(box["Height"] * h)  # テキスト範囲の縦幅

                text = block["Text"]  # テキスト内容取得
                region = [left, top, width, height]  # テキスト範囲の取得

                text_list.append(text)  # テキスト内容のリスト
                region_list.append(region)  # テキスト範囲のリスト

    text_data_list = {"text_list": text_list, "region_list": region_list}
    return text_data_list  # テキスト情報のリスト


def save_text_before(text_before_list, file_name):
    """翻訳前テキストをファイルに保存
    Args:
        text_before_list(list[text_before:str]): 翻訳前テキストリスト
        file_name(src): ファイル名(現在日時)
    """
    directory_path = SystemSetting.text_before_directory_path  # 翻訳前テキストのディレクトリパス
    file_extension = ".txt"  # 拡張子
    file_path = directory_path + file_name + file_extension  # ファイルパス(絶対参照)
    Fn.save_text_file(text_before_list, file_path)  # テキストファイルへの保存


def get_text_after_list(text_before_list):
    """翻訳後テキストの取得

    Args:
        text_before_list(List[text_before]) : 翻訳前テキストのリスト
            - text_before(str) : 翻訳前テキスト
    Returns:
        text_after_list(List[text_after]) : 翻訳後テキストのリスト
            - text_after(str) : 翻訳後テキスト
    """

    translation_soft = UserSetting.translation_soft  # 翻訳ソフト
    source_language_code = UserSetting.source_language_code  # 翻訳前言語
    target_language_code = UserSetting.target_language_code  # 翻訳後言語

    # OCRソフトによって分岐
    if translation_soft == "Amazon Translate":  # 翻訳ソフトがAmazonなら
        translate = boto3.client("translate")  # Translate サービスクライアントを作成
        text_after_list = []  # 翻訳語テキストのリスト作成

        for text_before in text_before_list:  # 翻訳前テキストで走査
            # 英語から日本語に翻訳
            result = translate.translate_text(
                Text=text_before,  # 翻訳テキスト
                SourceLanguageCode=source_language_code,  # 翻訳前言語
                TargetLanguageCode=target_language_code,  # 翻訳後言語
            )
            text_after_list.append(result["TranslatedText"])  # 翻訳後テキストのリスト作成
    return text_after_list  # 翻訳後テキストのリスト


def save_text_after(text_after_list, file_name):
    """翻訳後テキストをファイルに保存
    Args:
        text_after_list(list[text_after:str]): 翻訳後テキストリスト
        file_name(src): ファイル名(現在日時)
    """
    directory_path = SystemSetting.text_after_directory_path  # 翻訳後テキストのディレクトリパス
    file_extension = ".txt"  # 拡張子
    file_path = directory_path + file_name + file_extension  # ファイルパス(絶対参照)
    Fn.save_text_file(text_after_list, file_path)  # テキストファイルへの保存



Fn.time_log("システム開始")
file_name = Fn.get_now_file_name()  # ファイル名(現在日時)

screenshot_image = get_screenshot()  # スクショ撮影
ss_file_path = save_screenshot(screenshot_image, file_name)  # スクショ保存
Fn.time_log("スクショ撮影")


ss_file_path = os.path.dirname(__file__) + "/test/image_before.jpg"  # テスト用


text_data_dict = get_text_data_dict(ss_file_path)  # 画像からテキスト情報を取得
text_before_list = text_data_dict["text_list"]  # 翻訳前テキストリストの取得
region_list = text_data_dict["region_list"]  # テキスト範囲のリストの取得
save_text_before(text_before_list, file_name)  # 翻訳前テキストをファイルに保存

Fn.time_log("文字取得")

text_after_list = get_text_after_list(text_before_list)  # 翻訳後テキストリストの取得
save_text_after(text_after_list, file_name)  # 翻訳後テキストをファイルに保存

Fn.time_log("翻訳")
