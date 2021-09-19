import PySimpleGUI as sg
from chart_display_module.chart_display import generate_graph, generate_music_signature_graph
import os.path
import shutil
import tempfile
import io
from PIL import Image, ImageColor, ImageDraw

GRAPH_SIZE = 500
GRAPH_MIDDLE = GRAPH_SIZE / 2
LINES = 3

if __name__ == '__main__':
    layout = [[sg.Graph(canvas_size=(GRAPH_SIZE, GRAPH_SIZE), graph_bottom_left=(0, 0),
                        graph_top_right=(GRAPH_SIZE, GRAPH_SIZE), background_color='white',
                        enable_events=True, key='graph')],
              [sg.Text('Change circle color to:'), sg.Button('Red'), sg.Button('Blue'), sg.Button('Move')]]

    window = sg.Window('Trajectory of fifths', layout, finalize=True)
    generate_graph(window, GRAPH_SIZE - 50, LINES, [[0, 1], [1, 0], [0.3, 0.4]])

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break
    window.close()
