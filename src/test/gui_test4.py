import PySimpleGUI as sg

layout = [
    [sg.pin(sg.Text("このテキストは切り替わります", key='-TEXT-'))],  # sg.pin()を使用して囲む
    [sg.Button("表示/非表示")]
]

window = sg.Window("テキストの表示・非表示デモ", layout)

text_visible = True

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == "表示/非表示":
        text_visible = not text_visible
        window['-TEXT-'].update(visible=text_visible)

window.close()
