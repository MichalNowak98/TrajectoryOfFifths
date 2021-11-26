from chart_display_module.calculations import calculate_coordinates,\
    calculate_unit_length, calculate_max_line_index
from trajectory_of_fifths_module.calculations import PitchClass, calculate_cpms, find_main_axis_signature,\
    angle_between_vector_and_x_axis, find_main_axis_trajectory

LABEL_MARGIN = 1.05
CARET_LENGTH_MULTIPLIER = 0.05
CPMS_FORMATTER = "{0:.2f}"


def generate_graph(graph, graph_size, margin, unit_length, number_of_lines):
    # lines and legend
    for pitch_class in PitchClass:
        x, y = calculate_coordinates(pitch_class.angle(), unit_length, number_of_lines)
        graph.draw_text(pitch_class.label(), (x * LABEL_MARGIN, y * LABEL_MARGIN))
        graph.draw_line((0, 0), (x, y), color='grey70')
    # circles
    for i in range(number_of_lines):
        graph.draw_circle((0, 0), unit_length * (i + 1))
        graph.draw_text(i + 1, (unit_length * (i + 1) * LABEL_MARGIN, -50), color='grey40')


def generate_music_signature_graph(graph, graph_size, margin, note_class_durations):
    x, y = calculate_cpms(note_class_durations)
    max_line_index = calculate_max_line_index([(x, y)])
    main_axis_pitch_class = find_main_axis_signature(note_class_durations)

    unit_length = calculate_unit_length(graph_size, margin, max_line_index)
    generate_graph(graph, graph_size, margin, unit_length, max_line_index)

    # CPMS point
    graph.draw_point((x * unit_length, y * unit_length), 10, color='red')
    graph.draw_text("CPMS " + CPMS_FORMATTER.format(x) + ", " + CPMS_FORMATTER.format(y), (x * unit_length * LABEL_MARGIN, y * unit_length * LABEL_MARGIN), color='red')

    # vectors
    for pitch_class in PitchClass:
        x, y = calculate_coordinates(pitch_class.angle(), unit_length, note_class_durations[pitch_class.value])
        graph.draw_point((x, y), 7, color='blue')
        graph.draw_line((0, 0), (x, y), color='blue', width=3)

    draw_main_directed_axis(graph, main_axis_pitch_class, unit_length, max_line_index)


def generate_trajectory_of_fifths_graph(graph, graph_size, margin, cpms_table):
    max_line_index = calculate_max_line_index(cpms_table)
    unit_length = calculate_unit_length(graph_size, margin, max_line_index)
    generate_graph(graph, graph_size, margin, unit_length, max_line_index)
    main_axis_pitch_class = find_main_axis_trajectory(cpms_table)

    # points and lines between them
    for point in range(len(cpms_table)):
        x = cpms_table[point][0] * unit_length
        y = cpms_table[point][1] * unit_length
        previous_x = cpms_table[point - 1][0] * unit_length
        previous_y = cpms_table[point - 1][1] * unit_length
        graph.draw_point((x, y), 5, color='blue')
        if point != 0:
            graph.draw_line((previous_x, previous_y), (x, y), color='blue')

    draw_main_directed_axis(graph, main_axis_pitch_class, unit_length, max_line_index)


def draw_main_directed_axis(graph, main_axis_pitch_class, unit_length, number_of_lines):
    x1, y1 = calculate_coordinates(main_axis_pitch_class.angle(), unit_length, number_of_lines)
    x2, y2 = calculate_coordinates(PitchClass.class_for_index(main_axis_pitch_class.value + 6).angle(), unit_length,
                                   number_of_lines)
    draw_dashed_line(graph, x1, y1, x2, y2, 30)
    draw_caret(graph, main_axis_pitch_class, unit_length, number_of_lines)
    # draw_main_axis_label(graph, PitchClass.class_for_index(main_axis_pitch_class.value - 1), unit_length,
    #                     number_of_lines)


def draw_main_axis_label(graph, pitch_class, unit_length, number_of_lines):
    x, y = calculate_coordinates(pitch_class.angle(), unit_length, number_of_lines)
    graph.draw_text(pitch_class.name, (x * LABEL_MARGIN, y * LABEL_MARGIN), color='red')


def draw_caret(graph, main_axis_pitch_class, unit_length, number_of_lines):
    x, y = calculate_coordinates(main_axis_pitch_class.angle(), unit_length, number_of_lines)
    x1, y1 = calculate_coordinates(main_axis_pitch_class.angle() + 0.05, unit_length*0.9, number_of_lines)
    x2, y2 = calculate_coordinates(main_axis_pitch_class.angle() - 0.05, unit_length*0.9, number_of_lines)
    graph.draw_line((x1, y1), (x, y), color='red', width=3)
    graph.draw_line((x2, y2), (x, y), color='red', width=3)


def draw_dashed_line(graph, x1, y1, x2, y2, number_of_points):
    for i in range(0, number_of_points, 2):
        graph.draw_line((x1 / number_of_points * i, y1 / number_of_points * i),
                        (x1 / number_of_points * (i+1), y1 / number_of_points * (i+1)), color='red', width=3)
        graph.draw_line((x2 / number_of_points * i, y2 / number_of_points * i),
                        (x2 / number_of_points * (i+1), y2 / number_of_points * (i+1)), color='red', width=3)
