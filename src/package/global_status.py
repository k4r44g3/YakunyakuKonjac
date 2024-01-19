from typing import Any, Dict, List, Optional, Tuple, Union  # 型ヒント


class GlobalStatus:
    """グローバル変数保存用クラス"""

    # 現在開いているウィンドウクラスのインスタンス
    win_instance = None  # win_instance: Optional['BaseWin']

    is_main_thread_running: bool = True  # メインスレッドが実行中かどうか
    is_sub_thread_error: bool = False  # サブスレッドでエラーが発生したかどうか
    sub_thread_error_message: str = ""  # サブスレッドでエラー発生時の表示エラーメッセージ
