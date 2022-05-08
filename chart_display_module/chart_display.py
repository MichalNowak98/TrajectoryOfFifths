from chart_display_module.calculations import calculate_coordinates, \
    calculate_unit_length, calculate_max_line_index, calculate_line_length
from trajectory_of_fifths_module.calculations import PitchClass, calculate_cpms, find_main_axis_signature, \
    angle_between_vector_and_x_axis, find_main_axis_trajectory

LABEL_MARGIN = 1.2
CARET_LENGTH_MULTIPLIER = 0.05
CPMS_FORMATTER = "{0:.2f}"

LINES_WIDTH = 3
VECTORS_WIDTH = 5
POINT_DIAMETER = 30
FONT = ("Arial", 30)


def generate_graph(graph, unit_length, number_of_lines):
    # lines and legend
    for pitch_class in PitchClass:
        x, y = calculate_coordinates(pitch_class.angle(), unit_length, number_of_lines)
        graph.draw_text(pitch_class.label(), (x * LABEL_MARGIN, y * LABEL_MARGIN), font=FONT)
        graph.draw_line((0, 0), (x, y), color='grey70', width=LINES_WIDTH)
    # circles
    for i in range(number_of_lines):
        graph.draw_circle((0, 0), unit_length * (i + 1), line_width=LINES_WIDTH)
        graph.draw_text(i + 1, (unit_length * (i + 1) * LABEL_MARGIN, -50), color='grey40', font=FONT)


def generate_music_signature_graph_for_note_class_durations_with_directed_axis(graph, graph_size, margin, note_class_durations):
    generate_music_signature_graph_for_note_class_durations(graph, graph_size, margin, note_class_durations)
    main_axis_pitch_class = find_main_axis_signature(note_class_durations)
    x, y = calculate_cpms(note_class_durations)
    max_line_index = calculate_max_line_index([(x, y)])
    unit_length = calculate_unit_length(graph_size, margin, max_line_index)
    draw_main_directed_axis(graph, main_axis_pitch_class, unit_length, max_line_index)
    draw_mode_axis(graph, main_axis_pitch_class, unit_length, max_line_index)



def generate_music_signature_graph_for_note_class_durations(graph, graph_size, margin, note_class_durations):
    x, y = calculate_cpms(note_class_durations)
    max_line_index = 2

    unit_length = calculate_unit_length(graph_size, margin, max_line_index)
    generate_graph(graph, graph_size, margin, unit_length, max_line_index)

    # CPMS point
    graph.draw_point((x * unit_length, y * unit_length), POINT_DIAMETER, color='red')
    graph.draw_text("CPMS " + CPMS_FORMATTER.format(x) + ", " + CPMS_FORMATTER.format(y),
                    (x * unit_length - 20, y * unit_length + 40), color='red', font=FONT)

    # vectors
    for pitch_class in PitchClass:
        x, y = calculate_coordinates(pitch_class.angle(), unit_length, note_class_durations[pitch_class.value])
        if x != 0 or y != 0:
            graph.draw_point((x, y), 7, color='blue')
            graph.draw_line((0, 0), (x, y), color='blue', width=LINES_WIDTH)
            draw_caret(graph, pitch_class, unit_length, max_line_index, x, y, 'blue')


def generate_music_signature_graph_for_point(graph, graph_size, margin, point):
    x, y = point
    max_line_index = calculate_max_line_index([(x, y)])

    unit_length = calculate_unit_length(graph_size, margin, max_line_index)
    generate_graph(graph, unit_length, max_line_index)

    # CPMS point
    graph.draw_point((x * unit_length, y * unit_length), 10, color='red')
    graph.draw_text("CPMS " + CPMS_FORMATTER.format(x) + ", " + CPMS_FORMATTER.format(y),
                    (x * unit_length + 20, y * unit_length + 40), color='red', font=FONT)

    # vectors
    for pitch_class in PitchClass:
        x, y = calculate_coordinates(pitch_class.angle(), unit_length, note_class_durations[pitch_class.value])
        graph.draw_point((x, y), 7, color='blue')
        graph.draw_line((0, 0), (x, y), color='blue', width=LINES_WIDTH)


