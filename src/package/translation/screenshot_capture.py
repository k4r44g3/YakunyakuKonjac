import pyautogui  # スクショ撮影

from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from package.system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス


class ScreenshotCapture:
    """スクリーンショット撮影機能関連のクラス"""

    def get_screenshot():
        """スクリーンショットの撮影

        Returns:
            Image: スクショ画像
        """
        ss_region = UserSetting.ss_region  # SS撮影範囲

        screenshot_image = pyautogui.screenshot(region=ss_region)  # スクショ撮影

        return screenshot_image  # スクショ画像

    def save_screenshot(screenshot_image, file_name):
        """スクリーンショットの保存
        Args:
            screenshot_image(Image): スクショ画像
            file_name(src): ファイル名(現在日時)
        Returns:
            ss_file_path(str): スクショ画像のファイルパス
        """
        directory_path = SystemSetting.image_before_directory_path  # 翻訳前画像のディレクトリパス
        file_extension = SystemSetting.image_file_extension  # 拡張子
        ss_file_path = directory_path + file_name + file_extension  # ファイルパス(絶対参照)
        screenshot_image.save(ss_file_path)  # 翻訳前画像保存

        return ss_file_path  # 翻訳前画像ファイルパス
