import os
import easyocr
from deep_translator import GoogleTranslator


# 翻訳前テキストリスト
text_before_list = [
    "MARLEY'S GHOST",
    "Marley was dead: to begin with. There is no",
    "doubt whatever about that. The register of his",
    "burial was signed by the clergyman, the clerk,",
    "the undertaker, and the chief mourner. Scrooge",
    "signed it: and Scrooge's name was good upon",
    "'Change, for anything he chose to put his hand to.",
    "Old Marley was as dead as a door-nail.",
    '" A CHRISTMAS CAROL"',
    "by Charles Dickens",
]


source_language_code = 'auto' # 翻訳前言語
target_language_code = 'ja' # 翻訳後言語

# 翻訳オブジェクト作成
google_translator = GoogleTranslator(source=source_language_code, target=target_language_code)

text_after_list = []  # 翻訳語テキストのリスト作成

for text_before in text_before_list:  # 翻訳前テキストで走査
    # 英語から日本語に翻訳
    result = google_translator.translate(text=text_before)
    text_after_list.append(result)  # 翻訳後テキストのリスト作成

# translate = boto3.client("translate")  # Translate サービスクライアントを作成
# text_after_list = []  # 翻訳語テキストのリスト作成

# for text_before in text_before_list:  # 翻訳前テキストで走査
#     # 英語から日本語に翻訳
#     result = translate.translate_text(
#         Text=text_before,  # 翻訳テキスト
#         SourceLanguageCode=source_language_code,  # 翻訳前言語
#         TargetLanguageCode=target_language_code,  # 翻訳後言語
#     )
#     text_after_list.append(result["TranslatedText"])  # 翻訳後テキストのリスト作成
