from math import sin, cos

LEGEND = ["C", "G", "D", "A", "E", "B", "Gb", "Db", "Ab", "Eb", "Bb", "F"]


def generate_graph(window, graph_size, number_of_lines, point_table):
    graph_middle = graph_size / 2 + 25
    graph = window['graph']  # type: sg.Graph
    unit_length = graph_size / number_of_lines / 2
    # lines and legend
    for i in range(12):
        # 30 degrees equals ~0.524 in radians
        x = sin(0.524 * i) * unit_length * number_of_lines
        y = cos(0.524 * i) * unit_length * number_of_lines
        graph.draw_text(LEGEND[i], (graph_middle + x * 1.05, graph_middle + y * 1.05))
        graph.draw_line((graph_middle, graph_middle), (graph_middle + x, graph_middle + y), color='grey70')
    # circles
    for i in range(number_of_lines):
        graph.draw_circle((graph_middle, graph_middle), unit_length * (i + 1))
    # points
    for point in point_table:
        x = graph_middle + point[0] * unit_length
        y = graph_middle + point[1] * unit_length
        graph.draw_point((x, y), 5, color='green')


def generate_music_signature_graph(window, graph_size, point_table):
    generate_graph(window, graph_size, 1)
