import boto3  # AWSのAIサービス

from fn import Fn  # 自作関数クラス
from user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス


class TextTranslation:
    """テキスト翻訳機能関連のクラス"""

    def get_text_after_list(text_before_list):
        """翻訳後テキストの取得

        Args:
            text_before_list(List[text_before]) : 翻訳前テキストのリスト
                - text_before(str) : 翻訳前テキスト
        Returns:
            text_after_list(List[text_after]) : 翻訳後テキストのリスト
                - text_after(str) : 翻訳後テキスト
        """

        translation_soft = UserSetting.translation_soft  # 翻訳ソフト
        source_language_code = UserSetting.source_language_code  # 翻訳前言語
        target_language_code = UserSetting.target_language_code  # 翻訳後言語

        # OCRソフトによって分岐
        if translation_soft == "Amazon Translate":  # 翻訳ソフトがAmazonなら
            translate = boto3.client("translate")  # Translate サービスクライアントを作成
            text_after_list = []  # 翻訳語テキストのリスト作成

            for text_before in text_before_list:  # 翻訳前テキストで走査
                # 英語から日本語に翻訳
                result = translate.translate_text(
                    Text=text_before,  # 翻訳テキスト
                    SourceLanguageCode=source_language_code,  # 翻訳前言語
                    TargetLanguageCode=target_language_code,  # 翻訳後言語
                )
                text_after_list.append(result["TranslatedText"])  # 翻訳後テキストのリスト作成
        return text_after_list  # 翻訳後テキストのリスト

    def save_text_after(text_after_list, file_name):
        """翻訳後テキストをファイルに保存
        Args:
            text_after_list(list[text_after:str]): 翻訳後テキストリスト
            file_name(src): ファイル名(現在日時)
        """
        directory_path = SystemSetting.text_after_directory_path  # 翻訳後テキストのディレクトリパス
        file_extension = ".txt"  # 拡張子
        file_path = directory_path + file_name + file_extension  # ファイルパス(絶対参照)
        Fn.save_text_file(text_after_list, file_path)  # テキストファイルへの保存
