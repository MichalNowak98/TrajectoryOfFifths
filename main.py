from chart_display_module.chart_display import generate_trajectory_of_fifths_graph, \
    generate_music_signature_graph_for_note_class_durations, \
    generate_music_signature_graph_for_note_class_durations_with_directed_axis
import PySimpleGUI
from midi_module.midi_analyzer import get_cpms_array_whole_file, get_cpms_array_quarter_notes, get_cpms_array_from_csv,\
    get_note_time_segments_array_quarter_notes
from layouts import ComparisonGraphLayout, GraphLayout


NUMBER_OF_CHUNKS = 32
GRAPH_SIZE = 900
MARGIN = 250
GRAPH_MIDDLE = GRAPH_SIZE / 2
SIGNATURE_TEST_ARRAYS = [
    #[A D G C F Bb Es As Ds Gs B E]
    ###################
    ## first example ##
    ###################
    [0, 0, 2/7, 0, 0, 0, 0, 0, 0, 0, 2/7, 1], #0
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1], #3
    [0.06, 0.5, 1, 0.96, 0.37, 0.06, 0.61, 0.49, 0.21, 0.1, 0.23, 0.1],
    [0, 0, 0.67, 1, 0, 0, 0.33, 0, 0, 0, 0, 0],
    [0, 0, 0.5, 1, 0, 0, 0.5, 0, 0, 0, 0, 0], #6
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0.5, 0, 0, 0.5, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1/3, 2/3, 0, 0, 0, 0, 0, 0, 0, 1], #9
    [0, 0, 1, 0.5, 0, 0, 0, 0, 0, 0, 0, 0.5],
    [0.5, 0, 0, 1, 0.5, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1/5, 2/5, 1, 0, 0, 4/5, 0, 0, 0], #12
    ##########################
    ## nothing else matters ##
    ##########################
    [0, 0, 6/7, 0, 0, 0, 0, 0, 0, 0, 1, 5/7],
    [1/8, 1, 1/8, 1, 0, 0, 0, 0, 0, 1/8, 0, 1/8],
    [0, 1/10, 7/10, 0, 0, 0, 1/10, 0, 0, 1/10, 1, 0], #15
    [0, 0, 2/7, 0, 0, 0, 0, 0, 0, 0, 2/7, 1],
    ####################
    ## Always with me ##
    ####################
    [0, 0, 0, 0, 0, 0, 2/8, 0, 0, 0, 1, 1/8],
    [0, 0, 0, 0, 0, 0, 0, 2/7, 0, 0, 2/7, 1],#18
    [0, 0, 0, 0, 0, 0, 0, 0, 1/8, 1, 2/8, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1/6, 2/6, 2/6, 0],
    [0, 0, 0, 0, 0, 0, 1/6, 2/6, 2/6, 0, 0, 1],#21
    [0, 0, 0, 0, 0, 0, 0, 0, 1/8, 1, 2/8, 0],
    [0, 0, 0, 0, 0, 2/8, 0, 0, 1/8, 1, 2/8, 0],
    ########################
    ## prelude suite no.1 ##
    ########################
    #[A D G C F Bb Es As Ds Gs B E]
    [1, 1/3, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1/3],#24
    [0, 1/3, 1, 0, 0, 0, 0, 0, 0, 1/3, 1, 0],
    [0, 1/3, 1, 0, 0, 0, 0, 0, 1, 1/3, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1/7, 6/7, 0, 2/7], #27
    #####################
    ## prelude d major ##
    #####################
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 1/3, 0, 1/3], #28
    [1/3, 1, 0, 0, 0, 0, 0, 0, 0, 1/3, 0, 1/3],
    [1/3, 1/3, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1/3], #30
    [1/3, 1, 0, 0, 0, 0, 0, 0, 0, 1/3, 0, 1/3],
    [0, 0, 2/3, 0, 0, 0, 0, 0, 0, 1/3, 0, 1],
    [0, 1, 0, 0, 0, 0, 0, 0, 1/3, 0, 2/3, 0], #33
    [1, 0, 1/2, 0, 0, 0, 0, 0, 1/2, 1/2, 0, 1/2],
    [1/2, 0, 1/2, 0, 0, 0, 0, 0, 1, 1/2, 0, 1/2],
]
TRAJECTORY_TEST_ARRAYS = [
    ##########################
    ## nothing else matters ##
    ##########################
    [(0.32, 1), (-1.12, -1.09), (0.11, 2.1), (1, -3.1)],
    [(1.55, -0.48), (1.16, 1.42), (0.84, -0.31), (1.15, -0.50)],
    [(1.15,0),(1.47,0),(0.91,-1),(1.47,0),(1.20,-0.26),(1.03,-0.37),(1.43,-0.75),(0.68,-1.18),]
]
PATHS = [
    'd:/Studia/Magisterka/Trajektorie/MIDI/',
    'd:/Download/'
]
TRACKS = [
    "I_Prelude2_4",
    "Metallica - Nothing Else Matters"
]
CHOSEN_INDEX = 28


