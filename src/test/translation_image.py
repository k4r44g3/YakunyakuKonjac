import os  # ディレクトリ管理
import sys  # システム関連
from typing import Any, Dict, List, Optional, Tuple, Union  # 型ヒント

# 翻訳されたテキストを日本語で表示するためにフォントとサイズを指定
from PIL import Image, ImageDraw, ImageFont

#! デバッグ用
if __name__ == "__main__":
    src_path = os.path.join(os.path.dirname(__file__), "..", "..")  # パッケージディレクトリパス
    sys.path.append(src_path)  # モジュール検索パスを追加

from package.debug import Debug  # デバッグ用クラス
from package.fn import Fn  # 自作関数クラス
from package.system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス


class TranslationImage:
    """オーバーレイ翻訳画像作成機能関連のクラス"""

    def get_overlay_translation_image(
        user_setting: "UserSetting", ss_file_path: str, text_after_list: List[str], text_region_list: Dict[str, int]
    ) -> "Image":
        """オーバーレイ翻訳画像の取得

        Args:
            user_setting(UserSetting): ユーザーが変更可能の設定
            ss_file_path(str): スクショ画像のファイルパス
            text_after_list(List[text_after(str)]) : 翻訳後テキスト内容のリスト
            text_region_list(List[text_region]): テキスト範囲のリスト
                - text_region(dict{Left:int, Top:int, Width:int, Height:int}): テキスト範囲

        Returns:
            overlay_translation_image(Image): オーバーレイ翻訳画像
        """

        image_out = Image.open(ss_file_path)  # 出力画像を作成

        draw = ImageDraw.Draw(image_out)  # 画像に図形やテキストを描画するオブジェクトの作成

        # 言語情報一覧リストの取得
        language_list = SystemSetting.language_list
        # 翻訳後言語の取得
        target_language_code = user_setting.get_setting("target_language_code")
        # フォントパスの取得
        font_path = Fn.search_dict_in_list(language_list, "code", target_language_code)["font_path"]

        # フォントサイズと行数の計算
        font_size_info = TranslationImage.find_max_font_size(font_path, text_after_list, text_region_list)

        # フォントサイズ
        font_size_list = [d["font_size_list"] for d in font_size_info]

        # 行数
        line_count_list = [d["line_count_list"] for d in font_size_info]

        # フォントサイズが0である要素の削除
        TranslationImage.remove_empty_text_data(font_size_list, text_after_list, text_region_list, line_count_list)

        # 画像内のテキストボックスを塗りつぶす処理
        TranslationImage.fill_text_box_image(draw, text_region_list)

        # 画像にテキストを描画する処理
        TranslationImage.draw_text_image(
            draw, font_path, text_after_list, text_region_list, font_size_list, line_count_list
        )

        return image_out

    def find_max_font_size(
        font_path: str, text_after_list: List[str], text_region_list: List[Dict[str, int]]
    ) -> List[Dict[str, List[int]]]:
        """テキストボックスに収まる最大のフォントサイズと行数のリストの取得

        Args:
            font_path(str) : フォントファイルのパス
            text_after_list(List[text_after(str)]) : 翻訳後テキスト内容のリスト
            text_region_list(List[text_region]): テキスト範囲のリスト
                - text_region(dict{Left:int, Top:int, Width:int, Height:int}): テキスト範囲

        Returns:
            font_size_info(list[dict{font_size_list, line_count_list}]): 最大のフォントサイズと行数のリスト
                - font_size_list(list[font_size(int)]): 最大のフォントサイズ(偶数)のリスト
                - line_count_list(list[line_count(int)]): 行数のリスト
        """
        font_size_info = []  # フォントサイズのリスト
        # ブロックごとに走査
        for text_after, text_region in zip(text_after_list, text_region_list):
            if text_after is not None:
                # 翻訳後テキストが存在するなら
                line_count = 1  # 行数
                # テキストボックスの幅と高さを取得
                text_box_width = text_region["width"]
                text_box_height = text_region["height"]
                font_size = 2  # フォントサイズの初期値
                font_image = ImageFont.truetype(font_path, font_size)  # フォントオブジェクトの作成

                # テキストボックスと同じサイズの、テキスト描画用イメージオブジェクトを作成
                image = Image.new("RGB", (text_box_width, text_box_height))
                # 画像に図形やテキストを描画するオブジェクトの作成
                draw = ImageDraw.Draw(image)

                while True:
                    # 指定したフォントサイズでテキストのバウンディングボックスを計算
                    font_image = font_image.font_variant(size=font_size)  # フォントサイズの更新
                    # テキスト範囲の取得
                    now_text_region = draw.textbbox((0, 0), text=text_after, font=font_image)
                    # 現在のフォントでのテキストサイズの取得
                    now_text_width = now_text_region[2] - now_text_region[0]  # テキストサイズの横幅取得
                    # テキストサイズの縦幅
                    # ? 欧米文字などは文字によって縦幅が違う
                    now_text_height = font_size * 1.5  # テキストサイズの縦幅取得
                    # now_text_height = now_text_region[3] - now_text_region[1]  # テキストサイズの縦幅取得

                    # 改行分の空白文字を現在のテキストサイズの横幅に追加する処理
                    # 複数行なら
                    if line_count > 1:
                        # 全角空白文字の範囲の取得
                        full_width_space_region = draw.textbbox((0, 0), text="　", font=font_image)
                        # 全角空白文字の横幅の取得
                        full_width_space_width = full_width_space_region[2] - full_width_space_region[0]
                        # 改行分の空白文字を現在のテキストサイズの横幅に追加
                        now_text_width += full_width_space_width * (line_count - 1)

                    # 縦幅がテキストボックスに収まるなら
                    if now_text_height < text_box_height / line_count:
                        # 横幅がテキストボックスに収まるなら。（複数行の場合は行数分テキストボックスを拡大）
                        if now_text_width < text_box_width * line_count:
                            # フォントサイズを加算する
                            font_size += 2
                            continue

                        # 横幅がテキストボックスに収まらないなら
                        else:
                            # 改行するとテキストボックスに収まるなら
                            if (now_text_width < text_box_width * (line_count + 1)) and (  # 1行に繋げた時に横幅が超えない
                                now_text_height < text_box_height / (line_count + 1)  # 改行した時に縦幅が超えないなら
                            ):
                                # 行数を増やす
                                line_count += 1
                                continue

                    # 改行してもテキストボックスに収まらないなら
                    font_size -= 2  # 収まるサイズに戻す

                    # フォントサイズと行数を保存
                    font_size_info.append({"font_size_list": font_size, "line_count_list": line_count})
                    break

        return font_size_info  # テキストボックスに収まる最大のフォントサイズのリスト

    def remove_empty_text_data(
        font_size_list: List[int],
        text_after_list: List[str],
        text_region_list: Dict[str, int],
        line_count_list: List[int],
    ) -> None:
        """フォントサイズが0である要素の削除

        Args:
            font_size_list (list[font_size(int)]): 最大のフォントサイズ(偶数)のリスト
            text_after_list(List[text_after(str)]) : 翻訳後テキスト内容のリスト
            text_region_list(List[text_region]): テキスト範囲のリスト
                - text_region(dict{Left:int, Top:int, Width:int, Height:int}): テキスト範囲
            line_count_list(list[line_count(int)]): 行数のリスト
        """
        # フォントサイズが0である要素番号のリストの取得
        zero_font_size_index_list = [index for index, font_size in enumerate(font_size_list) if font_size == 0]

        # フォントサイズが0である要素番号で走査（削除後の要素番号のずれを防ぐために逆順にソート）
        for delete_index in zero_font_size_index_list[::-1]:
            # フォントサイズが0の要素を削除
            del font_size_list[delete_index]
            del text_after_list[delete_index]
            del text_region_list[delete_index]
            del line_count_list[delete_index]

    def fill_text_box_image(draw: "ImageDraw", text_region_list: Dict[str, int]) -> None:
        """画像内のテキストボックスを塗りつぶす処理

        Args:
            draw (ImageDraw): 画像に図形やテキストを描画するオブジェクト
            text_region_list(List[text_region]): テキスト範囲のリスト
                - text_region(dict{Left:int, Top:int, Width:int, Height:int}): テキスト範囲
        """
        background_color = "#FFF"  # 背景色
        background_border_color = "#FFF"  # 背景の枠線の色

        # ブロックごとに走査
        for text_region in text_region_list:
            # テキストボックスの背景の描画
            draw.rectangle(
                # 背景描画座標
                xy=(
                    text_region["left"],  # テキストボックスの左側x座標の取得
                    text_region["top"],  # テキストボックスの上側y座標の取得
                    text_region["left"] + text_region["width"],  # テキストボックスの右側x座標の取得
                    text_region["top"] + text_region["height"],  # テキストボックスの下側y座標の取得
                ),
                fill=background_color,  # 背景色
                outline=background_border_color,  # 背景の枠線の色
            )

    def draw_text_image(
        draw: "ImageDraw",
        font_path: str,
        text_after_list: List[str],
        text_region_list: Dict[str, int],
        font_size_list: List[int],
        line_count_list: List[int],
    ) -> None:
        """画像にテキストを描画する処理

        Args:
            draw (ImageDraw): 画像に図形やテキストを描画するオブジェクト
            font_path(str) : フォントファイルのパス
            text_after_list(List[text_after(str)]) : 翻訳後テキスト内容のリスト
            text_region_list(List[text_region]): テキスト範囲のリスト
                - text_region(dict{Left:int, Top:int, Width:int, Height:int}): テキスト範囲
            font_size_list (list[font_size]): 最大のフォントサイズ(偶数)のリスト
            line_count_list(list[line_count(int)]): 行数のリスト
        """
        font_color = "#000"  # フォントカラー

        # ブロックごとに走査
        for text_after, text_region, font_size, line_count in zip(
            text_after_list,  # 翻訳語テキスト内容のリスト
            text_region_list,  # テキスト範囲のリスト
            font_size_list,  # フォントサイズのリスト
            line_count_list,  # 行数のリスト
        ):
            # 翻訳後テキストが存在するなら
            if text_after is not None:
                # フォントの設定
                font_image = ImageFont.truetype(font_path, font_size)

                # テキストが1行なら
                if line_count == 1:
                    # 翻訳されたテキストを指定した座標に描画
                    draw.text(
                        (text_region["left"], text_region["top"]),
                        text_after,
                        fill=font_color,
                        font=font_image,
                    )
                # テキストが複数行なら
                else:
                    # 全体のテキスト範囲を計算
                    all_text_region = draw.textbbox((0, 0), text=text_after + "　" * line_count, font=font_image)

                    # 全体のテキスト幅を計算
                    all_text_width = all_text_region[2] - all_text_region[0]  # テキストサイズの横幅取得

                    # 1行あたりの最大幅を計算
                    line_text_max_width = all_text_width / line_count
                    # 結果を格納するリスト
                    text_lines = []
                    current_line = ""  # 現在の行のテキスト
                    current_width = 0  # 現在の行の幅

                    # 1文字ずつ走査
                    for text_index, char in enumerate(text_after):
                        # 現在の文字の範囲を計算
                        char_region = draw.textbbox((0, 0), text=char, font=font_image)

                        # 現在の文字の横幅を計算
                        char_width = char_region[2] - char_region[0]  # テキストサイズの横幅取得

                        # テキストの末尾でないなら
                        if text_index != len(text_after) - 1:
                            # 現在の行に文字を追加しても最大幅を超えないなら
                            if current_width + char_width <= line_text_max_width and text_index != len(text_after) - 1:
                                current_line += char  # 現在の行に文字を追加
                                current_width += char_width  # 現在の行の幅を加算

                            # 現在の行に文字を追加すると最大幅を超えるなら
                            else:
                                text_lines.append(current_line)  # 現在の行の保存
                                current_line = char  # 新しい行に文字を追加
                                current_width = char_width  # 新しい行に幅を追加

                        # テキストの末尾なら
                        else:
                            current_line += char  # 現在の行に文字を追加
                            current_width += char_width  # 現在の行の幅を加算
                            text_lines.append(current_line)  # 現在の行の保存

                    # 翻訳後テキストを改行する
                    text_after = "\n".join(text_lines)

                    # 翻訳されたテキストを指定した座標に描画
                    draw.text(
                        (text_region["left"], text_region["top"]),
                        text_after,
                        fill=font_color,
                        font=font_image,
                    )

    def save_overlay_translation_image(overlay_translation_image: Image, file_name: str) -> str:
        """オーバーレイ翻訳画像の保存
        Args:
            overlay_translation_image(Image): オーバーレイ翻訳画像
            file_name(str): ファイル名(撮影日時)
        Returns:
            overlay_translation_image_path(str): オーバーレイ翻訳画像のファイルパス
        """
        directory_path = SystemSetting.image_after_directory_path  # 翻訳後画像のディレクトリパス
        overlay_translation_image_path = os.path.join(directory_path, file_name)  # ファイルパス(絶対参照)

        overlay_translation_image.save(overlay_translation_image_path)  # 翻訳後画像保存

        return overlay_translation_image_path  # 翻訳後画像ファイルパス


# ! デバッグ用
if __name__ == "__main__":
    user_setting = UserSetting()  # ユーザ設定のインスタンス化
    ss_file_path = Debug.ss_file_path  # スクショ画像パス
    text_after_list = Debug.text_before_list  # 翻訳後テキストリスト
    text_region_list = Debug.text_region_list  # テキスト範囲のリスト

    # オーバーレイ翻訳画像の取得
    overlay_translation_image = TranslationImage.get_overlay_translation_image(
        user_setting, ss_file_path, text_after_list, text_region_list
    )
    # オーバーレイ翻訳画像の表示
    overlay_translation_image.show()
