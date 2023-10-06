import os


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

    # リサイズした翻訳後画像の保存先設定
    resize_after_directory_path = history_directory_path + "resize_image_after/"  # ディレクトリパス

    # リサイズした翻訳前画像の保存先設定
    resize_before_directory_path = history_directory_path + "resize_image_before/"  # ディレクトリパス

    # オプションファイル保存先設定
    option_file_name = "option.json"  # ファイル名
    option_directory_path = package_path + "../"  # ディレクトリパス
    option_file_path = option_directory_path + option_file_name  # オプションファイルパス

    # アプリケーションの名前
    app_name = "ヤクミャクコンジャック"
