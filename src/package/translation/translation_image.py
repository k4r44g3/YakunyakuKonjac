import os  # ディレクトリ管理

# 翻訳されたテキストを日本語で表示するためにフォントとサイズを指定
from PIL import Image, ImageFont, ImageDraw


from package.system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス


class TranslationImage:
    """オーバーレイ翻訳画像作成機能関連のクラス"""

    def get_overlay_translation_image(ss_file_path, text_after_list, text_region_list):
        """オーバーレイ翻訳画像の取得

        Args:
            ss_file_path(str): スクショ画像のファイルパス
            text_after_list(List[text(str)]) : 翻訳後テキスト内容のリスト
            text_region_list(List[region]): テキスト範囲のリスト
                - text_region(dict{Left:int, Top:int, Width:int, Height:int}): テキスト範囲
        Returns:
            overlay_translation_image(Image): オーバーレイ翻訳画像
        """

        image_out = Image.open(ss_file_path)  # 出力画像を作成

        font_path = SystemSetting.font_file_path  # 使用するフォントファイルのパス
        font_color = "#000"  # フォントカラー
        background_color = "#FFF"  # 背景色
        background_border_color = "#000"  # 背景の枠線の色

        # ブロックごとに走査
        for text_after, region in zip(text_after_list, text_region_list):
            max_w_font_size = region["width"] // len(text_after)  # 横の最大フォントサイズ
            max_h_font_size = region["height"]  # 縦の最大フォントサイズ

            font_size = min(max_w_font_size, max_h_font_size)  # 最大フォントサイズが小さい方に設定する

            # フォントサイズが偶数になるように処理
            if font_size % 2 == 1:  # フォントサイズが奇数なら
                font_size -= 1  # フォントサイズを1小さくする

            draw = ImageDraw.Draw(image_out)  # 元画像のオブジェクト
            font = ImageFont.truetype(font_path, font_size)  # フォントの設定

            right = region["left"] + region["width"]  # テキストボックスの左側x座標の取得
            bottom = region["top"] + region["height"]  # テキストボックスの下側y座標の取得

            # テキストボックスの背景の描画
            draw.rectangle(
                xy=(region["left"], region["top"], right, bottom),  # 背景描画座標
                fill=background_color,  # 背景色
                outline=background_border_color,  # 背景の枠線の色
            )

            # 翻訳されたテキストを指定した座標に描画
            draw.text((region["left"], region["top"]), text_after, fill=font_color, font=font)

        return image_out

    def save_overlay_translation_image(overlay_translation_image, file_name):
        """オーバーレイ翻訳画像の保存
        Args:
            overlay_translation_image(Image): オーバーレイ翻訳画像
            file_name(src): ファイル名(現在日時)
        Returns:
            overlay_translation_image_path(str): オーバーレイ翻訳画像のファイルパス
        """
        directory_path = SystemSetting.image_after_directory_path  # 翻訳後画像のディレクトリパス
        file_extension = SystemSetting.image_file_extension  # 拡張子
        overlay_translation_image_path = directory_path + file_name + file_extension  # ファイルパス(絶対参照)

        overlay_translation_image.save(overlay_translation_image_path)  # 翻訳後画像保存

        return overlay_translation_image_path  # 翻訳後画像ファイルパス
