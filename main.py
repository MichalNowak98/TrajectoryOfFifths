from chart_display_module.chart_display import generate_trajectory_of_fifths_graph, generate_music_signature_graph
import PySimpleGUI
from midi_module.midi_analyzer import get_cpms_array_whole_file, get_cpms_array_quarter_notes, get_cpms_array_from_csv
from layouts import ComparisonGraphLayout, GraphLayout


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


def show_music_signature():
    graph_layout = GraphLayout(GRAPH_SIZE)
    window = PySimpleGUI.Window('Characteristic point of music signature', graph_layout.layout, finalize=True)
    generate_music_signature_graph(window[graph_layout.GRAPH_KEY], GRAPH_SIZE, MARGIN, SIGNATURE_TEST_ARRAYS[7])
    sustain_window(window)


def show_trajectory_of_fifths():
    graph_layout = GraphLayout(GRAPH_SIZE)
    window = PySimpleGUI.Window('Trajectory of fifths', graph_layout.layout, finalize=True)
    track = "I_Prelude3_8"
    midi_cpms = get_cpms_array_quarter_notes('d:/Studia/Magisterka/Trajektorie/MIDI/{}.mid'.format(track),
                                             NUMBER_OF_CHUNKS)
    generate_trajectory_of_fifths_graph(window[graph_layout.GRAPH_KEY], GRAPH_SIZE, MARGIN, midi_cpms)
    sustain_window(window)


def show_comparison_of_trajectories():
    graph_layout = ComparisonGraphLayout(GRAPH_SIZE)
    window = PySimpleGUI.Window('Comparison of trajectories of fifths', graph_layout.layout, finalize=True)
    track = "I_Prelude3_8"
    midi_cpms = get_cpms_array_quarter_notes('d:/Studia/Magisterka/Trajektorie/MIDI/{}.mid'.format(track),
                                             NUMBER_OF_CHUNKS)
    csv_cpms = get_cpms_array_from_csv(
        'd:/Studia/Magisterka/Trajektorie/CPMS/{}_quarter_note_from-0-to-32_Trajektoria.csv'.format(track))
    generate_trajectory_of_fifths_graph(window[graph_layout.LEFT_GRAPH_KEY], GRAPH_SIZE, MARGIN, midi_cpms)
    generate_trajectory_of_fifths_graph(window[graph_layout.RIGHT_GRAPH_KEY], GRAPH_SIZE, MARGIN, csv_cpms)
    sustain_window(window)


def sustain_window(window):
    while True:
        event, values = window.read()
        print(event, values)
        if event == PySimpleGUI.WIN_CLOSED:
            break
    window.close()


if __name__ == '__main__':
    show_music_signature()







