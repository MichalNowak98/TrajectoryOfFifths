from chart_display_module.chart_display import generate_trajectory_of_fifths_graph, generate_music_signature_graph
import PySimpleGUI as sg
from midi_module.midi_analyzer import get_cpms_array_whole_file, get_cpms_array_quarter_notes, get_cpms_array_from_csv

NUMBER_OF_CHUNKS = 32
GRAPH_SIZE = 700
MARGIN = 50
GRAPH_MIDDLE = GRAPH_SIZE / 2
SIGNATURE_TEST_ARRAYS = [
    #[A D G C F Bb Es As Ds Gs B E]
    [0.06, 0.5, 1, 0.96, 0.37, 0.06, 0.61, 0.49, 0.21, 0.1, 0.23, 0.1],
    [0, 0, 0.67, 1, 0, 0, 0.33, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0.5, 0, 0, 0.5, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1/3, 2/3, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 1, 0.5, 0, 0, 0, 0, 0, 0, 0, 0.5],
    [0.5, 0, 0, 1, 0.5, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1/5, 2/5, 1, 0, 0, 4/5, 0, 0, 0]
]
TRAJECTORY_TEST_ARRAYS = [
    [(0.32, 1), (-1.12, -1.09), (0.11, 2.1), (1, -3.1)]
]

if __name__ == '__main__':
    track = "I_Prelude22_4"
    midi_cpms = get_cpms_array_quarter_notes('d:/Studia/Magisterka/Trajektorie/MIDI/{}.mid'.format(track), NUMBER_OF_CHUNKS)
    csv_cpms = get_cpms_array_from_csv('d:/Studia/Magisterka/Trajektorie/CPMS/{}_quarter_note_from-0-to-32_Trajektoria.csv'.format(track))

    layout = [
        [
            sg.Graph(canvas_size=(GRAPH_SIZE, GRAPH_SIZE), graph_bottom_left=(-GRAPH_SIZE, -GRAPH_SIZE),
                        graph_top_right=(GRAPH_SIZE, GRAPH_SIZE), background_color='white',
                        enable_events=True, key='cvs_graph'),
            sg.Graph(canvas_size=(GRAPH_SIZE, GRAPH_SIZE),graph_bottom_left=(-GRAPH_SIZE, -GRAPH_SIZE),
                        graph_top_right=(GRAPH_SIZE, GRAPH_SIZE), background_color='white',
                        enable_events=True, key='midi_graph')
        ]
    ]

    window = sg.Window('Trajectory of fifths', layout, finalize=True)
    generate_trajectory_of_fifths_graph(window['cvs_graph'], GRAPH_SIZE, MARGIN, csv_cpms)
    generate_trajectory_of_fifths_graph(window['midi_graph'], GRAPH_SIZE, MARGIN, midi_cpms)
    #generate_music_signature_graph(window['midi_graph'], GRAPH_SIZE, MARGIN, SIGNATURE_TEST_ARRAYS[7])

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break
    window.close()
