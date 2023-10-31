import re
import datetime


def is_valid_filename(filename):
    # 正規表現で"yyyymmdd_hhmmss.拡張子"の形式に一致するかチェック
    match = re.match(r"^(\d{8})_(\d{6})\..+$", filename)
    if not match:
        return False

    # キャプチャグループから日付と時刻の部分を取得
    date_str, time_str = match.groups()

    # 日付と時刻の形式が正しいかチェック
    try:
        datetime.datetime.strptime(date_str + time_str, "%Y%m%d%H%M%S")
        return True
    except ValueError:
        return False


# テスト
print(is_valid_filename("20231031_123456.txt"))  # True
print(is_valid_filename("20234431_123456.txt"))  # False
print(is_valid_filename("invalid_filename.txt"))  # False
