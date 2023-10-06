import os  # ファイル操作
from decimal import Decimal  # 固定小数点
import pyautogui as pag  # スクショ撮影
import PySimpleGUI as sg  # GUI

from package.fn import Fn  # 自作関数クラス
from package.debug import Debug  # デバッグ用クラス
from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス
from package.system_setting import SystemSetting  # ユーザーが変更不可能の設定クラス

from package.translation.translation import Translation  # 翻訳機能関連のクラス
from package.window.translation_win import TranslationWin  # メインウィンドウクラス

Fn.time_log("システム開始")
# メインウィンドウの処理

transition_target_win = TranslationWin  # 遷移先ウィンドウ名

win_instance = transition_target_win()  # 遷移先ウィンドウ作成

Fn.time_log("システム終了")

# ! 翻訳処理
# Translation.save_history()
