import os
import easyocr
from deep_translator import GoogleTranslator


ocr_lang_list = ['ja', 'en'] # 抽出する言語のリスト
reader = easyocr.Reader(lang_list=ocr_lang_list,gpu=True)  # 画像内のテキストを抽出する

# 'test.png' からテキストを抽出
image_path = os.path.dirname(__file__) + "/image_before.png"
result = reader.readtext(image_path)

print(type(result))
# for text in result:
#     print(text)
# OCRで取得したテキストを保持するリスト
# ocr_texts = [text[1] for text in result]

# テキストを翻訳する（'ja' に翻訳）
# translated_texts = [GoogleTranslator(source='auto', target='ja').translate(text) for text in ocr_texts]

# print(ocr_texts)
# EasyOCR参照URL
# https://camp.trainocate.co.jp/magazine/about-easyocr/

# translator参照URL
# https://qiita.com/FKjujcc/items/c7e206bec306da891573
