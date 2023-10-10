import PySimpleGUI as sg

import os


print(os.path.dirname(__file__) + "/../debug_history/image_after.png")
# 1. レイアウト
layout = [
    [
        sg.Button("押してね", size=(30, 3), key="BUTTON"),
    ],
    [
        sg.Column(
            [
                [
                    sg.Image(
                        filename=os.path.dirname(__file__)
                        + "/../debug_history/resize_image_after.png"
                    )
                ]
            ],
            size=(1000, 1000),
            scrollable=True,
            background_color="#7799dd",
        )
    ],
]

# 2. ウィンドウの生成
window = sg.Window(title="Window title", layout=layout)
window.finalize()

# 3. GUI処理
while True:
    event, values = window.read(timeout=None)
    if event is None:
        break
window.close()
