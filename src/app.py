from package.fn import Fn  # 自作関数クラス

from package.window.translation_win import TranslationWin  # 翻訳画面ウィンドウクラス
from package.window.input_win import InputWin  # 入力画面ウィンドウクラス
from package.window.output_win import OutputWin  # 出力画面ウィンドウクラス

from package.window.output_win import OutputWin  # 出力画面ウィンドウクラス

from package.user_setting import UserSetting  # ユーザーが変更可能の設定クラス

# ユーザ設定のインスタンス化
# user_setting = UserSetting()

# Fn.time_log("システム開始")
# # メインウィンドウの処理

transition_target_win = "TranslationWin"  # 遷移先ウィンドウ名
win_class = globals()[transition_target_win]  # 遷移先ウィンドウクラス
win_instance = win_class()  # ウィンドウ作成
transition_target_win = win_instance.get_transition_target_win()  # 遷移先ウィンドウ名取得

# 遷移先ウィンドウが存在する間、繰り返す
while transition_target_win != None:
    print(
        "現在ウィンドウクラス",
        win_instance,
        "\n遷移先ウィンドウ名",
        transition_target_win,
        "\n遷移先ウィンドウクラス",
        globals()[transition_target_win],
    )
    win_class = globals()[transition_target_win]  # 遷移先ウィンドウクラス
    win_instance = win_class()  # ウィンドウ作成
    transition_target_win = win_instance.get_transition_target_win()  # 遷移先ウィンドウ名取得

Fn.time_log("システム終了")
