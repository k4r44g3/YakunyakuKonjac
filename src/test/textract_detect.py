"""
Chapter6 textract
    画像内の文字列を検出します
"""

# 各種ライブラリのインポート
import boto3
import json
import sys
import os
from PIL import Image


image_path = os.path.dirname(__file__) + "/novel.jpg"  # 画像ファイルパス

textract = boto3.client("textract", "us-east-1")  # Textractサービスクライアントを作成

with open(image_path, "rb") as file:  # 画像ファイルを開く
    result = textract.detect_document_text(Document={"Bytes": file.read()})  # 文字列を検出

image_in = Image.open(image_path)  # 入力画像のファイルを読み込む
w, h = image_in.size  # 画像サイズを取得
text_data_list = []  # テキスト情報のリスト

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

        text_data_list.append({"text": text, "region": region})  # テキスト情報のリストの作成

print(text_data_list)

# image_in = Image.open(image_path)  # 入力画像のファイルを読み込む
# w, h = image_in.size  # 画像サイズを取得
# image_out = Image.new('RGB', (w, h), (200, 200, 200))  # 出力画像を作成
# for block in result['Blocks']:  # 検出されたブロックを順番に処理
#     if block['BlockType'] == 'LINE':  # ブロックタイプが行かどうかを調べる
#         box = block['Geometry']['BoundingBox']  # バウンディングボックスを取得
#         # 文字列の左、上、右、下の座標を計算
#         left = int(box['Left']*w)
#         top = int(box['Top']*h)
#         right = left+int(box['Width']*w)
#         bottom = top+int(box['Height']*h)
#         image_out.paste(
#             image_in.crop((left, top, right, bottom)), (left, top))  # 入力画像から出力画像に文字列の部分を貼り付け
#         print(block['Text']),  # 文字列の内容を表示
# image_out.save('detect_'+sys.argv[1])  # 出力画像をファイルに保存
# image_out.show()  # 出力画像を表示

"""
画像内の文字列を検出する
    書式
        detect_document_text(
            Document={'Bytes': 画像データ})
"""
