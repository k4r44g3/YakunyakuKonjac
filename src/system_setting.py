import os


class SystemSetting:
    """ユーザーが変更不可能の設定クラス"""

    debug = True  # デバッグモード

    # 翻訳前画像保存先設定
    image_before_filename = "image_before.png"  # ファイル名
    image_before_filepath = os.path.dirname(__file__) + "/history/image_before/"  # ファイルパス
    image_before_filepath += image_before_filename  # ファイルパス更新

    # オプションファイル保存先設定
    option_filename = "option.json"  # ファイル名
    option_filepath = os.path.dirname(__file__) + "/"  # ファイルパス このファイルのディレクトリの絶対パス
    option_filepath += option_filename  # オプションファイルパス更新

    # アプリケーションの名前
    app_name = "ヤクミャクコンジャック"
