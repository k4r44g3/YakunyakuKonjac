class UserSetting:
    """ユーザーが変更可能の設定クラス"""

    # スクリーンショット撮影範囲
    ss_top_left_x = 0  # SS範囲の左上x座標
    ss_top_left_y = 0  # SS範囲の左上y座標
    ss_bottom_right_x = 1280  # SS範囲の右下x座標
    ss_bottom_right_y = 720  # SS範囲の右下y座標

    ss_width = abs(ss_bottom_right_x - ss_top_left_x)  # SS範囲の横幅
    ss_height = abs(ss_bottom_right_y - ss_top_left_y)  # SS範囲の縦幅

    # スクリーンショット撮影範囲(left,top,width,height)
    ss_region = (ss_top_left_x, ss_top_left_y, ss_width, ss_height)

    ocr_soft = "Amazon Textract" # OCRソフト

    translation_soft = "Amazon Translate" # 翻訳ソフト

    source_language_code = "en" # 翻訳元言語

    target_language_code = "ja" # 翻訳先言語
    