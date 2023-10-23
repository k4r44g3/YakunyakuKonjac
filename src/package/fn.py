from datetime import datetime  # 日時
import os  # ディレクトリ関連

from package.system_setting import SystemSetting  # ユーザーが変更不可の設定クラス


class Fn:
    """自作関数クラス
    全体に適応される"""

    def log(*text):
        """ログの表示
            デバッグモードでのみ動作する
        Args:
            text (*str): 出力文字
        """
        if SystemSetting.debug:  # デバッグモードなら
            if len(text) == 1:
                # 要素数が1なら文字列にする
                print(text[0])
            else:
                # 要素数が2以上ならタプルにする
                print(text)

    def time_log(*text):
        """ログと現在時刻の表示
            デバッグモードでのみ動作する
        Args:
            text (*str): 出力文字
        """
        if SystemSetting.debug:  # デバッグモードなら
            now = datetime.now()  # 現在の時刻を取得
            if len(text) == 1:
                # 要素数が1なら文字列にする
                print(text[0], now.strftime("%H:%M:%S.%f")[:-3])  # 時刻の表示（ミリ秒三桁まで）
            else:
                # 要素数が2以上ならタプルにする
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

    def get_now_file_base_name():
        """ファイルのベース名用現在時刻の取得
        Returns:
            now_file_base_name(str) : ファイルのベース名用現在時刻("yyyymmdd_hhmmss")
        """
        now = datetime.now()  # 現在の時刻を取得
        now_file_base_name = now.strftime("%Y%m%d_%H%M%S")  # 時刻の表示
        return now_file_base_name  # ファイルのベース名用現在時刻

    def save_text_file(text_list, file_path):
        """テキストファイルへの保存
        Args:
            text_list(list[text:str]): テキストリスト
            filepath(src): ファイルパス
        """
        file = open(file_path, "w", encoding="utf-8")  # 新規書き込みでテキストファイルを開く
        # file = open(text_filepath, "w",)  # 新規書き込みでテキストファイルを開く
        for text_before in text_list:  # テキストで走査
            if text_before is not None:
                # テキストが存在するなら
                file.write(text_before + "\n")  # ファイルに書き込む
        file.close()  # ファイルを閉じる

    def get_max_file_name(dir_path):
        """辞書順で最大のファイル名を取得
        Args:
            dir_path (str): ディレクトリパス

        Returns:
            max_file_name: 辞書順で最大のファイル名
        """
        file_list = os.listdir(dir_path)  # ファイル名のリストを取得
        max_file_name = max(file_list)  # 辞書順で最大のファイル名を取得
        return max_file_name  # 辞書順で最大のファイル名

    def get_history_file_name_list():
        """履歴ファイル名のリストを取得

        翻訳前、後画像の両方が存在する履歴ファイル名を取得
        存在しないなら、該当ファイルを削除

        Returns:
            history_file_name_list: 履歴ファイル名のリスト
        """

        # 翻訳前画像保存先設定
        image_before_directory_path = SystemSetting.image_before_directory_path  # ディレクトリパス

        # 翻訳後画像保存先設定
        image_after_directory_path = SystemSetting.image_after_directory_path  # ディレクトリパス

        # 翻訳前画像ファイル名のリスト
        before_file_name_list = os.listdir(image_before_directory_path)
        # 翻訳後画像ファイル名のリスト
        after_file_name_list = os.listdir(image_after_directory_path)

        # 集合型に変換
        before_file_name_set = set(before_file_name_list)
        after_file_name_set = set(after_file_name_list)

        # 共通要素の取得
        common_file_name_set = before_file_name_set & after_file_name_set

        # 片方のみに存在する要素の取得
        before_only_file_name_set = before_file_name_set - common_file_name_set  # 翻訳前画像のみのファイル名の取得
        after_only_file_name_set = after_file_name_set - common_file_name_set  # 翻訳後画像のみのファイル名の取得

        # 翻訳前画像のみのファイルの削除
        for before_file_name in before_only_file_name_set:
            os.remove(image_before_directory_path + "/" + before_file_name)
        # 翻訳後画像のみのファイルの削除
        for after_file_name in after_only_file_name_set:
            os.remove(image_after_directory_path + "/" + after_file_name)

        # 履歴ファイル名のリストを取得
        history_file_name_list = list(common_file_name_set)

        # 昇順に並び替え
        history_file_name_list.sort()

        # .gitkeepを履歴ファイル名のリストから削除して返す
        return history_file_name_list[1:]

    def search_dict_in_list(lst, key_name, value):
        """与えられたリスト内の辞書から指定したキーと値に一致する辞書を取得

        Args:
            lst (list of dict): 検索対象の辞書要素が格納されたリスト
            key_name (str): 検索に使用するキーの名前
            value (任意の型) 検索する値

        Returns:
            dict: 一致する辞書（最初に見つかったもの）
        """

        for item in lst:  # リストから辞書を取り出す
            if item[key_name] == value:
                # 辞書のキーと値が一致するなら一致する辞書を返す
                return item

    def convert_time_from_filename(file_name):
        """ファイル名から日時を取得

        Args:
            file_name (str): ファイル名("yyyymmdd_hhmmss.拡張子")

        Returns:
            file_time (str): 日時("%Y/%m/%d %H:%M:%S")
        """
        # ファイルのベース名の取得
        file_base_name = file_name.split(".")[0]
        # "yyyymmdd_hhmmss"の形式の文字列を解析してdatetimeオブジェクトに変換
        dt = datetime.strptime(file_base_name, "%Y%m%d_%H%M%S")

        # "%Y/%m/%d %H:%M:%S"の形式にフォーマット
        file_time = dt.strftime("%Y/%m/%d %H:%M:%S")
        return file_time  # 日時("%Y/%m/%d %H:%M:%S")

    def convert_filename_from_time(file_time):
        """日時からファイル名を取得

        Args:
            file_time (str): 日時("%Y/%m/%d %H:%M:%S")

        Returns:
            file_name (str): ファイル名("yyyymmdd_hhmmss.拡張子")
        """
        # "%Y/%m/%d %H:%M:%S"の形式の文字列を解析してdatetimeオブジェクトに変換
        dt = datetime.strptime(file_time, "%Y/%m/%d %H:%M:%S")
        # "yyyymmdd_hhmmss"の形式にフォーマット
        file_base_name = dt.strftime("%Y%m%d_%H%M%S")
        # 拡張子の取得
        image_file_extension = ".png"
        # ファイル名の取得
        file_name = file_base_name + image_file_extension

        return file_name  # ファイル名("yyyymmdd_hhmmss.拡張子")
