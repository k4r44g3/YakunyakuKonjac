from main_win import MainWin
from input_win import InputWin  # 入力画面
from output_win import OutputWin  # 出力画面

transition_target_win = "MainWin"  # 遷移先ウィンドウ名
print(globals())
win_class = globals()[transition_target_win] # 遷移先ウィンドウクラス
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
    win_class = globals()[transition_target_win] # 遷移先ウィンドウクラス
    win_instance = win_class()  # ウィンドウ作成
    transition_target_win = win_instance.get_transition_target_win()  # 遷移先ウィンドウ名取得
