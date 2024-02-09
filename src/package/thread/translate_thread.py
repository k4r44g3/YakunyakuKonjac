import os  # ディレクトリ関連

from package.error_log import ErrorLog  # エラーログに関するクラス
from package.fn import Fn  # 自作関数クラス
from package.global_status import GlobalStatus  # グローバル変数保存用のクラス
from package.system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス
from package.translation.translation import Translation  # 翻訳機能関連のクラス


class TranslateThread:
    """翻訳処理を行うスレッドクラス"""

    @staticmethod  # スタティックメソッドの定義
    @ErrorLog.decorator  # エラーログを取得するデコレータ
    def run():
        """翻訳処理"""

        # ウィンドウオブジェクトの取得
        window = GlobalStatus.win_instance.window

        Fn.time_log("翻訳開始")

        # 翻訳前, 結果画像を一時保存する
        save_history_result = Translation.save_tmp_history()

        # 保存ファイル名の取得
        file_name = save_history_result["file_name"]

        # 保存処理でエラーが発生していないかつ、ウィンドウが開いているなら
        if not save_history_result["is_error"] and not (window.was_closed()):
            Fn.time_log("翻訳終了")
            key = "-translate_thread_end-"
            value = file_name
            # スレッドから、翻訳イベントを送信
            window.write_event_value(key, value)

        # 保存処理でエラーが発生したもしくは、ウィンドウが閉じてあるなら
        else:
            # 一時保存画像を削除する
            directory_path = SystemSetting.image_tmp_directory_path  # 翻訳中一時保存画像のディレクトリパス
            # 翻訳前の一時保存画像のパス
            ss_file_path = os.path.join(directory_path, f"before_{file_name}")
            Fn.delete_file(ss_file_path)  # 翻訳前の一時保存画像ファイルの削除
            # 翻訳後の一時保存画像のパス
            overlay_translation_image_path = os.path.join(directory_path, f"after_{file_name}")
            Fn.delete_file(overlay_translation_image_path)  # 翻訳後の一時保存画像ファイルの削除

            # 保存処理でエラーが発生したなら
            if save_history_result["is_error"]:
                # リクエスト過多エラーなら
                if type(save_history_result["exception"]).__name__ == "TooManyRequests":
                    message = [
                        "翻訳ソフト'GoogleTranslator'でエラーが発生しました。",
                        "サーバーへのリクエストが多すぎます。",
                        "しばらく時間を置いてから再度試してみてください",
                        "このエラーが再発する場合は環境設定画面から翻訳ソフトを変更してみてください。",
                        "エラーメッセージ:",
                        str(save_history_result["exception"]),
                    ]

                # リクエスト過多エラー以外なら
                else:
                    message = [
                        "申し訳ありません、翻訳処理中に不明なエラーが発生しました。",
                        "このエラーが再発する場合は環境設定画面からソフトを変更してみてください。",
                        "エラーログファイルが作成されました。",
                        "管理者にこのファイルを提供していただけると幸いです。",
                        "エラーメッセージ:",
                        str(save_history_result["exception"]),
                    ]

                # ログの表示
                print("\n".join(message))

                # 現在開いているウィンドウクラスのインスタンスでウィンドウオブジェクトが作成されているかどうか
                if hasattr(GlobalStatus.win_instance, "window"):
                    # ウィンドウオブジェクトの取得
                    window = GlobalStatus.win_instance.window
                    # ウィンドウが閉じられていないなら
                    if not window.was_closed():
                        # スレッドから、キーイベントを送信
                        window.write_event_value(key="-thread_popup_event-", value=message)
