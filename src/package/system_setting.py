import os  # ディレクトリ関連


class SystemSetting:
    """ユーザーが変更不可能の設定クラス"""

    debug = True  # デバッグモード

    # 画像ファイル形式
    image_file_extension = ".png"

    package_path = os.path.dirname(__file__) + "/"  # パッケージディレクトリパス

    history_directory_path = package_path + "../history/"  # 履歴ディレクトリパス

    # 翻訳前画像保存先設定
    image_before_directory_path = history_directory_path + "image_before/"  # ディレクトリパス

    # 翻訳後画像保存先設定
    image_after_directory_path = history_directory_path + "image_after/"  # ディレクトリパス

    # 翻訳前テキスト保存先設定
    text_before_directory_path = history_directory_path + "text_before/"  # ディレクトリパス

    # 翻訳後テキスト保存先設定
    text_after_directory_path = history_directory_path + "text_after/"  # ディレクトリパス

    # 設定ファイル保存先設定
    setting_file_name = "setting.json"  # ファイル名
    setting_directory_path = package_path + "../"  # ディレクトリパス
    setting_file_path = setting_directory_path + setting_file_name  # 設定ファイルパス

    # 静的ファイル保存先設定
    static_path = package_path + "../../static/"

    # 使用するフォントファイルのパス MS明朝
    font_file_path = static_path + "msmincho.ttc"

    # アプリケーションの名前
    app_name = "ヤクミャクコンジャック"

    # 言語情報一覧リスト{日本語表記、英語表記、言語コード(ISO 639-1)}
    language_list = [
        {"ja_text": "アラビア語", "en_text": "Arabic", "code": "ar"},
        {"ja_text": "中国語", "en_text": "Chinese", "code": "zh"},
        {"ja_text": "英語", "en_text": "English", "code": "en"},
        {"ja_text": "フランス語", "en_text": "French", "code": "fr"},
        {"ja_text": "ドイツ語", "en_text": "German", "code": "de"},
        {"ja_text": "イタリア語", "en_text": "Italian", "code": "it"},
        {"ja_text": "日本語", "en_text": "Japanese", "code": "ja"},
        {"ja_text": "韓国語", "en_text": "Korean", "code": "ko"},
        {"ja_text": "ポルトガル語", "en_text": "Portuguese", "code": "pt"},
        {"ja_text": "ロシア語", "en_text": "Russian", "code": "ru"},
        {"ja_text": "スペイン語", "en_text": "Spanish", "code": "es"},
    ]

    # EasyOCR用の言語コード(ISO 639-2)のリスト((ISO 639-1):(ISO 639-2))
    EasyOCR_language_code = {"zh": "ch_sim"}
