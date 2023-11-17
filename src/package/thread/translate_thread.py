import os  # ディレクトリ関連

from package.system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス
from package.translation.translation import Translation  # 翻訳機能関連のクラス

from package.error_log import ErrorLog  # エラーログに関するクラス

from package.global_status import GlobalStatus  # グローバル変数保存用のクラス


class TranslateThread:
    """翻訳処理を行うスレッドクラス"""

    @staticmethod  # スタティックメソッドの定義
    # @ErrorLog.parameter_decorator(None)  # エラーログを取得するデコレータ
    @ErrorLog.decorator  # エラーログを取得するデコレータ
    def run(window):
        """翻訳処理
        Args:
            window(sg.Window): Windowオブジェクト
        """

        # ウィンドウオブジェクトの保存
        window = GlobalStatus.win_instance.window

        # 翻訳処理
        # file_name = Translation.save_history()

        # ! デバッグ
        try:
            # 翻訳処理
            file_name = Translation.save_history()
        except:
            import shutil  # ファイルのコピー

            source_dir_path = SystemSetting.image_before_directory_path  # 翻訳前履歴画像フォルダパス
            target_dir_path = SystemSetting.error_log_directory_path  # エラーログのディレクトリパス

            shutil.copytree(source_dir_path, target_dir_path, dirs_exist_ok=True)  # エラーが発生した画像の保存
            print("警告：エラーが発生した画像を保存しました")
            raise  # エラーを発生させる

        # ウィンドウが開いているなら
        if not (window.was_closed()):
            key = "-translate_thread_end-"
            value = file_name
            # スレッドから、翻訳イベントを送信
            window.write_event_value(key, value)
        # ウィンドウが閉じてあるなら
        else:
            for dir_path in [
                SystemSetting.image_before_directory_path,  # 翻訳前履歴画像フォルダパス
                SystemSetting.image_after_directory_path,  # 翻訳後履歴画像フォルダパス
            ]:
                # ファイルパス
                file_path = os.path.join(dir_path, file_name)
                # ファイルが存在するかチェック
                if os.path.exists(file_path):
                    # ファイルを削除
                    os.remove(file_path)
