from math import sin, cos, pi

LEGEND = ["C", "G", "D", "A", "E", "B", "Gb", "Db", "Ab", "Eb", "Bb", "F"]
# 30 degrees equals ~0.524 in radians
ANGLE = pi / 6
LABEL_MARGIN = 1.05


def calculate_middle_and_unit_length(graph_size, margin, number_of_lines):
    graph_middle = graph_size / 2
    # reducing unit length by margin to make space for legend
    unit_length = (graph_size - margin) / number_of_lines / 2
    return graph_middle, unit_length


def generate_graph(graph, graph_size, margin, graph_middle, unit_length, number_of_lines):
    # lines and legend
    for i in range(12):
        x = sin(ANGLE * i) * unit_length * number_of_lines
        y = cos(ANGLE * i) * unit_length * number_of_lines
        graph.draw_text(LEGEND[i], (graph_middle + x * LABEL_MARGIN, graph_middle + y * LABEL_MARGIN))
        graph.draw_line((graph_middle, graph_middle), (graph_middle + x, graph_middle + y), color='grey70')
    # circles
    for i in range(number_of_lines):
        graph.draw_circle((graph_middle, graph_middle), unit_length * (i + 1))


def generate_music_signature_graph(graph, graph_size, margin, point_table):
    graph_middle, unit_length = calculate_middle_and_unit_length(graph_size, margin, 1)
    generate_graph(graph, graph_size, margin, graph_middle, unit_length, 1)
    # points
    for point in point_table:
        x = graph_middle + point[0] * unit_length
        y = graph_middle + point[1] * unit_length
        graph.draw_point((x, y), 5, color='green')

def generate_trajectory_of_fifths_graph(graph, graph_size, margin, point_table, number_of_lines):
    graph_middle, unit_length = calculate_middle_and_unit_length(graph_size, margin, number_of_lines)
    generate_graph(graph, graph_size, margin, graph_middle, unit_length, number_of_lines)
    # points
    for point in point_table:
        x = graph_middle + point[0] * unit_length
        y = graph_middle + point[1] * unit_length
        graph.draw_point((x, y), 5, color='green')
