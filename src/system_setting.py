import os


class SystemSetting:
    """ユーザーが変更不可能の設定クラス"""

    debug = True  # デバッグモード

    # 画像ファイル形式
    image_file_extension = ".png"

    # 翻訳前画像保存先設定
    image_before_directory_path = os.path.dirname(__file__) + "/history/image_before/"  # ディレクトリパス

    # 翻訳後画像保存先設定
    image_after_directory_path = os.path.dirname(__file__) + "/history/image_after/"  # ディレクトリパス

    # 翻訳前テキスト保存先設定
    text_before_directory_path = os.path.dirname(__file__) + "/history/text_before/"  # ディレクトリパス

    # 翻訳後テキスト保存先設定
    text_after_directory_path = os.path.dirname(__file__) + "/history/text_after/"  # ディレクトリパス

    # オプションファイル保存先設定
    option_file_name = "option.json"  # ファイル名
    option_directory_path = os.path.dirname(__file__) + "/"  # ディレクトリパス
    option_file_path = option_directory_path + option_file_name  # オプションファイルパス

    # アプリケーションの名前
    app_name = "ヤクミャクコンジャック"
