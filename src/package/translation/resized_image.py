import boto3  # AWSのAIサービス

from PIL import Image  # 画像処理

from package.fn import Fn  # 自作関数クラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from package.system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス


class ResizedImage:
    """リサイズ画像作成機能関連のクラス"""

    def get_resize_before_save_path(file_name):
        """リサイズした翻訳前画像の保存先パスの取得

        Args:
            file_name (str): ファイル名(現在日時)

        Returns:
            resize_before_save_path(str): リサイズした翻訳前画像の保存先パス
        """

        directory_path = SystemSetting.resize_before_directory_path  # 翻訳前画像のディレクトリパス
        file_extension = SystemSetting.image_file_extension  # 拡張子
        resize_before_save_path = directory_path + file_name + file_extension  # ファイルパス(絶対参照)
        return resize_before_save_path  # リサイズした翻訳前画像の保存先パス

    def get_resize_after_save_path(file_name):
        """リサイズした翻訳後画像の保存先パスの取得

        Args:
            file_name (str): ファイル名(現在日時)

        Returns:
            resize_after_save_path(str): リサイズした翻訳後画像の保存先パス
        """

        directory_path = SystemSetting.resize_after_directory_path  # 翻訳後画像のディレクトリパス
        file_extension = SystemSetting.image_file_extension  # 拡張子
        resize_after_save_path = directory_path + file_name + file_extension  # ファイルパス(絶対参照)
        return resize_after_save_path  # リサイズした翻訳後画像の保存先パス

    def save_keep_aspect_resize(img_path, save_path):
        """アスペクト比を保ったままリサイズして保存

        Args:
            img_path (str): 画像パス
            file_name(src): ファイル名(現在日時)
        """

        # リサイズ前の画像を読み込み
        img = Image.open(img_path)

        # リサイズ前画像サイズ
        img_width = img.width
        img_height = img.height

        # 表示画像サイズの最大
        image_width_max = UserSetting.image_width_max
        image_height_max = UserSetting.image_height_max

        # 拡大率の取得
        width_magnification_rate = image_width_max / img_width  # 表示サイズを超えない横幅の拡大率
        height_magnification_rate = image_height_max / img_height  # 表示サイズを超えない縦幅の拡大率
        magnification_rate = min(
            width_magnification_rate, height_magnification_rate
        )  # 小さいほうの拡大率を適用

        # リサイズするサイズ
        resize_width = round(img_width * magnification_rate)
        resize_height = round(img_height * magnification_rate)

        img_resized = img.resize(size=(resize_width, resize_height))  # 画像をリサイズする

        img_resized.save(save_path)  # リサイズ後画像保存

    def save_resize_image(img_path, save_path, magnification_rate):
        """リサイズして保存
        Args:
            img_path (str): 画像パス
            file_name(src): ファイル名(現在日時)
            magnification_rate(float): 拡大率
        """

        # リサイズ前の画像を読み込み
        img = Image.open(img_path)

        # リサイズ前画像サイズ
        img_width = img.width
        img_height = img.height

        # リサイズするサイズ
        resize_width = round(img_width * magnification_rate)
        resize_height = round(img_height * magnification_rate)

        img_resized = img.resize(size=(resize_width, resize_height))  # 画像をリサイズする

        img_resized.save(save_path)  # リサイズ後画像保存
