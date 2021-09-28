from chart_display_module.calculations import calculate_coordinates,\
    calculate_unit_length, calculate_max_line_index
from trajectory_of_fifths_module.calculations import PitchClass, calculate_cpms

LABEL_MARGIN = 1.05
CPMS_FORMATTER = "{0:.2f}"


def generate_graph(graph, graph_size, margin, unit_length, number_of_lines):
    # lines and legend
    for pitch_class in PitchClass:
        x, y = calculate_coordinates(pitch_class.angle(), unit_length, number_of_lines)
        graph.draw_text(pitch_class.name, (x * LABEL_MARGIN, y * LABEL_MARGIN))
        graph.draw_line((0, 0), (x, y), color='grey70')
    # circles
    for i in range(number_of_lines):
        graph.draw_circle((0, 0), unit_length * (i + 1))
        graph.draw_text(i + 1, (unit_length * (i + 1) * LABEL_MARGIN, -50), color='grey40')


def generate_music_signature_graph(graph, graph_size, margin, point_table):
    x, y = calculate_cpms(point_table)
    max_line_index = calculate_max_line_index([(x, y)])

    unit_length = calculate_unit_length(graph_size, margin, max_line_index)
    generate_graph(graph, graph_size, margin, unit_length, max_line_index)

    # CMPS point
    graph.draw_point((x * unit_length, y * unit_length), 10, color='red')
    graph.draw_text("CPMS " + CPMS_FORMATTER.format(x) + ", " + CPMS_FORMATTER.format(y), (x * unit_length * LABEL_MARGIN, y * unit_length * LABEL_MARGIN), color='red')

    # vectors
    for pitch_class in PitchClass:
        x, y = calculate_coordinates(pitch_class.angle(), unit_length, point_table[pitch_class.value])
        graph.draw_point((x, y), 7, color='blue')
        graph.draw_line((0, 0), (x, y), color='blue', width=3)


def generate_trajectory_of_fifths_graph(graph, graph_size, margin, point_table):
    max_line_index = calculate_max_line_index(point_table)
    unit_length = calculate_unit_length(graph_size, margin, max_line_index)
    generate_graph(graph, graph_size, margin, unit_length, max_line_index)

    # points and lines between them
    for point in range(len(point_table)):
        x = point_table[point][0] * unit_length
        y = point_table[point][1] * unit_length
        previous_x = point_table[point - 1][0] * unit_length
        previous_y = point_table[point - 1][1] * unit_length
        graph.draw_point((x, y), 5, color='blue')
        if point != 0:
            graph.draw_line((previous_x, previous_y), (x, y), color='blue')
