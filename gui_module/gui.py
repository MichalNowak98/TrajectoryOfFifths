import PySimpleGUI as sg

frames = 50

sg.theme("DarkBlue")

lay1 = [sg.Button('Butt1', key='-col-', visible=False)]
lay2 = [sg.Button('Butt2', key='-col1-')]

frame_layout = [
    lay1,
    lay2
    ]
layout = [[sg.Frame('Frame', frame_layout, key='FRAME')],
          [sg.Frame('Frame1', frame_layout, key='FRAME1')]]
window = sg.Window('Title', layout, size=(200, 100), finalize=True)

def run_gui():
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == '-col1-':
            print(event, values)
            window['-col1-'].update(visible=False)
            window['-col-'].update(visible=True)

    window.close()