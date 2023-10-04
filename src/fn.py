import datetime  # 現在時刻

from system_setting import SystemSetting  # ユーザーが変更不可の設定クラス


class Fn:
    """自作関数クラス
    全体に適応される"""

    def get_filename():
        """ファイル名用現在時刻の取得
        Returns:
            str : 現在時刻("yyyymmdd_hhmmss_fff")
        """
        now = datetime.datetime.now()  # 現在の時刻を取得
        return now.strftime("%Y%m%d_%H%M%S_%f")[:-3]  # 時刻の表示（ミリ秒三桁まで）

    def log(*text):
        """ログの表示
            デバッグモードでのみ動作する
        Args:
            text (*str): 出力文字
        """
        if SystemSetting.debug:  # デバッグモードなら
            print(text)

    def time_log(*text):
        """ログと現在時刻の表示
            デバッグモードでのみ動作する
        Args:
            text (*str): 出力文字
        """
        if SystemSetting.debug:  # デバッグモードなら
            now = datetime.datetime.now()  # 現在の時刻を取得
            print(text, now.strftime("%H:%M:%S.%f")[:-3])  # 時刻の表示（ミリ秒三桁まで）

    def isfloat(value):
        """値が少数かどうかを返す

        Args:
            value (str): 確認する値

        Returns:
            bool: 値が少数ならTrue
        """
        try:
            # 少数に変換出来なかったら中断
            float(value)  # 少数に変換
            return True  # 少数に変換できたならTrueを返す
        except ValueError:  # 少数に変換できなかったなら
            return False  # falseを返す

    def isint(value):
        """値が整数かどうかを返す

        Args:
            value (str): 確認する値

        Returns:
            bool: 値が整数ならTrue
        """

        try:
            # 整数に変換出来なかったら中断
            int(value)  # 整数に変換
            return True  # 整数に変換できたならTrueを返す
        except ValueError:  # 整数に変換できなかったなら
            return False  # falseを返す
