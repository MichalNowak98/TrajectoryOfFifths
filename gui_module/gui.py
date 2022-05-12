import PySimpleGUI as sg
from layouts import ComparisonGraphLayout, GraphLayout
from chart_display_module.chart_display import generate_trajectory_of_fifths_graph, \
    generate_trajectory_of_fifths_graph_with_directed_axis, \
    generate_music_signature_graph_for_note_class_durations, \
    generate_music_signature_graph_for_note_class_durations_with_directed_axis
from midi_module.midi_analyzer import TrajectoryOfFifthsMidi

GRAPH_SIZE = 900
MARGIN = 250
trajectory = TrajectoryOfFifthsMidi()

graph_layout = GraphLayout(GRAPH_SIZE)
sg.theme("GreenMono")

option_buttons_layout = [

    sg.Button(button_text='Generate trajectory of fifths', key='-generate_button-'),
    sg.Text('', text_color='red', visible=False, key='-trajectory_validation_text-')

]
signature_options_layout = [
    [
        sg.Text('Index of music signature: '),
        sg.InputText("", key='-signature_index-', size=(5, 110))
    ],
    [
        sg.Button(button_text='Show music signature', key='-signature_button-')
    ],
    [
        sg.Button(button_text='Show music signature with directed axis', key='-signature_axis_button-')
    ],
    [
        sg.Text('', text_color='red', visible=False, key='-signature_validation_text-')
    ]
]
signature_options_frame = [
    sg.Frame('Signature options', signature_options_layout, key='-signature_options_frame-', vertical_alignment='top', visible=False)
]
open_file_layout = [
    [
        sg.Text("Choose a MIDI file: ")
    ],
    [
        sg.FileBrowse(key='-fileBrowse-', file_types=(("MIDI files", "*.mid"),)),
        sg.InputText("", key='-browse_path-')
    ],
    [
        sg.Checkbox(text='Show Main Directed Axis and Mode Axis', default=True, key='-show_axes-')
    ],
    [
        sg.Text('Number of fragments: '), sg.InputText(size=(34, 110), key='-number_of_fragments-')
    ],
    option_buttons_layout,
    signature_options_frame,
]

layout = [
    [
        [sg.Frame('Options', open_file_layout, key='FRAME', vertical_alignment='top'),
         sg.Frame('', graph_layout.layout, key='FRAME3', visible=True)]
    ],
    # [
    #     sg.Frame('', graph_layout.layout, key='FRAME3', visible=True)
    # ]
]
window = sg.Window('Trajectory of fifths generator', layout, size=(1400, 900), finalize=True)


def run_gui():
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == '-generate_button-':
            window['-graph-'].erase()
            try:
                midi_path = values['-browse_path-']
                show_axes = values['-show_axes-']
                number_of_fragments = int(values['-number_of_fragments-'])
                if midi_path == '':
                    window.Element('-trajectory_validation_text-').update('Choose MIDI file', visible=True)
                else:
                    window.Element('-trajectory_validation_text-').update(visible=False)
                    show_trajectory_of_fifths_quarter_notes(midi_path, show_axes, number_of_fragments)
                    window.Element('-signature_options_frame-').update(visible=True)
            except ValueError:  # integer cast exception
                window.Element('-trajectory_validation_text-').update('Type correct number of fragments', visible=True)
            except:
                window.Element('-trajectory_validation_text-').update('Type correct name of file', visible=True)
        elif event == '-signature_button-':
            try:
                signature_index = int(values['-signature_index-'])
                maximum_index = len(trajectory.get_note_class_duration_array())
                if 0 < signature_index <= maximum_index:
                    window['-graph-'].erase()
                    window.Element('-signature_validation_text-').update(visible=False)
                    show_music_signature_for_point(signature_index - 1)
                else:
                    window.Element('-signature_validation_text-').update('Signature index range: 1 to {}'.format(maximum_index),
                                                                         visible=True)
            except ValueError:  # integer cast exception
                window.Element('-signature_validation_text-').update('Type correct index of signature', visible=True)
        elif event == '-signature_axis_button-':
            try:
                signature_index = int(values['-signature_index-'])
                maximum_index = len(trajectory.get_note_class_duration_array())
                if 0 < signature_index <= maximum_index:
                    window['-graph-'].erase()
                    window.Element('-signature_validation_text-').update(visible=False)
                    show_music_signature_for_point_with_axis(signature_index - 1)
                else:
                    window.Element('-signature_validation_text-').update('Signature index range: 1 to {}'.format(maximum_index),
                                                                         visible=True)
            except ValueError:  # integer cast exception
                window.Element('-signature_validation_text-').update('Type correct index of signature', visible=True)
    window.close()


def show_trajectory_of_fifths_quarter_notes(midi_path, show_axes, number_of_fragments):
    trajectory.calculate_cpms_array_quarter_notes(midi_path, number_of_fragments)
    if show_axes:
        generate_trajectory_of_fifths_graph_with_directed_axis(window[graph_layout.GRAPH_KEY], GRAPH_SIZE, MARGIN,
                                                               trajectory.get_cpms_array(),
                                                               trajectory.get_note_class_duration_array())
    else:
        generate_trajectory_of_fifths_graph(window[graph_layout.GRAPH_KEY], GRAPH_SIZE, MARGIN,
                                            trajectory.get_cpms_array())


def show_music_signature_for_point(point_index):
    generate_music_signature_graph_for_note_class_durations(window[graph_layout.GRAPH_KEY], GRAPH_SIZE, MARGIN,
                                                            trajectory.get_note_class_durations(point_index))


def show_music_signature_for_point_with_axis(point_index):
    generate_music_signature_graph_for_note_class_durations_with_directed_axis(window[graph_layout.GRAPH_KEY],
                                                                               GRAPH_SIZE, MARGIN,
                                                                               trajectory.get_note_class_durations(
                                                                                   point_index))
