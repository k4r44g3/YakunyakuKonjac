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

    screenshot = pyautogui.screenshot(region=ss_region)  # スクショ撮影

    return screenshot  # スクショ画像


def save_screenshot(screenshot, filename):
    """スクリーンショットの保存
    Args:
        screenshot(Image): スクショ画像
        filename(src): ファイル名(現在日時)
    Returns:
        ss_filepath(str): スクショ画像のファイルパス
    """
    filepath = SystemSetting.image_before_filepath  # 翻訳前画像パス
    file_extension = SystemSetting.image_file_extension  # 拡張子
    screenshot.save(filepath + filename + file_extension)  # スクショ画像保存

    ss_filepath = filepath + filename + file_extension  # ファイルパス(絶対参照)
    return ss_filepath


def get_text_data_dict(ss_filepath):
    """画像からテキスト情報を取得
    Args:
        textract(Textract): Textractサービスクライアント
        ss_filepath(src): スクショ画像のファイルパス
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

        image_in = Image.open(ss_filepath)  # 入力画像のファイルを読み込む
        w, h = image_in.size  # 画像サイズを取得

        with open(ss_filepath, "rb") as file:  # 画像ファイルを開く
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


def save_text_before(text_before_list, filename):
    """翻訳前テキストの保存
    Args:
        text_before_list(list[text_before:str]): 翻訳前テキストリスト
        filename(src): ファイル名(現在日時)
    """
    filepath = SystemSetting.text_before_filepath  # 翻訳前テキストパス
    file_extension = ".txt"  # 拡張子
    text_filepath = filepath + filename + file_extension  # ファイルパス(絶対参照)

    file = open(text_filepath, "w",encoding="utf-8")  # 新規書き込みでテキストファイルを開く
    # file = open(text_filepath, "w",)  # 新規書き込みでテキストファイルを開く
    for text_before in text_before_list:  # 翻訳前テキストで走査
        print(text_before)
        file.write(text_before + "\n")  # ファイルに書き込む
    file.close()  # ファイルを閉じる


Fn.time_log("システム開始")
filename = Fn.get_filename()  # ファイル名(現在日時)
screenshot = get_screenshot()  # スクショ撮影
ss_filepath = save_screenshot(screenshot, filename)  # スクショ保存
Fn.time_log("スクショ撮影")


ss_filepath = os.path.dirname(__file__) + "/test/image_before.jpg"  # テスト用


text_data_dict = get_text_data_dict(ss_filepath)  # 画像からテキスト情報を取得
text_before_list = text_data_dict["text_list"]  # 翻訳前テキストリストの取得
region_list = text_data_dict["region_list"]  # テキスト範囲のリストの取得

save_text_before(text_before_list, filename)  # 翻訳前テキスト保存
Fn.time_log("テキスト読み取り")

# translate = boto3.client("translate")  # Translate サービスクライアントを作成
