from mido import MidiFile
from trajectory_of_fifths_module.calculations import calculate_cpms_array, calculate_points_count_between_vectors, \
    calculate_quarter_point_counts, find_main_axis_trajectory, CIRCLE_DUR_LABELS, CIRCLE_MOLL_LABELS, \
    CIRCLE_DUR_LABELS_UTF8, CIRCLE_MOLL_LABELS_UTF8, PitchClass
import csv, os
from locale import atof, setlocale, LC_NUMERIC
from math import ceil

setlocale(LC_NUMERIC, 'French_Canada.1252')
MIDI_NOTE_CLASS = {
    0: "C", 1: "Db", 2: "D", 3: "Eb", 4: "E", 5: "F", 6: "Gb", 7: "G", 8: "Ab", 9: "A", 10: "Bb", 11: "B"
}


class TrajectoryOfFifthsMidi:
    __cpms_array = []
    __note_class_duration_array = []
    __points_count_between_vectors = []
    __quarter_point_counts = []
    __main_axis_pitch_class = None
    __track_name = ""

    def get_cpms_array(self):
        return self.__cpms_array

    def get_note_class_duration_array(self):
        return self.__note_class_duration_array

    def get_note_class_durations(self, index):
        return self.__note_class_duration_array[index]

    def get_points_count_between_vectors(self):
        return self.__points_count_between_vectors

    def get_quarter_point_counts(self):
        return self.__quarter_point_counts

    def get_main_axis_pitch_class(self):
        return self.__main_axis_pitch_class

    def get_track_name(self):
        return self.__track_name

    def get_signature_key_label(self):
        if self.__main_axis_pitch_class.value is None:
            return None
        if self.__quarter_point_counts[0] > self.__quarter_point_counts[1]:
            return CIRCLE_DUR_LABELS[PitchClass.class_for_index(self.__main_axis_pitch_class.value - 1).value]
        else:
            return CIRCLE_MOLL_LABELS[PitchClass.class_for_index(self.__main_axis_pitch_class.value - 1).value]

    def get_signature_key_label_utf8(self):
        if self.__main_axis_pitch_class.value is None:
            return None
        if self.__quarter_point_counts[0] > self.__quarter_point_counts[1]:
            return CIRCLE_DUR_LABELS_UTF8[PitchClass.class_for_index(self.__main_axis_pitch_class.value - 1).value]
        else:
            return CIRCLE_MOLL_LABELS_UTF8[PitchClass.class_for_index(self.__main_axis_pitch_class.value - 1).value]

    def calculate_cpms_array_whole_notes(self, midi_path, number_of_chunks):
        mid = MidiFile(midi_path, clip=True)
        self.__save_track_name(mid)
        note_time_segments_array, time = self.__get_note_time_segments_array_and_time(mid)
        number_of_chunks = min(number_of_chunks, ceil(time / mid.ticks_per_beat))
        self.__get_cpms_array(note_time_segments_array, mid.ticks_per_beat * 4, number_of_chunks)
        self.__points_count_between_vectors = calculate_points_count_between_vectors(self.__cpms_array)
        self.__main_axis_pitch_class = find_main_axis_trajectory(self.__note_class_duration_array)
        self.__quarter_point_counts = calculate_quarter_point_counts(self.__points_count_between_vectors, self.__main_axis_pitch_class)

    def calculate_cpms_array_half_notes(self, midi_path, number_of_chunks):
        mid = MidiFile(midi_path, clip=True)
        self.__save_track_name(mid)
        note_time_segments_array, time = self.__get_note_time_segments_array_and_time(mid)
        number_of_chunks = min(number_of_chunks, ceil(time / mid.ticks_per_beat))
        self.__get_cpms_array(note_time_segments_array, mid.ticks_per_beat * 2, number_of_chunks)
        self.__points_count_between_vectors = calculate_points_count_between_vectors(self.__cpms_array)
        self.__main_axis_pitch_class = find_main_axis_trajectory(self.__note_class_duration_array)
        self.__quarter_point_counts = calculate_quarter_point_counts(self.__points_count_between_vectors, self.__main_axis_pitch_class)

    def calculate_cpms_array_quarter_notes(self, midi_path, number_of_chunks):
        mid = MidiFile(midi_path, clip=True)
        self.__save_track_name(mid)
        note_time_segments_array, time = self.__get_note_time_segments_array_and_time(mid)
        number_of_chunks = min(number_of_chunks, ceil(time / mid.ticks_per_beat))
        self.__get_cpms_array(note_time_segments_array, mid.ticks_per_beat, number_of_chunks)
        self.__points_count_between_vectors = calculate_points_count_between_vectors(self.__cpms_array)
        self.__main_axis_pitch_class = find_main_axis_trajectory(self.__note_class_duration_array)
        self.__quarter_point_counts = calculate_quarter_point_counts(self.__points_count_between_vectors, self.__main_axis_pitch_class)

    def calculate_cpms_array_quaver_notes(self, midi_path, number_of_chunks):
        mid = MidiFile(midi_path, clip=True)
        self.__save_track_name(mid)
        note_time_segments_array, time = self.__get_note_time_segments_array_and_time(mid)
        number_of_chunks = min(number_of_chunks, ceil(time / mid.ticks_per_beat))
        self.__get_cpms_array(note_time_segments_array, mid.ticks_per_beat/2, number_of_chunks)
        self.__points_count_between_vectors = calculate_points_count_between_vectors(self.__cpms_array)
        self.__main_axis_pitch_class = find_main_axis_trajectory(self.__note_class_duration_array)
        self.__quarter_point_counts = calculate_quarter_point_counts(self.__points_count_between_vectors, self.__main_axis_pitch_class)

    def calculate_cpms_array_semiquaver_notes(self, midi_path, number_of_chunks):
        mid = MidiFile(midi_path, clip=True)
        self.__save_track_name(mid)
        note_time_segments_array, time = self.__get_note_time_segments_array_and_time(mid)
        number_of_chunks = min(number_of_chunks, ceil(time / mid.ticks_per_beat))
        self.__get_cpms_array(note_time_segments_array, mid.ticks_per_beat/4, number_of_chunks)
        self.__points_count_between_vectors = calculate_points_count_between_vectors(self.__cpms_array)
        self.__main_axis_pitch_class = find_main_axis_trajectory(self.__note_class_duration_array)
        self.__quarter_point_counts = calculate_quarter_point_counts(self.__points_count_between_vectors, self.__main_axis_pitch_class)

    def calculate_cpms_array_from_csv(self, csv_path):
        with open(csv_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                self.__cpms_array.append((atof(row[0]), atof(row[1])))



    def __save_track_name(self, mid):
        track_name, extension = os.path.splitext(os.path.basename(mid.filename))
        self.__track_name = track_name

    def __get_cpms_array(self, note_time_segments_array, time_per_chunk, number_of_chunks):
        self.__note_class_duration_array = self.__get_note_class_duration_array(note_time_segments_array, time_per_chunk,
                                                                  number_of_chunks)
        self.__cpms_array = calculate_cpms_array(self.__note_class_duration_array)

    def __get_note_time_segments_array_and_time(self, mid):
        track_time = 0
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
                            note_time_segments_array[self.__get_note_class(msg.note)].append((notes_on[note_index]["time"], time))
                            del notes_on[note_index]
                            break
                track_time = max(track_time, time)
        return note_time_segments_array, track_time

    def __get_note_class_duration_array(self, note_time_segments_array, time_per_chunk, number_of_chunks):
        note_class_duration_array = []
        time_per_chunk = time_per_chunk
        for chunk_index in range(number_of_chunks):
            note_class_duration_array.append({
                "A": 0, "D": 0, "G": 0, "C": 0, "F": 0, "Bb": 0, "Eb": 0, "Ab": 0, "Db": 0, "Gb": 0, "B": 0, "E": 0
            })
            chunk_time_range = (chunk_index * time_per_chunk, (chunk_index + 1) * time_per_chunk - 1)
            for note_class in note_time_segments_array:
                for time_segment in note_time_segments_array[note_class]:
                    note_class_duration_array[chunk_index][note_class] = note_class_duration_array[chunk_index][
                        note_class] + self.__calculate_note_duration_in_chunk(time_segment, chunk_time_range)
        return note_class_duration_array

    def __calculate_note_duration_in_chunk(self, time_segment, chunk_time_range):
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

    @staticmethod
    def __get_note_class(note):
        return MIDI_NOTE_CLASS[note % 12]
