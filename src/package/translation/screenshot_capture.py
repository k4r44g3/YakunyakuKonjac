import os

import pyautogui  # スクショ撮影
from package.system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from PIL import Image  # 画像処理


class ScreenshotCapture:
    """スクリーンショット撮影機能関連のクラス"""

    def get_screenshot(user_setting: "UserSetting") -> None:
        """スクリーンショットの撮影
        Args:
            user_setting(UserSetting): ユーザーが変更可能の設定
        Returns:
            Image: スクショ画像
        """

        # スクリーンショット撮影範囲(left, top, width, height)の取得
        ss_region = [
            user_setting.get_setting("ss_left_x"),  # SS範囲の左側x座標
            user_setting.get_setting("ss_top_y"),  # SS範囲の上側y座標
            abs(user_setting.get_setting("ss_right_x") - user_setting.get_setting("ss_left_x")),  # SS範囲の横幅
            abs(user_setting.get_setting("ss_bottom_y") - user_setting.get_setting("ss_top_y")),  # SS範囲の縦幅
        ]

        screenshot_image = pyautogui.screenshot(region=ss_region)  # スクショ撮影

        return screenshot_image  # スクショ画像

    def save_screenshot(screenshot_image: "Image", file_name: str) -> str:
        """スクリーンショット画像の一時保存
        Args:
            screenshot_image(Image): スクショ画像
            file_name(str): ファイル名(撮影日時)
        Returns:
            ss_file_path(str): スクショ画像のファイルパス
        """
        directory_path = SystemSetting.image_tmp_directory_path  # 翻訳中一時保存画像のディレクトリパス
        ss_file_path = os.path.join(directory_path, f"before_{file_name}")  # ファイルパス(絶対参照)
        screenshot_image.save(ss_file_path)  # 翻訳前画像保存

        return ss_file_path  # 翻訳前画像ファイルパス
