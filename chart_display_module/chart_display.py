from math import sin, cos, ceil, sqrt, pow, pi
from trajectory_of_fifths_module.calculations import PitchClass, calculate_cpms, find_main_axis_signature

LABEL_MARGIN = 1.2
CARET_LENGTH_MULTIPLIER = 0.05
CPMS_FORMATTER = "{0:.2f}"

LINES_WIDTH = 3
VECTORS_WIDTH = 5
POINT_DIAMETER = 30
FONT = ("Arial", 30)
SIGNATURE_COLOR = 'red'


class TrajectoryOfFifthsChart:
    __graph = None
    __graph_size = 0
    __margin = 0
    __unit_length = 0
    __max_line_index = 0
    __main_axis_signature_pitch_class = None

    def __init__(self, graph, graph_size, margin):
        self.__graph = graph
        self.__graph_size = graph_size
        self.__margin = margin

    def generate_music_signature_graph_for_note_class_durations_with_directed_axis(self, note_class_durations, number_of_lines):
        self.generate_music_signature_graph_for_note_class_durations(note_class_durations, number_of_lines)
        self.__main_axis_signature_pitch_class = find_main_axis_signature(note_class_durations)
        x, y = calculate_cpms(note_class_durations)
        self.__calculate_max_line_index([(x, y)])
        if number_of_lines > 0:
            self.__max_line_index = number_of_lines
        self.__calculate_unit_length()
        if self.__main_axis_signature_pitch_class is not None:
            self.__draw_main_directed_axis(self.__main_axis_signature_pitch_class, SIGNATURE_COLOR)
            #self.__draw_mode_axis(self.__main_axis_signature_pitch_class)

    def generate_music_signature_graph_for_note_class_durations(self, note_class_durations, number_of_lines):
        x, y = calculate_cpms(note_class_durations)
        self.__calculate_max_line_index([(x, y)])
        if number_of_lines > 0:
            self.__max_line_index = number_of_lines
        self.__calculate_unit_length()
        self.__generate_graph()

        # CPMS point
        self.__graph.draw_point((x * self.__unit_length, y * self.__unit_length), POINT_DIAMETER, color=SIGNATURE_COLOR)
        self.__graph.draw_text("CPMS " + CPMS_FORMATTER.format(x) + ", " + CPMS_FORMATTER.format(y),
                               (x * self.__unit_length - 20, y * self.__unit_length + 50), color=SIGNATURE_COLOR, font=FONT)

        # vectors
        for pitch_class in PitchClass:
            x, y = self.__calculate_coordinates(pitch_class.angle(), self.__unit_length,
                                                note_class_durations[pitch_class.name])
            if x != 0 or y != 0:
                self.__graph.draw_point((x, y), 7, color=SIGNATURE_COLOR)
                self.__graph.draw_line((0, 0), (x, y), color=SIGNATURE_COLOR, width=LINES_WIDTH)
                self.__draw_caret(pitch_class, x, y, SIGNATURE_COLOR)

    def generate_music_signature_on_trajectory_of_fifths_graph(self, index, number_of_lines, cpms_table, note_time_segments_array, show_axes, points_count_between_vectors, quarter_point_counts, main_axis_pitch_class):
        if show_axes:
            self.__main_axis_signature_pitch_class = find_main_axis_signature(note_time_segments_array[index])
            self.generate_trajectory_of_fifths_graph_with_directed_axis(cpms_table, number_of_lines, points_count_between_vectors,quarter_point_counts, main_axis_pitch_class)
            if self.__main_axis_signature_pitch_class is not None:
                self.__draw_main_directed_axis(self.__main_axis_signature_pitch_class, SIGNATURE_COLOR)
        else:
            self.generate_trajectory_of_fifths_graph(cpms_table, number_of_lines, points_count_between_vectors, quarter_point_counts)
        note_class_durations = note_time_segments_array[index]
        x, y = calculate_cpms(note_class_durations)
        self.__graph.draw_point((x * self.__unit_length, y * self.__unit_length), POINT_DIAMETER, color=SIGNATURE_COLOR)
        self.__graph.draw_text("CPMS " + CPMS_FORMATTER.format(x) + ", " + CPMS_FORMATTER.format(y),
                               (x * self.__unit_length - 20, y * self.__unit_length + 50), color=SIGNATURE_COLOR,
                               font=FONT)

        # vectors
        for pitch_class in PitchClass:
            x, y = self.__calculate_coordinates(pitch_class.angle(), self.__unit_length,
                                                note_class_durations[pitch_class.name])
            if x != 0 or y != 0:
                self.__graph.draw_point((x, y), 7, color=SIGNATURE_COLOR)
                self.__graph.draw_line((0, 0), (x, y), color=SIGNATURE_COLOR, width=LINES_WIDTH)
                self.__draw_caret(pitch_class, x, y, SIGNATURE_COLOR)

    def generate_trajectory_of_fifths_graph_with_directed_axis(self, cpms_table, number_of_lines, points_count_between_vectors, quarter_point_counts, main_axis_pith_class):
        self.__calculate_max_line_index(cpms_table)
        if number_of_lines > 0:
            self.__max_line_index = number_of_lines
        self.__calculate_unit_length()
        self.__generate_graph()
        self.__draw_main_directed_axis(main_axis_pith_class, 'blue')
        self.__draw_mode_axis(main_axis_pith_class)
        self.__draw_trajectory(cpms_table, points_count_between_vectors, quarter_point_counts, main_axis_pith_class)

    def generate_trajectory_of_fifths_graph(self, cpms_table, number_of_lines, points_count_between_vectors, quarter_point_counts):
        self.__calculate_max_line_index(cpms_table)
        if number_of_lines > 0:
            self.__max_line_index = number_of_lines
        self.__calculate_unit_length()
        self.__generate_graph()
        self.__draw_trajectory(cpms_table, points_count_between_vectors, quarter_point_counts, None)

    def __generate_graph(self):
        # lines and legend
        for pitch_class in PitchClass:
            x, y = self.__calculate_coordinates(pitch_class.angle(), self.__unit_length, self.__max_line_index)
            self.__graph.draw_text(pitch_class.label(), (x * LABEL_MARGIN, y * LABEL_MARGIN), font=FONT)
            self.__graph.draw_line((0, 0), (x, y), color='grey70', width=LINES_WIDTH)
        # circles
        for i in range(self.__max_line_index):
            self.__graph.draw_circle((0, 0), self.__unit_length * (i + 1), line_width=LINES_WIDTH)

    def __draw_trajectory(self, cpms_table, points_count_between_vectors, quarter_point_counts, main_axis_pitch_class):
        # points and lines between them
        for point in range(len(cpms_table)):
            x = cpms_table[point][0] * self.__unit_length
            y = cpms_table[point][1] * self.__unit_length
            previous_x = cpms_table[point - 1][0] * self.__unit_length
            previous_y = cpms_table[point - 1][1] * self.__unit_length
            self.__graph.draw_point((x, y), POINT_DIAMETER, color='blue')
            if point != 0:
                self.__graph.draw_line((previous_x, previous_y), (x, y), color='blue', width=LINES_WIDTH)
        for pitch_class in PitchClass:
            x, y = self.__calculate_coordinates(pitch_class.angle() + pi / 12, self.__unit_length, self.__max_line_index)
            self.__graph.draw_text(points_count_between_vectors[pitch_class.value], (x * LABEL_MARGIN, y * LABEL_MARGIN), font=FONT, color='orange')
        if main_axis_pitch_class is not None:
            x, y = self.__calculate_coordinates(main_axis_pitch_class.angle() - 1.5 * pi / 6, self.__unit_length, self.__max_line_index)
            self.__graph.draw_text(quarter_point_counts[0], (x * LABEL_MARGIN * 1.1, y * LABEL_MARGIN * 1.1), font=FONT, color='red')
            x, y = self.__calculate_coordinates(main_axis_pitch_class.angle() - 4.5 * pi / 6, self.__unit_length, self.__max_line_index)
            self.__graph.draw_text(quarter_point_counts[1], (x * LABEL_MARGIN * 1.1, y * LABEL_MARGIN * 1.1), font=FONT, color='red')
            #
            #
            #
            #

    def __draw_main_directed_axis(self, main_axis_pith_class, color):
        x1, y1 = self.__calculate_coordinates(main_axis_pith_class.angle(), self.__unit_length,
                                              self.__max_line_index)
        x2, y2 = self.__calculate_coordinates(
            PitchClass.class_for_index(main_axis_pith_class.value + 6).angle(), self.__unit_length,
            self.__max_line_index)
        self.__draw_dashed_line(x1, y1, x2, y2, 30, color)
        self.__draw_caret(main_axis_pith_class, x1, y1, color)

    def __draw_caret(self, pitch_class, x, y, color):
        line_length = self.__calculate_line_length([0, 0], [x, y])
        caret_line_angle_diff = 0.025 * (self.__unit_length * self.__max_line_index / line_length)
        x1, y1 = self.__calculate_coordinates(
            pitch_class.angle() + caret_line_angle_diff, line_length - 30, 1
        )
        x2, y2 = self.__calculate_coordinates(
            pitch_class.angle() - caret_line_angle_diff, line_length - 30, 1
        )
        self.__graph.draw_line((x1, y1), (x, y), color=color, width=VECTORS_WIDTH)
        self.__graph.draw_line((x2, y2), (x, y), color=color, width=VECTORS_WIDTH)

    def __draw_dashed_line(self, x1, y1, x2, y2, number_of_dashes, color):
        for i in range(0, number_of_dashes, 2):
            self.__graph.draw_line((x1 / number_of_dashes * i, y1 / number_of_dashes * i),
                                   (x1 / number_of_dashes * (i + 1), y1 / number_of_dashes * (i + 1)), color=color,
                                   width=VECTORS_WIDTH)
            self.__graph.draw_line((x2 / number_of_dashes * i, y2 / number_of_dashes * i),
                                   (x2 / number_of_dashes * (i + 1), y2 / number_of_dashes * (i + 1)), color=color,
                                   width=VECTORS_WIDTH)

    def __draw_mode_axis(self, main_axis_pith_class):
        mode_axis_pitch_class = PitchClass.class_for_index(main_axis_pith_class.value - 3)
        x, y = self.__calculate_coordinates(mode_axis_pitch_class.angle(), self.__unit_length, self.__max_line_index)
        self.__draw_dashed_line(0, 0, x, y, 20, 'green')
        self.__draw_caret(mode_axis_pitch_class, x, y, 'green')

    @staticmethod
    def __calculate_line_length(starting_point, ending_point):
        a = starting_point[0] - ending_point[0]
        b = starting_point[1] - ending_point[1]
        return sqrt(pow(a, 2) + pow(b, 2))

    @staticmethod
    def __calculate_coordinates(angle, unit_length, value_multiplier):
        return (cos(angle) * unit_length * value_multiplier,
                sin(angle) * unit_length * value_multiplier)

    def __calculate_unit_length(self):
        # reducing unit length by margin to make space for legend
        self.__unit_length = (self.__graph_size - self.__margin) / self.__max_line_index

    def __calculate_max_line_index(self, point_table):
        self.__max_line_index = 0
        for point in point_table:
            self.__max_line_index = max(1, self.__max_line_index,
                                        ceil(self.__calculate_line_length((0, 0), (point[0], point[1]))))
