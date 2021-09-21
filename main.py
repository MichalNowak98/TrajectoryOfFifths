import PySimpleGUI as sg
from chart_display_module.chart_display import generate_trajectory_of_fifths_graph, generate_music_signature_graph

GRAPH_SIZE = 500
MARGIN = 50
GRAPH_MIDDLE = GRAPH_SIZE / 2
LINES = 3

if __name__ == '__main__':
    layout = [[sg.Graph(canvas_size=(GRAPH_SIZE, GRAPH_SIZE), graph_bottom_left=(-GRAPH_SIZE, -GRAPH_SIZE),
                        graph_top_right=(GRAPH_SIZE, GRAPH_SIZE), background_color='white',
                        enable_events=True, key='graph')]]

    window = sg.Window('Trajectory of fifths', layout, finalize=True)
    #generate_trajectory_of_fifths_graph(window['graph'], GRAPH_SIZE, MARGIN, [[1, 0]], 5)
    generate_music_signature_graph(window['graph'], GRAPH_SIZE, MARGIN, [0.06, 0.5, 1, 0.96, 0.37, 0.06, 0.61, 0.49,
                                                                         0.21, 0.1, 0.23, 0.1])

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break
    window.close()
