import PySimpleGUI as sg
import webbrowser

def open_url(url):
    webbrowser.open(url, new=2)  # 新しいタブでURLを開く

layout = [
    [sg.Text('Webページを開くボタン')],
    [sg.Button('Googleを開く', key='Open_Google')],
    [sg.Button('終了')]
]

window = sg.Window('Webページオープナー', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == '終了':
        break
    elif event == 'Open_Google':
        open_url('https://www.google.com')

window.close()