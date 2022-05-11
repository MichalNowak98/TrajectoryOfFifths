import PySimpleGUI as sg
from layouts import ComparisonGraphLayout, GraphLayout
from chart_display_module.chart_display import generate_trajectory_of_fifths_graph, \
    generate_trajectory_of_fifths_graph_with_directed_axis, \
    generate_music_signature_graph_for_note_class_durations, \
    generate_music_signature_graph_for_note_class_durations_with_directed_axis
from midi_module.midi_analyzer import get_cpms_array_whole_file, get_cpms_array_quarter_notes, get_cpms_array_from_csv,\
    get_note_time_segments_array_quarter_notes, get_cpms_array_and_note_time_segments_array_quarter_notes

GRAPH_SIZE = 900
MARGIN = 250

graph_layout = GraphLayout(GRAPH_SIZE)

sg.theme("GreenMono")
open_file_layout = [
    [
        sg.Text("Choose a file: ")
    ],
    [
        sg.FileBrowse(key='-fileBrowse-', file_types=(("MIDI files", "*.mid"),)),
        sg.InputText("", key='-browsePath-')
    ],
    [
        sg.Checkbox(text='Show Main Directed Axis and Mode Axis', default=True, key='-show_axes-')
    ],
    [
        sg.Text('Number of fragments: '), sg.InputText(size=(34, 110), key='-number_of_fragments-')
    ],
]
option_buttons_layout = [
    [
        sg.Button(button_text='Generate trajectory of fifths', key='-generate_button-'),
        sg.Text('', text_color='red', visible=False, key='-validation_text-')
    ],
]

layout = [
    [
        [sg.Frame('Frame', open_file_layout, key='FRAME')], [sg.Frame('', option_buttons_layout, key='FRAME2')]
    ],
    [
        sg.Frame('', graph_layout.layout, key='FRAME3', visible=True)
    ]
]
window = sg.Window('Trajectory of fifths generator', layout, size=(1600, 1000), finalize=True)


def run_gui():
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == '-generate_button-':
            window['-graph-'].erase()
            midi_path = ''
            show_axes = False
            number_of_fragments = 0
            try:
                midi_path = values['-browsePath-']
                show_axes = values['-show_axes-']
                number_of_fragments = int(values['-number_of_fragments-'])
                if midi_path == '':
                    window.Element('-validation_text-').update('Choose MIDI file', visible=True)
                elif number_of_fragments == '':
                    window.Element('-validation_text-').update('Type number of fragments', visible=True)
                else:
                    window.Element('-validation_text-').update(visible=False)
                    show_trajectory_of_fifths(midi_path, show_axes, number_of_fragments)
            except:
                window.Element('-validation_text-').update('Type correct number of fragments', visible=True)

    window.close()


def show_trajectory_of_fifths(midi_path, show_axes, number_of_fragments):
    midi_cpms, note_time_segments_array = get_cpms_array_and_note_time_segments_array_quarter_notes(midi_path,
                                                                                                    number_of_fragments)
    if show_axes:
        generate_trajectory_of_fifths_graph_with_directed_axis(window[graph_layout.GRAPH_KEY], GRAPH_SIZE, MARGIN,
                                                               midi_cpms, note_time_segments_array)
    else:
        generate_trajectory_of_fifths_graph(window[graph_layout.GRAPH_KEY], GRAPH_SIZE, MARGIN, midi_cpms)

