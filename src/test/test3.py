import PySimpleGUI as sg
import time

# My function that takes a long time to do...
def my_long_operation(i):
    time.sleep(10)
    return i * 2


def main():
    layout = [  [sg.Text('My Window')],
                [sg.Button('Go'), sg.Button('Threaded')]  ]

    window = sg.Window('Window Title', layout, keep_on_top=True)

    while True:
        event, values = window.read(timeout=1000)
        if event == sg.WIN_CLOSED:
            break
        
        print(event,values)
        if event == 'Go':
            print("長時間処理開始")
            out=my_long_operation(1)
            print(out)
            print("長時間処理終了")
        elif event  == 'Threaded':
            print("長時間処理開始")
            window.perform_long_operation(lambda: my_long_operation(1), '-fn_end-')
        elif event  == '-fn_end-':
            print(values)
            print("長時間処理終了")

        elif event == "__TIMEOUT__":
            print("time_out")

    window.close()

if __name__ == '__main__':
    main()

