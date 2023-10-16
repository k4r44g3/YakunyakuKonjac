import PySimpleGUI as sg

# 1. レイアウト
layout = (
    [
        [
            sg.Button("押してね", size=(30, 3), key="BUTTON"),
        ],
        [
            # 松竹梅から選択する。初期値'梅'
            sg.Spin(["松", "竹", "梅"], "梅", readonly=False, key="SPIN_1"),
            # range()の返り値をそのまま渡すとバグるのでリストに変換しておく
            sg.Spin(list(range(100)), 0, readonly=False, key="SPIN_2"),
        ],
        [
            # 松竹梅から選択する。初期値'梅'
            sg.Combo(['松', '竹', '梅'], '梅', readonly=True, key='COMBO')
        ],
        [
            sg.Radio('松', 'group_1', True, key='RADIO_MATSU'), 
            sg.Radio('竹', 'group_1', False, key='RADIO_TAKE'), 
            sg.Radio('梅', 'group_1', False, key='RADIO_UME'), 
        ]
    ],
)

# 2. ウィンドウの生成
window = sg.Window(title="Window title", layout=layout)
window.finalize()

# 3. GUI処理
while True:
    event, values = window.read(timeout=None)
    print(event, values)
    if event is None:
        break

window.close()
