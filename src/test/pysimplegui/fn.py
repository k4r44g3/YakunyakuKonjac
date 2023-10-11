import datetime  # 現在時刻
import os  # ディレクトリ関連
import json  # jsonファイルの読み書き


class Fn:
    """自作関数クラス
    全体に適応される"""

    def get_now_file_name():
        """ファイル名用現在時刻の取得
        Returns:
            now_file_name(str) : 現在時刻("yyyymmdd_hhmmss_fff")
        """
        now = datetime.datetime.now()  # 現在の時刻を取得
        now_file_name = now.strftime("%Y%m%d_%H%M%S_%f")[:-3]  # 時刻の表示（ミリ秒三桁まで）
        return now_file_name  # ファイル名用現在時刻

    def log(*text):
        """ログの表示
            デバッグモードでのみ動作する
        Args:
            text (*str): 出力文字
        """
        if True:  # デバッグモードなら
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
        if True:  # デバッグモードなら
            now = datetime.datetime.now()  # 現在の時刻を取得
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

    def save_text_file(text_list, file_path):
        """テキストファイルへの保存
        Args:
            text_list(list[text:str]): テキストリスト
            filepath(src): ファイルパス
        """
        file = open(file_path, "w", encoding="utf-8")  # 新規書き込みでテキストファイルを開く
        # file = open(text_filepath, "w",)  # 新規書き込みでテキストファイルを開く
        for text_before in text_list:  # テキストで走査
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

    def create_setting_file():
        """設定ファイルを新規作成して辞書として返す

        Returns:
            default_setting(dict): デフォルトの設定
        """
        setting_file_path = os.path.dirname(__file__) + "/setting.json"  # 設定ファイルのパス
        default_setting = {"-name-": "山田太郎", "-age-": "20"}  # デフォルトの設定
        with open(
            file=setting_file_path, mode="w"
        ) as f:  # ファイルを開く(書き込み)
            json.dump(obj=default_setting, fp=f, indent=2)  # ファイルの新規作成
        return default_setting  # デフォルト設定を戻り値に指定

    def load_setting_file():
        """設定ファイルを読み込み辞書として返す
        設定ファイルが存在しない場合は新規作成する

        Returns:
            setting(dict): 読み込んだ設定
        """
        setting_file_path = os.path.dirname(__file__) + "/setting.json"  # 設定ファイルのパス

        # 設定ファイルの読み込み処理（ファイルが存在しないなら新規作成）
        if os.path.isfile(setting_file_path):  # ファイルが存在するなら
            # ファイルが存在するなら読み込む
            with open(setting_file_path, "r") as f:  # ファイルを開く(読み込み)
                setting = json.load(f)  # ファイルを読み込む
        else:
            # ファイルが存在しないなら新規作成して読み込む
            Fn.time_log("設定ファイルが存在しません。作成します。")
            setting = Fn.create_setting_file()  # デフォルトを戻り値に指定
        return setting # 設定を戻り値に指定

    def save_setting_file(current_setting,update_setting):
        """現在の設定を更新して、jsonファイルに保存する

        Args:
            current_setting (dict): 現在の設定
            update_setting (dict): 更新する設定
        """

        setting_file_path = os.path.dirname(__file__) + "/setting.json"  # 設定ファイルのパス

        current_setting.update(update_setting) # 現在の設定を更新

        with open(setting_file_path, "w") as f:  # ファイルを開く(書き込み)
            json.dump(obj=current_setting, fp=f, indent=2)  # ファイルに読み込む
