from math import sin, cos, pi, ceil, sqrt, pow, acos
from enum import Enum

# 30 degrees equals ~0.524 in radians
ANGLE_BETWEEN_AXES = pi / 6
#♭
MIDI_NOTE_CLASS = {
    0: "C", 1: "Db", 2: "D", 3: "Eb", 4: "E", 5: "F", 6: "Gb", 7: "G", 8: "Ab", 9: "A", 10: "Bb", 11: "B"
}
CIRCLE_DUR_LABELS = [
    "A", "D", "G", "C", "F", "Bb", "Eb", "Ab", "Db", "Gb/F#", "B", "E"
]
CIRCLE_MOLL_LABELS = [
    "f#", "b", "e", "a", "d", "g", "c", "f", "bb", "eb/d#", "g#", "c#"
]


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

    def label(self):
        return CIRCLE_DUR_LABELS[self.value] + " / " + CIRCLE_MOLL_LABELS[self.value]

    def angle(self):
        return ANGLE_BETWEEN_AXES * self.value

    @staticmethod
    def class_for_index(index):
        while index < 0:
            index += 12
        return PitchClass(index % 12)


def calculate_cpms(point_table):
    x = 0
    y = 0
    for pitch_class in PitchClass:
        _x, _y = calculate_coordinates(point_table, pitch_class)
        x += _x
        y += _y
    return x, y


def calculate_coordinates(point_table, pitch_class):
    # x = point_table[pitch_class.name] * cos(pitch_class.angle())
    # y = point_table[pitch_class.name] * sin(pitch_class.angle())
    x = point_table[pitch_class.value] * cos(pitch_class.angle())
    y = point_table[pitch_class.value] * sin(pitch_class.angle())
    return x, y


def calculate_cpms_for_note_class_array(note_class_durations):
    x = 0
    y = 0
    for pitch_class in PitchClass:
        x += note_class_durations[pitch_class.name] * cos(pitch_class.angle())
        y += note_class_durations[pitch_class.name] * sin(pitch_class.angle())
    return x, y


def calculate_cpms_array(note_class_duration_array):
    cpms_array = []
    for note_class_durations in note_class_duration_array:
        note_class_durations = normalize_note_class_array(note_class_durations)
        cpms_array.append(calculate_cpms_for_note_class_array(note_class_durations))
    return cpms_array


def normalize_note_class_array(note_class_durations):
    max_val = note_class_durations[max(note_class_durations, key=note_class_durations.get)]
    if max_val > 0:
        for note_class in note_class_durations:
            note_class_durations[note_class] = note_class_durations[note_class] / max_val
    return note_class_durations


def get_note_class(note):
    return MIDI_NOTE_CLASS[note % 12]


def find_main_axis_signature(note_class_durations):
    main_axe = [0, 0]
    for pitch_class in PitchClass:
        axis = directed_axis_value_signature(pitch_class, note_class_durations)
        if axis > main_axe[0]:
            main_axe = [axis, pitch_class]
    return main_axe[1]


def find_main_axis_trajectory(cpms_table):
    main_axe = [0, 0]
    for pitch_class in PitchClass:
        axis = directed_axis_value_trajectory(pitch_class, cpms_table)
        if axis > main_axe[0]:
            main_axe = [axis, pitch_class]
    return main_axe[1]


def directed_axis_value_trajectory(pitch_class, cpms_table):
    class_angle = pitch_class.angle()
    value = 0
    for cpms in cpms_table:
        angle = angle_between_vector_and_x_axis(cpms[0], cpms[1])
        if class_angle <= pi:
            if angle >= class_angle and angle < class_angle + pi:
                value -= calculate_vector_length(cpms[0], cpms[1])
            else:
                value += calculate_vector_length(cpms[0], cpms[1])
        else:
            if angle >= class_angle or angle < class_angle - pi:
                value -= calculate_vector_length(cpms[0], cpms[1])
            else:
                value += calculate_vector_length(cpms[0], cpms[1])
    return value


def directed_axis_value_signature(pitch_class, note_class_durations):
    value = 0
    for pitch_class_offset in range(1, 6):
        x, y = calculate_coordinates(
            note_class_durations,
            PitchClass.class_for_index(pitch_class.value - pitch_class_offset))
        value += calculate_vector_length(x, y)
        x, y = calculate_coordinates(
            note_class_durations,
            PitchClass.class_for_index(pitch_class.value + pitch_class_offset))
        value -= calculate_vector_length(x, y)
    return value


def calculate_vector_length(x, y):
    return sqrt(pow(x, 2) + pow(y, 2))


def angle_between_vector_and_x_axis(x, y):
    angle = acos((x * 1 + y * 0)/(sqrt(x * x + y * y) * sqrt(1 * 1 + 0 * 0)))
    if y < 0:
        angle = pi + pi - angle
    return angle
