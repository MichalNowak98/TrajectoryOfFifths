from mido import MidiFile
from trajectory_of_fifths_module.calculations import get_note_class, calculate_cpms_array
import csv
from locale import atof, setlocale, LC_NUMERIC
setlocale(LC_NUMERIC, 'French_Canada.1252')

def get_cpms_array(name, number_of_chunks):
    mid = MidiFile(name, clip=True)
    print(mid)
    note_time_segments_array, time = get_note_time_segments_array_and_time(mid)
    note_class_duration_array = get_note_class_duration_array(note_time_segments_array, time, number_of_chunks)
    cpms_array = calculate_cpms_array(note_class_duration_array)
    return cpms_array


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
        for msg in track:
            time += msg.time
            if msg.type == 'note_on':
                # time before first note_on is not important
                if first_note_on_msg:
                    notes_on.append({"note": msg.note, "channel": msg.channel, "time": 0})
                    time = 0
                    first_note_on_msg = False
                else:
                    notes_on.append({"note": msg.note, "channel": msg.channel, "time": time})
            elif msg.type == 'note_off':
                for note_index in range(len(notes_on)):
                    if notes_on[note_index]["note"] == msg.note and notes_on[note_index]["channel"] == msg.channel:
                        note_time_segments_array[get_note_class(msg.note)].append((notes_on[note_index]["time"], time))
                        del notes_on[note_index]
                        break
    return note_time_segments_array, time


def get_note_class_duration_array(note_time_segments_array, time, n):
    note_class_duration_array = []
    time_per_chunk = float(time) / n
    for chunk_index in range(n):
        note_class_duration_array.append({
            "A": 0, "D": 0, "G": 0, "C": 0, "F": 0, "Bb": 0, "Eb": 0, "Ab": 0, "Db": 0, "Gb": 0, "B": 0, "E": 0
        })
        chunk_time_range = (chunk_index * time_per_chunk, (chunk_index + 1) * time_per_chunk)
        for note_class in note_time_segments_array:
            for time_segment in note_time_segments_array[note_class]:
                x = note_class_duration_array[chunk_index][note_class]
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


 # while time < time_per_chunk:
        #     if len(notes_on) == 0:
        #         break
        #     notes_on_number = 1
        #     while notes_on[notes_on_last_index][1] == 0:
        #         notes_on_last_index = notes_on_last_index + 1
        #         note_off_index = 0
        #         #while
        #
        #     for note_off_index in range(notes_on_last_index):
        #
        #         for note_on_index in range(notes_on_last_index):
        #             if notes_on[note_on_index][0] == notes_off[note_off_index][0]:
        #                 time_on = notes_off[note_off_index][1] - notes_on[note_on_index][1]
        #                 del notes_on[note_on_index]
        #                 del notes_off[note_off_index]







            # time_on = notes_off[j][1] - notes_on[0][1]
            # if time_on + time > time_per_chunk:
            #     remaining_time = time_per_chunk - time
            #     notes_on[0] = (notes_on[0][0], notes_on[0][1] + remaining_time)
            #     note_class_arrays[i][notes_on[0][0]] += remaining_time
            #     time += remaining_time
            # else:
            #     note_class_arrays[i][notes_on[0][0]] += time_on
            #     del notes_on[0]
            #     del notes_off[j]
            #     time += time_on