def generate_trajectory_of_fifths_graph_with_directed_axis(graph, graph_size, margin, cpms_table):
    max_line_index = calculate_max_line_index(cpms_table)
    unit_length = calculate_unit_length(graph_size, margin, max_line_index)
    generate_graph(graph, unit_length, max_line_index)
    main_axis_pitch_class = find_main_axis_trajectory(cpms_table)
    draw_main_directed_axis(graph, main_axis_pitch_class, unit_length, max_line_index)
    draw_mode_axis(graph, main_axis_pitch_class, unit_length, max_line_index)


def generate_trajectory_of_fifths_graph(graph, graph_size, margin, cpms_table):
    max_line_index = calculate_max_line_index(cpms_table)
    unit_length = calculate_unit_length(graph_size, margin, max_line_index)
    generate_graph(graph, unit_length, max_line_index)

    # points and lines between them
    for point in range(len(cpms_table)):
        x = cpms_table[point][0] * unit_length
        y = cpms_table[point][1] * unit_length
        previous_x = cpms_table[point - 1][0] * unit_length
        previous_y = cpms_table[point - 1][1] * unit_length
        graph.draw_point((x, y), POINT_DIAMETER, color='blue')
        if point != 0:
            graph.draw_line((previous_x, previous_y), (x, y), color='blue', width=LINES_WIDTH)


def draw_main_directed_axis(graph, main_axis_pitch_class, unit_length, number_of_lines):
    x1, y1 = calculate_coordinates(main_axis_pitch_class.angle(), unit_length, number_of_lines)
    x2, y2 = calculate_coordinates(PitchClass.class_for_index(main_axis_pitch_class.value + 6).angle(), unit_length,
                                   number_of_lines)
    draw_dashed_line(graph, x1, y1, x2, y2, 30, 'red')
    draw_caret(graph, main_axis_pitch_class, unit_length, number_of_lines, x1, y1, 'red')
    # draw_main_axis_label(graph, PitchClass.class_for_index(main_axis_pitch_class.value - 1), unit_length,
    #                     number_of_lines)


def draw_main_axis_label(graph, pitch_class, unit_length, number_of_lines):
    x, y = calculate_coordinates(pitch_class.angle(), unit_length, number_of_lines)
    graph.draw_text(pitch_class.name, (x * LABEL_MARGIN, y * LABEL_MARGIN), color='red', font=FONT)


def draw_caret(graph, main_axis_pitch_class, unit_length, number_of_lines, x, y, color):
    line_length = calculate_line_length([0, 0], [x, y])
    caret_line_angle_diff = 0.025 * (unit_length * number_of_lines / line_length)
    if number_of_lines > 1:
        number_of_lines = number_of_lines - 1
    x1, y1 = calculate_coordinates(
        main_axis_pitch_class.angle() + caret_line_angle_diff, number_of_lines - 1 + line_length - 30, number_of_lines
    )
    x2, y2 = calculate_coordinates(
        main_axis_pitch_class.angle() - caret_line_angle_diff, number_of_lines - 1 + line_length - 30, number_of_lines
    )
    graph.draw_line((x1, y1), (x, y), color=color, width=VECTORS_WIDTH)
    graph.draw_line((x2, y2), (x, y), color=color, width=VECTORS_WIDTH)


def draw_dashed_line(graph, x1, y1, x2, y2, number_of_dashes, color):
    for i in range(0, number_of_dashes, 2):
        graph.draw_line((x1 / number_of_dashes * i, y1 / number_of_dashes * i),
                        (x1 / number_of_dashes * (i + 1), y1 / number_of_dashes * (i + 1)), color=color, width=VECTORS_WIDTH)
        graph.draw_line((x2 / number_of_dashes * i, y2 / number_of_dashes * i),
                        (x2 / number_of_dashes * (i + 1), y2 / number_of_dashes * (i + 1)), color=color, width=VECTORS_WIDTH)


def draw_mode_axis(graph, main_axis_pitch_class, unit_length, number_of_lines):
    mode_axis_pitch_class = PitchClass.class_for_index(main_axis_pitch_class.value - 3)
    x, y = calculate_coordinates(mode_axis_pitch_class.angle(), unit_length, number_of_lines)
    draw_dashed_line(graph, 0, 0, x, y, 20, 'green')
    draw_caret(graph, mode_axis_pitch_class, unit_length, number_of_lines, x, y, 'green')
