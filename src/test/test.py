import os


dir_path = os.path.dirname(__file__)
print(dir_path)
file_list = os.listdir(dir_path)
print(file_list)
print(min(file_list))

def get_min_file_name(dir_path):
    """辞書順で最小のファイル名を取得

    Args:
        dir_path (str): ディレクトリパス

    Returns:
        min_file_name: 辞書順で最小のファイル名
    """
    file_list = os.listdir(dir_path)
    return min(file_list)