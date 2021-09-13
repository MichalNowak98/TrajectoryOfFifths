import PySimpleGUI as sg
import os.path


if __name__ == '__main__':
    window_layout = [
        [
            sg.Text("MIDI file folder"),
            sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
            sg.FileBrowse(size=(10, 1), file_types=(("MIDI files", "*.mid"),))
        ], [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 20),
                key="-FILE LIST-"
            )
        ]
    ]
    window = sg.Window(title="Trajectory of Fifths", layout=window_layout, margins=(600, 300))

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
