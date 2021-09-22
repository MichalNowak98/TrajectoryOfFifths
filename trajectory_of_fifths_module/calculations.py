from math import sin, cos, pi, ceil, sqrt, pow
from enum import Enum

# 30 degrees equals ~0.524 in radians
ANGLE_BETWEEN_AXES = pi / 6

MIDI_NOTE_CLASS = {
    0: "C", 1: "Db", 2: "D", 3: "Eb", 4: "E", 5: "F", 6: "Gb", 7: "G", 8: "Ab", 9: "A", 10: "Bb", 11: "B"
}


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


def calculate_cpms(point_table):
    x = 0
    y = 0
    for pitch_class in PitchClass:
        x += point_table[pitch_class.value] * cos(pitch_class.angle())
        y += point_table[pitch_class.value] * sin(pitch_class.angle())
    return x, y


def calculate_cpms_for_note_class_array(note_class_array):
    x = 0
    y = 0
    for pitch_class in PitchClass:
        x += note_class_array[pitch_class.name] * cos(pitch_class.angle())
        y += note_class_array[pitch_class.name] * sin(pitch_class.angle())
    return x, y


def calculate_cpms_array(note_class_arrays):
    cpms_array = []
    for note_class_array in note_class_arrays:
        note_class_array = normalize_note_class_array(note_class_array)
        cpms_array.append(calculate_cpms_for_note_class_array(note_class_array))
    return cpms_array


def normalize_note_class_array(note_class_array):
    max_val = note_class_array[max(note_class_array, key=note_class_array.get)]
    for note_class in note_class_array:
        note_class_array[note_class] = note_class_array[note_class] / max_val
    return note_class_array


def get_note_class(note):
    return MIDI_NOTE_CLASS[note % 12]
