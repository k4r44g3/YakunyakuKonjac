from typing import Any, Dict, List, Optional, Tuple, Union  # 型ヒント

import boto3  # AWSのAIサービス
from deep_translator import GoogleTranslator  # google翻訳
from deep_translator.exceptions import TooManyRequests  # APIエラー取得
from package.fn import Fn  # 自作関数クラス
from package.system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス


class TextTranslation:
    """テキスト翻訳機能関連のクラス"""

    def get_text_after_list(
        user_setting: "UserSetting", text_before_list: List[str]
    ) -> Dict[str, Union[Optional[List[str]], bool, Optional[Exception]]]:
        """翻訳後テキストの取得

        Args:
            user_setting(UserSetting): ユーザーが変更可能の設定
            text_before_list(List[text_before]) : 翻訳前テキストのリスト
                - text_before(str) : 翻訳前テキスト
        Returns:
            result(dict[text_after_list, is_error, error_name, error_text]) : 翻訳後テキストのリストとエラー情報の辞書
                - text_after_list(Optional[List[text_after]]) : 翻訳後テキストのリスト
                    - text_after(str) : 翻訳後テキスト
                - is_error(bool) : エラーが発生したかどうか
                - exception(Optional[Exception]): 発生した例外オブジェクト
        """

        translation_soft = user_setting.get_setting("translation_soft")  # 翻訳ソフト

        # OCRソフトによって分岐
        if translation_soft == "AmazonTranslate":  # 翻訳ソフトがAmazonTranslateなら
            # AmazonTranslateを使用して、翻訳後テキストとエラー情報を取得
            translate_result = TextTranslation.amazon_translate(user_setting, text_before_list)
        elif translation_soft == "GoogleTranslator":
            # GoogleTranslatorを使用して、翻訳後テキストとエラー情報を取得
            translate_result = TextTranslation.google_translator(user_setting, text_before_list)

        # 翻訳後テキストとエラー情報を返す
        return translate_result

    def amazon_translate(
        user_setting: "UserSetting", text_before_list: List[str]
    ) -> Dict[str, Union[Optional[List[str]], bool, Optional[Exception]]]:
        """AmazonTranslateを使用して、翻訳後テキストを取得

        Args:
            user_setting(UserSetting): ユーザーが変更可能の設定
            text_before_list(List[text_before]) : 翻訳前テキストのリスト
                - text_before(str) : 翻訳前テキスト
        Returns:
            result(dict[text_after_list, is_error, error_name, error_text]) : 翻訳後テキストのリストとエラー情報の辞書
                - text_after_list(Optional[List[text_after]]) : 翻訳後テキストのリスト
                    - text_after(str) : 翻訳後テキスト
                - is_error(bool) : エラーが発生したかどうか
                - exception(Optional[Exception]): 発生した例外オブジェクト
        """
        source_language_code = user_setting.get_setting("source_language_code")  # 翻訳前言語
        target_language_code = user_setting.get_setting("target_language_code")  # 翻訳後言語

        text_after_list = []  # 翻訳語テキストのリスト作成

        try:
            translate = boto3.client("translate")  # Translate サービスクライアントを作成

            for text_before in text_before_list:  # 翻訳前テキストで走査
                # 英語から日本語に翻訳
                result = translate.translate_text(
                    Text=text_before,  # 翻訳テキスト
                    SourceLanguageCode=source_language_code,  # 翻訳前言語
                    TargetLanguageCode=target_language_code,  # 翻訳後言語
                )
                text_after_list.append(result["TranslatedText"])  # 翻訳後テキストのリスト作成

            return {
                "text_after_list": text_after_list,  # 翻訳後テキストのリスト
                "is_error": False,  # エラーが発生したかどうか
                "exception": None,  # エラークラス
            }

        # 不明なエラーが発生したなら
        except Exception as e:
            raise  # 例外を発生させる

    def google_translator(
        user_setting: "UserSetting", text_before_list: List[str]
    ) -> Dict[str, Union[Optional[List[str]], bool, Optional[Exception]]]:
        """GoogleTranslatorを使用して、翻訳後テキストを取得

        Args:
            user_setting(UserSetting): ユーザーが変更可能の設定
            text_before_list(List[text_before]) : 翻訳前テキストのリスト
                - text_before(str) : 翻訳前テキスト
        Returns:
            result(dict[text_after_list, is_error, error_name, error_text]) : 翻訳後テキストのリストとエラー情報の辞書
                - text_after_list(Optional[List[text_after]]) : 翻訳後テキストのリスト
                    - text_after(str) : 翻訳後テキスト
                - is_error(bool) : エラーが発生したかどうか
                - exception(Optional[Exception]): 発生した例外オブジェクト
        """
        source_language_code = user_setting.get_setting("source_language_code")  # 翻訳前言語
        target_language_code = user_setting.get_setting("target_language_code")  # 翻訳後言語

        text_after_list = []  # 翻訳語テキストのリスト作成

        try:
            # 翻訳オブジェクト作成
            google_translator = GoogleTranslator(source=source_language_code, target=target_language_code)

            # 翻訳前テキストで走査
            for text_before in text_before_list:
                # 英語から日本語に翻訳
                result = google_translator.translate(text=text_before)
                text_after_list.append(result)  # 翻訳後テキストのリスト作成

            return {
                "text_after_list": text_after_list,  # 翻訳後テキストのリスト
                "is_error": False,  # エラーが発生したかどうか
                "exception": None,  # エラークラス
            }

        # サーバーへのリクエスト超過エラーが発生したなら
        except TooManyRequests as e:
            return {
                "text_after_list": None,  # 翻訳後テキストのリスト
                "is_error": True,  # エラーが発生したかどうか
                "exception": e,  # エラークラス
            }
        # 不明なエラーが発生したなら
        except Exception as e:
            raise  # 例外を発生させる
