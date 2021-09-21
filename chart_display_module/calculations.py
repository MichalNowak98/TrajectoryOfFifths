from math import sin, cos, pi, ceil, sqrt, pow
from enum import Enum

# 30 degrees equals ~0.524 in radians
ANGLE_BETWEEN_AXES = pi / 6


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
        return ANGLE_BETWEEN_AXES * self.value


def calculate_line_length(starting_point, ending_point):
    a = starting_point[0] - ending_point[0]
    b = starting_point[1] - ending_point[1]
    return sqrt(pow(a, 2) + pow(b, 2))


def calculate_coordinates(angle, unit_length, value_multiplier):
    return (cos(angle) * unit_length * value_multiplier,
            sin(angle) * unit_length * value_multiplier)


def calculate_unit_length(graph_size, margin, number_of_lines):
    # reducing unit length by margin to make space for legend
    unit_length = (graph_size - margin) / number_of_lines
    return unit_length


def calculate_max_line_index(point_table):
    max_line_index = 0
    for point in point_table:
        ll = calculate_line_length((0, 0), (point[0], point[1]))
        max_line_index = max(max_line_index, ceil(calculate_line_length((0, 0), (point[0], point[1]))))
        return max_line_index


def calculate_cpms(point_table):
    x = 0
    y = 0
    for pitch_class in PitchClass:
        x += point_table[pitch_class.value] * cos(pitch_class.angle())
        y += point_table[pitch_class.value] * sin(pitch_class.angle())
    return x, y
