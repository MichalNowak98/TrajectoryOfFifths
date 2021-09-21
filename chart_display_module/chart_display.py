from math import sin, cos, pi
from enum import Enum


class PitchClass(Enum):
    A = 0
    D = 1
    G = 2
    C = 3
    F = 4
    Bb = 5
    Eb = 6
    Ab = 7
    Db = 8
    Gb = 9
    B = 10
    E = 11

    def angle(self):
        return - ANGLE_BETWEEN_AXES * self.value + ANGLE_MARGIN


# 30 degrees equals ~0.524 in radians
ANGLE_BETWEEN_AXES = pi / 6
# added to angle to start from A note
ANGLE_MARGIN = pi/2
LABEL_MARGIN = 1.05


def calculate_unit_length(graph_size, margin, number_of_lines):
    # reducing unit length by margin to make space for legend
    unit_length = (graph_size - margin) / number_of_lines
    return unit_length


def count_coordinates(angle, unit_length, value_multiplier):
    return (sin(angle) * unit_length * value_multiplier,
            cos(angle) * unit_length * value_multiplier)


def generate_graph(graph, graph_size, margin, unit_length, number_of_lines):
    # lines and legend
    for pitch_class in PitchClass:
        x, y = count_coordinates(pitch_class.angle(), unit_length, number_of_lines)
        graph.draw_text(pitch_class.name, (x * LABEL_MARGIN, y * LABEL_MARGIN))
        graph.draw_line((0, 0), (x, y), color='grey70')
    # circles
    for i in range(number_of_lines):
        graph.draw_circle((0, 0), unit_length * (i + 1))


def generate_music_signature_graph(graph, graph_size, margin, point_table):
    unit_length = calculate_unit_length(graph_size, margin, 1)
    generate_graph(graph, graph_size, margin, unit_length, 1)
    # points
    for pitch_class in PitchClass:
        x, y = count_coordinates(pitch_class.angle(), unit_length, point_table[pitch_class.value])
        graph.draw_point((x, y), 5, color='green')
        graph.draw_line((0, 0), (x, y), color='green')


def generate_trajectory_of_fifths_graph(graph, graph_size, margin, point_table, number_of_lines):
    unit_length = calculate_unit_length(graph_size, margin, number_of_lines)
    generate_graph(graph, graph_size, margin, unit_length, number_of_lines)
    # points
    for point in point_table:
        x = point[0] * unit_length
        y = point[1] * unit_length
        graph.draw_point((x, y), 5, color='green')
