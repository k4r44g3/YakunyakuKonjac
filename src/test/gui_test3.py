import PySimpleGUI as sg
import keyboard

# 1. レイアウト
layout = [
    [
        sg.Text("キー設定",),
        sg.Button(button_text="a", size=(30, 1), key="-key_text-"),
    ],
]

# 2. ウィンドウの生成
window = sg.Window(
    title="Window title",
    layout=layout,
    grab_anywhere=True,
    #  Trueの場合、キーボードのキー操作がRead呼び出しからイベントとして返されます
    return_keyboard_events=True,
    # no_titlebar=True,
    # disable_close=True,
    # Trueの場合、ウィンドウは画面上のすべての他のウィンドウの上に作成されます。このパラメータを使用して別のパラメータで作成されたウィンドウが下に押しやられる可能性があります
    # keep_on_top=True,
    use_custom_titlebar=True,
    # Trueの場合、ウィンドウは「X」をクリックして閉じられません。代わりに、window.readからWINDOW_CLOSE_ATTEMPTED_EVENTが返されます
    # enable_close_attempted_event = True
)
window.finalize()

key_code = "a"
is_key_input_waiting_state = False
# 3. GUI処理
while True:
    event, values = window.read(timeout=None)

    if event is None:
        break
    elif event == "-key_text-":
        is_key_input_waiting_state = True
        window["-key_text-"].update(text="何かキーを押してください")
    elif is_key_input_waiting_state:
        is_key_input_waiting_state = False
        key_code = event
        window["-key_text-"].update(text=key_code)

    elif event == key_code:
        print("処理")

window.close()
