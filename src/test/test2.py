import PySimpleGUI as sg

# ウィンドウの内容を定義
layout = [
    [sg.Text("スクロールバーの位置を取得")],
    [sg.Column([[sg.Text(f"行 {i}") for i in range(100)]], scrollable=True, key="-COLUMN-")],
    [sg.Button("位置取得"), sg.Button("終了")],
]

# ウィンドウを作成
window = sg.Window("ウィンドウタイトル", layout)

# イベントループ
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "終了":
        break
    if event == "位置取得":
        column_element = window["-COLUMN-"]
        # Canvasウィジェットにアクセスしてyviewメソッドを呼び出す
        try:
            #
            scrollbar_pos = column_element.Widget.canvas.xview()
            print("スクロールバーの位置:", scrollbar_pos)
        except AttributeError as e:
            print("スクロールバーの位置を取得できませんでした。", e)

# ウィンドウを閉じる
window.close()
