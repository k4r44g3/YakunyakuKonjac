from datetime import datetime


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
