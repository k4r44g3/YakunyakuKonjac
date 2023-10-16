import datetime  # 現在時刻
import os  # ディレクトリ関連

import boto3  # AWSのAIサービス
import easyocr  # OCRライブラリ

from PIL import Image  # 画像処理


def get_now_file_name():
    """ファイル名用現在時刻の取得
    Returns:
        now_file_name(str) : 現在時刻("yyyymmdd_hhmmss_fff")
    """
    now = datetime.datetime.now()  # 現在の時刻を取得
    now_file_name = now.strftime("%Y%m%d_%H%M%S_%f")[:-3]  # 時刻の表示（ミリ秒三桁まで）
    return now_file_name  # ファイル名用現在時刻


def get_text_data_dict(ss_file_path):
    """画像からテキスト情報を取得
    Args:
        user_setting(UserSetting): ユーザーが変更可能の設定
        ss_file_path(src): スクショ画像のファイルパス
    Returns:
        text_data_dict(List[text_list,text_region_list]): テキスト情報リスト
            - text_list(List[text(str)]) : テキスト内容のリスト
            - text_region_list(List[region]): テキスト範囲のリスト
                - text_region(dict{Left:int, Top:int, Width:int, Height:int}): テキスト範囲
    """
    ocr_soft = "Amazon Textract"  # OCRソフト
    ocr_soft = "EasyOCR"  # OCRソフト

    # OCRソフトによって分岐
    if ocr_soft == "Amazon Textract":  # OCRソフトがAmazonなら
        text_data_list = amazon_textract_ocr(ss_file_path)
    if ocr_soft == "EasyOCR":  # OCRソフトがAmazonなら
        text_data_list = easy_ocr(ss_file_path)

    return text_data_list  # テキスト情報のリスト


def amazon_textract_ocr(ss_file_path):
    """Amazon Textractを使用して画像からテキスト情報を取得
    Args:
        ss_file_path(src): スクショ画像のファイルパス

    Returns:
        text_data_dict(List[text_list,text_region_list]): テキスト情報リスト
            - text_list(List[text(str)]) : テキスト内容のリスト
            - text_region_list(List[region]): テキスト範囲のリスト
                - text_region(dict{Left:int, Top:int, Width:int, Height:int}): テキスト範囲
    """
    textract = boto3.client("textract", "us-east-1")  # Textractサービスクライアントを作成

    text_list = []  # テキスト内容のリスト
    text_region_list = []  # テキスト範囲のリスト

    image_in = Image.open(ss_file_path)  # 入力画像のファイルを読み込む
    w, h = image_in.size  # 画像サイズを取得

    with open(ss_file_path, "rb") as file:  # 画像ファイルを開く
        result = textract.detect_document_text(Document={"Bytes": file.read()})  # 文字列を検出

    for block in result["Blocks"]:  # 検出されたブロックを順番に処理
        if block["BlockType"] == "LINE":  # ブロックタイプが行かどうかを調べる
            text = block["Text"]  # テキスト内容取得
            box = block["Geometry"]["BoundingBox"]  # バウンディングボックスを取得
            # テキスト範囲の取得
            text_region = {
                "left": int(box["Left"] * w),  # テキスト範囲の左側x座標
                "top": int(box["Top"] * h),  # テキスト範囲の上側y座標
                "width": int(box["Width"] * w),  # テキスト範囲の横幅
                "height": int(box["Height"] * h),  # テキスト範囲の縦幅
            }
            text_list.append(text)  # テキスト内容のリスト
            text_region_list.append(text_region)  # テキスト範囲のリスト
    text_data_list = {
        "text_list": text_list,
        "text_region_list": text_region_list,
    }  # テキスト情報のリスト作成
    return text_data_list  # テキスト情報のリスト


def easy_ocr(ss_file_path):
    """EasyOCRを使用して画像からテキスト情報を取得
    Args:
        ss_file_path(src): スクショ画像のファイルパス

    Returns:
        text_data_dict(List[text_list,text_region_list]): テキスト情報リスト
            - text_list(List[text(str)]) : テキスト内容のリスト
            - text_region_list(List[region]): テキスト範囲のリスト
                - text_region(dict{Left:int, Top:int, Width:int, Height:int}): テキスト範囲
    """
    ocr_lang_list = ["ja", "en"]  # 抽出する言語のリスト

    text_list = []  # テキスト内容のリスト
    text_region_list = []  # テキスト範囲のリスト

    #! GPUが使用できないため警告メッセージが表示される
    reader = easyocr.Reader(lang_list=ocr_lang_list)  # OCRの作成

    result = reader.readtext(ss_file_path)  # # 画像内のテキストを抽出する

    # 段落ごとに走査
    for text_box in result:
        # テキスト範囲の取得
        text_region = {
            "left": int(text_box[0][0][0]),  # テキスト範囲の左側x座標
            "top": int(text_box[0][0][1]),  # テキスト範囲の上側y座標
            "width": int(text_box[0][2][0]) - int(text_box[0][0][0]),  # テキスト範囲の横幅
            "height": int(text_box[0][2][1]) - int(text_box[0][0][1]),  # テキスト範囲の縦幅
        }
        text = text_box[1]  # テキスト内容の取得
        # confidence = text_box[2] # 信頼度の取得

        text_list.append(text)  # テキスト内容のリスト
        text_region_list.append(text_region)  # テキスト範囲のリスト

    # テキスト情報のリスト作成
    text_data_list = {
        "text_list": text_list,
        "text_region_list": text_region_list,
    }

    return text_data_list  # テキスト情報のリスト


image_path = os.path.dirname(__file__) + "/image_before.png"

print(amazon_textract_ocr(image_path))
print(easy_ocr(image_path))
