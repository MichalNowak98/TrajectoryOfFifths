from chart_display_module.chart_display import generate_trajectory_of_fifths_graph, generate_music_signature_graph
import PySimpleGUI as sg
from midi_module.midi_analyzer import get_cpms_array_whole_file, get_cpms_array_quarter_notes, get_cpms_array_from_csv

NUMBER_OF_CHUNKS = 32
GRAPH_SIZE = 700
MARGIN = 50
GRAPH_MIDDLE = GRAPH_SIZE / 2
SIGNATURE_TEST_ARRAYS = [
    [0.06, 0.5, 1, 0.96, 0.37, 0.06, 0.61, 0.49, 0.21, 0.1, 0.23, 0.1],
    [0, 0, 0.67, 1, 0, 0, 0.33, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0.5, 0, 0, 0.5, 0, 0, 0, 0, 0, 0, 0]
]
TRAJECTORY_TEST_ARRAYS = [
    [(0.32, 1), (-1.12, -1.09), (0.11, 2.1), (1, -3.1)]
]

if __name__ == '__main__':
    cpms = get_cpms_array_quarter_notes('../../../Download/I_Prelude2_4.mid', NUMBER_OF_CHUNKS)
    #cpms = get_cpms_array_from_csv('../../../Download/I_Prelude2_4_quarter_note_from-0-to-32_Trajektoria.csv')

    layout = [[sg.Graph(canvas_size=(GRAPH_SIZE, GRAPH_SIZE), graph_bottom_left=(-GRAPH_SIZE, -GRAPH_SIZE),
                        graph_top_right=(GRAPH_SIZE, GRAPH_SIZE), background_color='white',
                        enable_events=True, key='graph')]]

    window = sg.Window('Trajectory of fifths', layout, finalize=True)
    generate_trajectory_of_fifths_graph(window['graph'], GRAPH_SIZE, MARGIN, cpms)
    #generate_music_signature_graph(window['graph'], GRAPH_SIZE, MARGIN, SIGNATURE_TEST_ARRAYS[0])

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break
    window.close()
