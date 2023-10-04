import pyautogui  # スクショ撮影


from fn import Fn  # 自作関数クラス
from user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス


def get_screenshot():
    """スクリーンショットの撮影

    Returns:
        Image: スクショ画像
    """
    ss_region = UserSetting.ss_region  # SS撮影範囲

    screenshot = pyautogui.screenshot(region=ss_region)  # スクショ撮影

    return screenshot # スクショ画像


def save_screenshot(screenshot,filename):
    """スクリーンショットの保存
    Args:
        screenshot(Image): スクショ画像
        filename(src): ファイル名(現在日時)
    """
    filepath = SystemSetting.image_before_filepath  # 翻訳前画像パス
    file_extension = SystemSetting.image_file_extension  # 拡張子
    screenshot.save(filepath + filename + file_extension)  # スクショ画像保存


# def get_text_dict():


Fn.time_log("システム開始")

screenshot = get_screenshot()  # スクショ撮影

Fn.time_log("スクショ撮影")

filename = Fn.get_filename()  # ファイル名(現在日時)

save_screenshot(screenshot,filename)

print(Fn.get_filename())
