import os


class SystemSetting:
    """ユーザーが変更不可能の設定クラス"""

    debug = True  # デバッグモード

    # 画像ファイル形式
    image_file_extension = ".png"

    # 翻訳前画像保存先設定
    image_before_filepath = os.path.dirname(__file__) + "/history/image_before/"  # ファイルパス

    # 翻訳後画像保存先設定
    image_after_filepath = os.path.dirname(__file__) + "/history/image_after/"  # ファイルパス

    # 翻訳前テキスト保存先設定
    text_before_filepath = os.path.dirname(__file__) + "/history/text_before/"  # ファイルパス

    # 翻訳後テキスト保存先設定
    text_after_filepath = os.path.dirname(__file__) + "/history/text_after/"  # ファイルパス


    # オプションファイル保存先設定
    option_filename = "option.json"  # ファイル名
    option_filepath = os.path.dirname(__file__) + "/"  # ファイルパス このファイルのディレクトリの絶対パス
    option_filepath += option_filename  # オプションファイルパス更新

    # アプリケーションの名前
    app_name = "ヤクミャクコンジャック"
