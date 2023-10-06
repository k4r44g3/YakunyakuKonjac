import boto3  # AWSのAIサービス

from PIL import Image  # 画像処理

from package.fn import Fn  # 自作関数クラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from package.system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス


class CharacterRecognition:
    """文字認識機能関連のクラス"""

    def get_text_data_dict(ss_file_path):
        """画像からテキスト情報を取得
        Args:
            textract(Textract): Textractサービスクライアント
            ss_file_path(src): スクショ画像のファイルパス
        Returns:
            text_data_dict(List[text_list,text_region_list]): テキスト情報リスト
                - text_list(List[text(str)]) : テキスト内容のリスト
                - text_region_list(List[region]): テキスト範囲のリスト
                    - text_region(dict{Left:int, Top:int, Width:int, Height:int}): テキスト範囲
        """
        ocr_soft = UserSetting.ocr_soft  # OCRソフト

        # OCRソフトによって分岐
        if ocr_soft == "Amazon Textract":  # OCRソフトがAmazonなら
            textract = boto3.client("textract", "us-east-1")  # Textractサービスクライアントを作成

            text_list = []  # テキスト内容のリスト
            text_region_list = []  # テキスト範囲のリスト

            image_in = Image.open(ss_file_path)  # 入力画像のファイルを読み込む
            w, h = image_in.size  # 画像サイズを取得

            with open(ss_file_path, "rb") as file:  # 画像ファイルを開く
                result = textract.detect_document_text(Document={"Bytes": file.read()})  # 文字列を検出

            for block in result["Blocks"]:  # 検出されたブロックを順番に処理
                if block["BlockType"] == "LINE":  # ブロックタイプが行かどうかを調べる
                    text = block["Text"]  # テキスト内容取得
                    box = block["Geometry"]["BoundingBox"]  # バウンディングボックスを取得
                    # テキスト範囲の取得
                    text_region = {
                        "left": int(box["Left"] * w),  # テキスト範囲の左側x座標
                        "top": int(box["Top"] * h),  # テキスト範囲の上側y座標
                        "width": int(box["Width"] * w),  # テキスト範囲の横幅
                        "height": int(box["Height"] * h),  # テキスト範囲の縦幅
                    }
                    text_list.append(text)  # テキスト内容のリスト
                    text_region_list.append(text_region)  # テキスト範囲のリスト

        text_data_list = {
            "text_list": text_list,
            "text_region_list": text_region_list,
        }  # テキスト情報のリスト作成
        return text_data_list  # テキスト情報のリスト

    def save_text_before(text_before_list, file_name):
        """翻訳前テキストをファイルに保存
        Args:
            text_before_list(list[text_before:str]): 翻訳前テキストリスト
            file_name(src): ファイル名(現在日時)
        """
        directory_path = SystemSetting.text_before_directory_path  # 翻訳前テキストのディレクトリパス
        file_extension = ".txt"  # 拡張子
        file_path = directory_path + file_name + file_extension  # ファイルパス(絶対参照)
        Fn.save_text_file(text_before_list, file_path)  # テキストファイルへの保存
