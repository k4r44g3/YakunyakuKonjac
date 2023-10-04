import pyautogui  # スクショ撮影


from fn import Fn  # 自作関数クラス
from user_setting import UserSetting # ユーザーが変更可能の設定クラス
from system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス


def get_screenshot():
    """スクリーンショットの撮影
    """
    screen_shot = pyautogui.screenshot(region=UserSetting.ss_region) # スクショ撮影
    screen_shot.save(SystemSetting.image_before_filepath) # スクショ画像保存

# def get_text_dict():
    

Fn.time_log("システム開始")

get_screenshot() # スクショ撮影

Fn.time_log("スクショ撮影")