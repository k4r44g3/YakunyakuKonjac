class UserSetting:
    """ユーザーが変更可能の設定クラス"""

    # スクリーンショット撮影範囲
    ss_left_x = 0  # SS範囲の左側x座標
    ss_top_y = 0  # SS範囲の上側y座標
    ss_right_x = 1280  # SS範囲の右側x座標
    ss_bottom_y = 720  # SS範囲の下側y座標

    ss_width = abs(ss_right_x - ss_left_x)  # SS範囲の横幅
    ss_height = abs(ss_bottom_y - ss_top_y)  # SS範囲の縦幅

    # スクリーンショット撮影範囲(left,top,width,height)
    ss_region = (ss_left_x, ss_top_y, ss_width, ss_height)

    ocr_soft = "Amazon Textract"  # OCRソフト

    translation_soft = "Amazon Translate"  # 翻訳ソフト

    source_language_code = "en"  # 翻訳元言語

    target_language_code = "ja"  # 翻訳先言語

    # ウィンドウ位置・サイズ
    window_left_x = 0
    window_top_y = 0
    window_width = 300
    window_height = 200

    # 翻訳間隔
    translation_interval_sec = 20
