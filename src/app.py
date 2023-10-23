from package.fn import Fn  # 自作関数クラス

from package.window.translation_win import TranslationWin  # 翻訳画面ウィンドウクラス
from package.window.input_win import InputWin  # 入力画面ウィンドウクラス
from package.window.output_win import OutputWin  # 出力画面ウィンドウクラス

from package.window.display_setting_win import DisplaySettingWin  # 表示設定画面ウィンドウクラス
from package.window.environment_setting_win import EnvironmentSettingWin  # 環境設定画面ウィンドウクラス
from package.window.key_setting_win import KeySettingWin  # キー設定画面ウィンドウクラス
from package.window.language_setting_win import LanguageSettingWin  # 言語設定画面ウィンドウクラス
from package.window.save_setting_win import SaveSettingWin  # 保存設定画面ウィンドウクラス
from package.window.shooting_setting_win import ShootingSettingWin  # 撮影設定画面ウィンドウクラス
from package.window.theme_setting_win import ThemeSettingWin  # テーマ設定画面ウィンドウクラス
from package.window.user_info_win import UserInfoWin  # 利用者情報画面ウィンドウクラス


from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス

# ユーザ設定のインスタンス化
user_setting = UserSetting()

Fn.time_log("システム開始")

# メインウィンドウの処理
transition_target_win = "TranslationWin"  # 遷移先ウィンドウ名
win_class = globals()[transition_target_win]  # 遷移先ウィンドウクラスの取得
win_instance = win_class()  # ウィンドウ作成
transition_target_win = win_instance.get_transition_target_win()  # 遷移先ウィンドウ名取得

# 遷移先ウィンドウが存在する間、繰り返す
while transition_target_win != None:
    win_class = globals()[transition_target_win]  # 遷移先ウィンドウクラス
    win_instance = win_class()  # ウィンドウ作成
    transition_target_win = win_instance.get_transition_target_win()  # 遷移先ウィンドウ名取得

Fn.time_log("システム終了")
