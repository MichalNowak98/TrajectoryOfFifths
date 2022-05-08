from mido import MidiFile
from trajectory_of_fifths_module.calculations import get_note_class, calculate_cpms_array
import csv
from locale import atof, setlocale, LC_NUMERIC
setlocale(LC_NUMERIC, 'French_Canada.1252')


def get_cpms_array(note_time_segments_array, time_per_chunk, number_of_chunks):
    note_class_duration_array = get_note_class_duration_array(note_time_segments_array, time_per_chunk, number_of_chunks)
    cpms_array = calculate_cpms_array(note_class_duration_array)
    return cpms_array


def get_cpms_array_quarter_notes(name, number_of_chunks):
    mid = MidiFile(name, clip=True)
    print(mid)
    note_time_segments_array, time = get_note_time_segments_array_and_time(mid)
    return get_cpms_array(note_time_segments_array, mid.ticks_per_beat, number_of_chunks)


def get_note_time_segments_array_quarter_notes(name, number_of_chunks):
    mid = MidiFile(name, clip=True)
    print(mid)
    note_time_segments_array, time = get_note_time_segments_array_and_time(mid)
    note_class_duration_array = get_note_class_duration_array(note_time_segments_array, mid.ticks_per_beat, number_of_chunks)
    return note_class_duration_array


def get_cpms_array_whole_file(name, number_of_chunks):
    mid = MidiFile(name, clip=True)
    note_time_segments_array, time = get_note_time_segments_array_and_time(mid)
    time_per_chunk = float(time) / number_of_chunks
    return get_cpms_array(note_time_segments_array, time_per_chunk, number_of_chunks)


def get_cpms_array_from_csv(name):
    cpms_array = []
    with open(name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            cpms_array.append((atof(row[0]), atof(row[1])))
    return cpms_array


def get_note_time_segments_array_and_time(mid):
    time = 0
    notes_on = list()
    note_time_segments_array = {
        "A": [], "D": [], "G": [], "C": [], "F": [], "Bb": [], "Eb": [], "Ab": [], "Db": [], "Gb": [], "B": [], "E": []
    }
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        first_note_on_msg = True
        time = 0
        for msg in track:
            time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                # time before first note_on is not important
                if first_note_on_msg:
                    notes_on.append({"note": msg.note, "channel": msg.channel, "time": msg.time})
                    time = msg.time
                    first_note_on_msg = False
                else:
                    notes_on.append({"note": msg.note, "channel": msg.channel, "time": time})
            elif msg.type == 'note_off' or msg.type == 'note_on' and msg.velocity == 0:
                for note_index in range(len(notes_on)):
                    if notes_on[note_index]["note"] == msg.note and notes_on[note_index]["channel"] == msg.channel:
                        note_time_segments_array[get_note_class(msg.note)].append((notes_on[note_index]["time"], time))
                        del notes_on[note_index]
                        break
    return note_time_segments_array, time


def get_note_class_duration_array(note_time_segments_array, time_per_chunk, number_of_chunks):
    note_class_duration_array = []
    time_per_chunk = time_per_chunk
    for chunk_index in range(number_of_chunks):
        note_class_duration_array.append({
            "A": 0, "D": 0, "G": 0, "C": 0, "F": 0, "Bb": 0, "Eb": 0, "Ab": 0, "Db": 0, "Gb": 0, "B": 0, "E": 0
        })
        chunk_time_range = (chunk_index * time_per_chunk, (chunk_index + 1) * time_per_chunk - 1)
        for note_class in note_time_segments_array:
            for time_segment in note_time_segments_array[note_class]:
                note_class_duration_array[chunk_index][note_class] = note_class_duration_array[chunk_index][note_class] + calculate_note_duration_in_chunk(time_segment, chunk_time_range)
    return note_class_duration_array


def calculate_note_duration_in_chunk(time_segment, chunk_time_range):
    if time_segment[0] < chunk_time_range[0]:
        if time_segment[1] > chunk_time_range[0]:
            if time_segment[1] > chunk_time_range[1]:
                return chunk_time_range[1] - chunk_time_range[0]
            else:
                return time_segment[1] - chunk_time_range[0]
        else:
            return 0
    else:
        if time_segment[0] < chunk_time_range[1]:
            if time_segment[1] > chunk_time_range[1]:
                return chunk_time_range[1] - time_segment[0]
            else:
                return time_segment[1] - time_segment[0]
        else:
            return 0
