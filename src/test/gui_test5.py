import PySimpleGUI as sg

# 1. レイアウト
layout = [
    [
        sg.Text(text="数値1", key="-text1-"),
        sg.Input(key="-input1-"),
    ],
    [
        sg.Text(text="数値2", key="-text2-"),
        sg.Input(key="-input2-"),
    ],
    [
        sg.Text(text="数値3", key="-text3-"),
        sg.Input(key="-input3-"),
    ],
    [
        sg.Button("決定", key="-button1-"),
    ],
]

# 2. ウィンドウの生成
window = sg.Window(
    title="Window title",
    layout=layout,
    grab_anywhere=True,
)
window.finalize()

# 3. GUI処理
while True:
    event, values = window.read()
    print(event, values)
    if event is None:
        break
    if event == "-button1-":
        print(values)

window.close()
