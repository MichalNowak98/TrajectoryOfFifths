from math import sin, cos, pi, ceil, sqrt, pow


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
