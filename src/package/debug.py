import os  # ディレクトリ管理


class Debug:
    """デバッグ用クラス"""

    # デバッグ用ディレクトリパス
    debug_directory_path = os.path.dirname(__file__) + "/../debug_history/"

    # 翻訳前画像パス
    ss_file_path = debug_directory_path + "/image_before.jpg"

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

    # テキスト範囲のリスト
    text_region_list = [
        {"left": 1118, "top": 290, "width": 1201, "height": 155},
        {"left": 392, "top": 663, "width": 2358, "height": 126},
        {"left": 394, "top": 823, "width": 2430, "height": 127},
        {"left": 393, "top": 982, "width": 2456, "height": 129},
        {"left": 393, "top": 1143, "width": 2507, "height": 131},
        {"left": 394, "top": 1302, "width": 2434, "height": 131},
        {"left": 394, "top": 1461, "width": 2645, "height": 131},
        {"left": 396, "top": 1623, "width": 2080, "height": 127},
        {"left": 1359, "top": 1999, "width": 1505, "height": 140},
        {"left": 1682, "top": 2204, "width": 1040, "height": 138},
    ]

    # 翻訳後テキストリスト
    text_after_list = [
        "マーリーの幽霊",
        "そもそも、マーリーは死んでいた。誰もいない",
        "それについては疑う余地はありません。彼の記録だ",
        "埋葬は牧師と事務員によって署名されました",
        "葬儀屋と主任会葬者スクルージ",
        "サインをして、スクルージの名前が好評だったんです",
        "「彼が選んだものは何でも変えなさい。",
        "オールド・マーリーはまるで釘のように死んでいた。",
        "「クリスマス・キャロル」",
        "チャールズ・ディケンズ",
    ]

    # 翻訳後画像パス
    overlay_translation_image_path = debug_directory_path + "/image_after.jpg"

    # リサイズした翻訳後画像の保存先パス
    resize_image_after_path = debug_directory_path + "/resize_image_after.png"

    # リサイズした翻訳前画像の保存先パス
    resize_image_before_path = debug_directory_path + "/resize_image_before.png"