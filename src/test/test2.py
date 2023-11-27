# 言語情報一覧リスト{日本語表記、英語表記、言語コード(ISO 639-1),フォントパス}
language_list = [
    {"ja_text": "アラビア語", "en_text": "Arabic", "code": "ar", "font_path": "font_Segoe_path"},
    {"ja_text": "中国語", "en_text": "Chinese", "code": "zh-CN", "font_path": "font_MicrosoftYaHei_path"},
    {"ja_text": "英語", "en_text": "English", "code": "en", "font_path": "font_Segoe_path"},
    {"ja_text": "フランス語", "en_text": "French", "code": "fr", "font_path": "font_Segoe_path"},
    {"ja_text": "ドイツ語", "en_text": "German", "code": "de", "font_path": "font_Segoe_path"},
    {"ja_text": "イタリア語", "en_text": "Italian", "code": "it", "font_path": "font_Segoe_path"},
    {"ja_text": "日本語", "en_text": "Japanese", "code": "ja", "font_path": "font_YuGothic_path"},
    {"ja_text": "韓国語", "en_text": "Korean", "code": "ko", "font_path": "font_MalgunGothic_path"},
    {"ja_text": "ポルトガル語", "en_text": "Portuguese", "code": "pt", "font_path": "font_Segoe_path"},
    {"ja_text": "ロシア語", "en_text": "Russian", "code": "ru", "font_path": "font_Segoe_path"},
    {"ja_text": "スペイン語", "en_text": "Spanish", "code": "es", "font_path": "font_Segoe_path"},
]

# EasyOCR用言語情報一覧リストの作成
# EasyOCR用言語情報一覧リスト（一部箇所でISO 639-2を使用）
easy_ocr_language_list = []
# EasyOCR用の言語コード(ISO 639-2)のリスト((ISO 639-1):(ISO 639-2))
easy_ocr_update_language_code = {"zh-CN": "ch_sim"}
# 言語情報で走査
for language_info in language_list:
    # 言語コードの取得
    language_code = language_info["code"]
    # 言語コードがEasyOCR用言語コードのリストに存在するなら
    if language_code in easy_ocr_update_language_code:
        # EasyOCR用言語コードに置き換える
        language_info["code"] = easy_ocr_update_language_code[language_code]
    # EasyOCR用言語情報一覧リストに追加する
    easy_ocr_language_list.append(language_info)