def show_music_signature():
    graph_layout = GraphLayout(GRAPH_SIZE)
    window = PySimpleGUI.Window('Characteristic point of music signature', graph_layout.layout, finalize=True)
    generate_music_signature_graph_for_note_class_durations(window[graph_layout.GRAPH_KEY], GRAPH_SIZE, MARGIN, SIGNATURE_TEST_ARRAYS[CHOSEN_INDEX])
    sustain_window(window)


def show_music_signature_with_directed_axis():
    graph_layout = GraphLayout(GRAPH_SIZE)
    window = PySimpleGUI.Window('Characteristic point of music signature', graph_layout.layout, finalize=True)
    generate_music_signature_graph_for_note_class_durations_with_directed_axis(window[graph_layout.GRAPH_KEY], GRAPH_SIZE, MARGIN, SIGNATURE_TEST_ARRAYS[CHOSEN_INDEX])
    sustain_window(window)


def show_trajectory_of_fifths(path):
    graph_layout = GraphLayout(GRAPH_SIZE)
    window = PySimpleGUI.Window('Trajectory of fifths', graph_layout.layout, finalize=True)
    midi_cpms = get_cpms_array_quarter_notes(path, NUMBER_OF_CHUNKS)
    generate_trajectory_of_fifths_graph(window[graph_layout.GRAPH_KEY], GRAPH_SIZE, MARGIN, midi_cpms)
    sustain_window(window)


def show_trajectory_of_fifths_for_array(array):
    graph_layout = GraphLayout(GRAPH_SIZE)
    window = PySimpleGUI.Window('Trajectory of fifths', graph_layout.layout, finalize=True)
    generate_trajectory_of_fifths_graph(window[graph_layout.GRAPH_KEY], GRAPH_SIZE, MARGIN, array)
    sustain_window(window)


def show_cpms_of_trajectory(path, index):
    graph_layout = GraphLayout(GRAPH_SIZE)
    window = PySimpleGUI.Window('Comparison of trajectories of fifths', graph_layout.layout, finalize=True)
    note_time_segments = get_note_time_segments_array_quarter_notes(path, NUMBER_OF_CHUNKS)
    generate_music_signature_graph_for_note_class_durations(window[graph_layout.GRAPH_KEY], GRAPH_SIZE, MARGIN, note_time_segments[index])
    sustain_window(window)


def show_comparison_of_trajectories(track):
    graph_layout = ComparisonGraphLayout(GRAPH_SIZE)
    window = PySimpleGUI.Window('Comparison of trajectories of fifths', graph_layout.layout, finalize=True)
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
    #show_trajectory_of_fifths_for_array(TRAJECTORY_TEST_ARRAYS[1])
    #show_music_signature()
    show_music_signature_with_directed_axis()
    #show_trajectory_of_fifths(PATHS[0] + TRACKS[0] + ".mid")
    #show_cpms_of_trajectory(PATHS[1] + TRACKS[1] + ".mid", 1)
    #show_comparison_of_trajectories()
