import PySimpleGUI as sg
import time


# My function that takes a long time to do...
def my_long_operation(id):
    time.sleep(10)
    return id


def main():
    layout = [
        [sg.Text("My Window")],
        [sg.Input(key="-IN-")],
        [sg.Text(key="-OUT-")],
        [sg.Button("Threaded"), sg.Button("cancel")],
    ]

    window = sg.Window("Window Title", layout, keep_on_top=True)

    thread_dict = {}
    thread_count = 0
    while True:  # Event Loop
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == "Threaded":
            # Let PySimpleGUI do the threading for you...
            id = thread_count
            thread_id = window.start_thread(
                lambda: my_long_operation(id), "-end-"
            )
            thread_dict[id] = thread_id
            print(thread_dict)
            thread_count += 1
        elif event == "-end-":
            print(values["-end-"])
            thread_dict.pop(values["-end-"])
            print(thread_dict)
        elif event == "cansel":
            pass

    window.close()


if __name__ == "__main__":
    main()
