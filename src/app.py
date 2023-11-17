import os  # オペレーティングシステム関連

# 初期化
error_log = None

# エラーログのインポート
try:
    from package.error_log import ErrorLog  # エラーログに関するクラス
    # エラーログ作成
    error_log = ErrorLog.create_error_log()
# インポートに失敗したなら
except Exception as e:
    message = [
        "申し訳ありません、エラーが発生しました。",
        f"エラーメッセージ: {str(e)}",
        "エラーログファイルの作成に失敗しました。",
        "管理者に問題を報告していただけると幸いです。",
    ]
    print("\n".join(message))
    exit() # 処理を終了する


# その他の自作クラスのインポート
try:

    from package.fn import Fn  # 自作関数クラス

    from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス
    from package.system_setting import SystemSetting  # ユーザーが変更不可の設定クラス

    from package.window.translation_win import TranslationWin  # 翻訳画面ウィンドウクラス
    from package.window.display_setting_win import DisplaySettingWin  # 表示設定画面ウィンドウクラス

    # 環境設定画面ウィンドウクラス
    from package.window.environment_setting_win import EnvironmentSettingWin
    from package.window.key_setting_win import KeySettingWin  # キー設定画面ウィンドウクラス
    from package.window.language_setting_win import LanguageSettingWin  # 言語設定画面ウィンドウクラス
    from package.window.save_setting_win import SaveSettingWin  # 保存設定画面ウィンドウクラス
    from package.window.shooting_setting_win import ShootingSettingWin  # 撮影設定画面ウィンドウクラス
    from package.window.theme_setting_win import ThemeSettingWin  # テーマ設定画面ウィンドウクラス
    from package.window.user_info_win import UserInfoWin  # 利用者情報画面ウィンドウクラス

except Exception as e:
    # エラーログの出力処理
    ErrorLog.output_error_log(error_log, e)

class App:
    """アプリケーションのメインクラス"""

    def __init__(self):
        """コンストラクタ"""
        # メイン処理
        self.run()

    @ErrorLog.decorator  # エラーログの出力
    def run(self):
        """メインの処理"""
        # 必要クラスのインポート

        # ウィンドウクラスのマッピング辞書
        WIN_CLASS_DICT = {
            "TranslationWin": TranslationWin,  # 翻訳画面ウィンドウクラス
            "DisplaySettingWin": DisplaySettingWin,  # 表示設定画面ウィンドウクラス
            "EnvironmentSettingWin": EnvironmentSettingWin,  # 環境設定画面ウィンドウクラス
            "KeySettingWin": KeySettingWin,  # キー設定画面ウィンドウクラス
            "LanguageSettingWin": LanguageSettingWin,  # 言語設定画面ウィンドウクラス
            "SaveSettingWin": SaveSettingWin,  # 保存設定画面ウィンドウクラス
            "ShootingSettingWin": ShootingSettingWin,  # 撮影設定画面ウィンドウクラス
            "ThemeSettingWin": ThemeSettingWin,  # テーマ設定画面ウィンドウクラス
            "UserInfoWin": UserInfoWin,  # 利用者情報画面ウィンドウクラス
        }

        Fn.time_log("システム開始")

        # AWSの設定ファイルのパスの設定
        os.environ["AWS_CONFIG_FILE"] = SystemSetting.aws_config_file_path
        # AWSの認証情報ファイルのパスの設定
        os.environ["AWS_SHARED_CREDENTIALS_FILE"] = SystemSetting.aws_credentials_file_path

        # ユーザ設定のインスタンス化
        user_setting = UserSetting()

        # # AWSサービスにアクセス可能か確認する処理
        # aws_service_exception = user_setting.check_access_aws_service()

        # # AWSサービスにアクセス時に発生した例外オブジェクトが存在するなら
        # if aws_service_exception is not None:
        #     print("AWSアクセスエラー")
        #     print(aws_service_exception)
        #     return
        # else:
        #     print("正常")

        # 翻訳前、後画像の両方が存在しない履歴ファイルを削除
        Fn.delete_unique_history_file()

        # メインウィンドウの処理
        transition_target_win = "TranslationWin"  # 遷移先ウィンドウ名
        win_class = WIN_CLASS_DICT[transition_target_win]  # 遷移先ウィンドウクラスの取得
        win_instance = win_class()  # ウィンドウ作成、ウィンドウクラスのインスタンスの保持
        transition_target_win = win_instance.get_transition_target_win()  # 遷移先ウィンドウ名取得

        # 遷移先ウィンドウが存在する間、繰り返す
        while transition_target_win is not None:
            win_class = WIN_CLASS_DICT[transition_target_win]  # 遷移先ウィンドウクラス
            win_instance = win_class()  # ウィンドウ作成、ウィンドウクラスのインスタンスの保持
            transition_target_win = win_instance.get_transition_target_win()  # 遷移先ウィンドウ名取得
        Fn.time_log("システム終了")

if __name__ == "__main__":
    app_instance = App()  # メイン処理
