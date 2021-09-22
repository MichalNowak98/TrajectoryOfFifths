from mido import MidiFile
from trajectory_of_fifths_module.calculations import get_note_class, calculate_cpms_array


def get_cpms_array(name, number_of_chunks):
    mid = MidiFile(name, clip=True)
    notes_on, notes_off, time = get_on_and_off_note_arrays_and_time(mid)
    pitch_class_arrays = get_note_class_arrays(notes_on, notes_off, time, number_of_chunks)
    cpms_array = calculate_cpms_array(pitch_class_arrays)
    return cpms_array


def get_on_and_off_note_arrays_and_time(mid):
    time = 0
    notes_on = list()
    notes_off = list()
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for msg in track:
            time += msg.time
            if msg.type == 'note_on':
                notes_on.append((get_note_class(msg.note), time))
            elif msg.type == 'note_off':
                notes_off.append((get_note_class(msg.note), time))
    return notes_on, notes_off, time


def get_note_class_arrays(notes_on, notes_off, time, n):
    note_class_arrays = []
    time_per_chunk = float(notes_off[-1][1] - notes_on[0][1]) / n
    for i in range(n):
        note_class_arrays.append({
            "A": 0, "D": 0, "G": 0, "C": 0, "F": 0, "Bb": 0, "Eb": 0, "Ab": 0, "Db": 0, "Gb": 0, "B": 0, "E": 0
        })
        time = 0
        while time < time_per_chunk:
            if len(notes_on) == 0:
                break
            j = 0
            while notes_on[0][0] != notes_off[j][0]:
                j = j + 1
            time_on = notes_off[j][1] - notes_on[0][1]
            if time_on + time > time_per_chunk:
                remaining_time = time_per_chunk - time
                notes_on[0] = (notes_on[0][0], notes_on[0][1] + remaining_time)
                note_class_arrays[i][notes_on[0][0]] += remaining_time
                time += remaining_time
            else:
                note_class_arrays[i][notes_on[0][0]] += time_on
                del notes_on[0]
                del notes_off[j]
                time += time_on
    return note_class_arrays
