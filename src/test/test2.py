import PySimpleGUI as sg
import time


def blink_thread(window):
    """
    A worker thread that communicates with the GUI through a queue
    This thread can block for as long as it wants and the GUI will not be affected
    :param window: (sg.Window) the window to communicate with
    """
    while True:
        time.sleep(2)  # sleep for a while
        window.write_event_value(('-THREAD-', 'LED ON'), 'LED ON')
        time.sleep(2)  # sleep for a while
        window.write_event_value(('-THREAD-', 'LED OFF'), 'LED OFF')


def main():
    """
    Starts and executes the GUI
    Reads data from a Queue and displays the data to the window
    Returns when the user exits / closes the window
    """

    layout = [[sg.Text('Blinking LED Simulation')],
              [sg.Text('*', text_color='red', key='-LED-', font='_ 25')],
              [sg.Text(key='-MESSAGE-')],
              [sg.Button('Start'), sg.Button('Exit')], ]

    window = sg.Window('Blinking LED Window', layout)

    # --------------------- EVENT LOOP ---------------------
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        window['-MESSAGE-'].update(f'{event}')
        if event == 'Start':
            window.start_thread(lambda: blink_thread(window), ('-THREAD-', '-THEAD ENDED-'))
        elif event == 'Click Me':
            print('Your GUI is alive and well')
        elif event[0] == '-THREAD-':
            if event [1] == 'LED ON':
                window['-LED-'].update('*')
            elif event [1] == 'LED OFF':
                window['-LED-'].update(' ')

    # if user exits the window, then close the window and exit the GUI func
    window.close()


if __name__ == '__main__':
    main()
