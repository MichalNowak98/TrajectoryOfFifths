import PySimpleGUI as sg
from chart_display_module.chart_display import generate_trajectory_of_fifths_graph, generate_music_signature_graph

GRAPH_SIZE = 500
MARGIN = 50
GRAPH_MIDDLE = GRAPH_SIZE / 2
SIGNATURE_TEST_ARRAYS = [
    [0.06, 0.5, 1, 0.96, 0.37, 0.06, 0.61, 0.49, 0.21, 0.1, 0.23, 0.1],
    [0, 0, 0.67, 1, 0, 0, 0.33, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
]
TRAJECTORY_TEST_ARRAYS = [
    [(0.32, 1), (-1.12, -1.09), (0.11, 2.1), (1, -3.1)]
]

if __name__ == '__main__':
    layout = [[sg.Graph(canvas_size=(GRAPH_SIZE, GRAPH_SIZE), graph_bottom_left=(-GRAPH_SIZE, -GRAPH_SIZE),
                        graph_top_right=(GRAPH_SIZE, GRAPH_SIZE), background_color='white',
                        enable_events=True, key='graph')]]

    window = sg.Window('Trajectory of fifths', layout, finalize=True)
    generate_trajectory_of_fifths_graph(window['graph'], GRAPH_SIZE, MARGIN, TRAJECTORY_TEST_ARRAYS[0])
    #generate_music_signature_graph(window['graph'], GRAPH_SIZE, MARGIN, SIGNATURE_TEST_ARRAYS[1])

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break
    window.close()
