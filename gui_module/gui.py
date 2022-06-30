import PySimpleGUI as sg
from gui_module.layouts import Layouts
from chart_display_module.chart_display import TrajectoryOfFifthsChart
from midi_module.midi_analyzer import TrajectoryOfFifthsMidi
from csv_module.csv_manager import CsvManager


class Gui:
    __layouts = []
    __window = None
    __trajectoryOfFifthsMidi = None
    __chart = None

    def __init__(self, graph_size, margin):
        layouts = Layouts(graph_size)
        self.__layouts = [
            [
                [sg.Frame('Options', layouts.options_layout, key='FRAME', vertical_alignment='top'),
                 sg.Frame('', layouts.graph_layout, key='FRAME3', visible=True)]
            ],
        ]
        self.__window = sg.Window('Trajectory of fifths generator', self.__layouts, size=(1400, 900), finalize=True)
        self.__trajectoryOfFifthsMidi = TrajectoryOfFifthsMidi()
        self.__chart = TrajectoryOfFifthsChart(self.__window['-graph-'], graph_size, margin)
        while True:
            event, values = self.__window.read()
            self.__window.Element('-trajectory_validation_text-').update(visible=False)
            self.__window.Element('-signature_validation_text-').update(visible=False)
            if event == sg.WINDOW_CLOSED:
                break
            elif event == '-semiquaver_generate_button-' \
                    or event == '-quaver_generate_button-' \
                    or event == '-quarter_generate_button-' \
                    or event == '-half_generate_button-' \
                    or event == '-whole_generate_button-':
                self.__window['-graph-'].erase()
                try:
                    number_of_samples = int(values['-number_of_samples-'])
                    try:
                        midi_path = values['-browse_path-']
                        show_axes = values['-show_axes-']
                        if midi_path == '':
                            self.__window.Element('-trajectory_validation_text-').update('Choose MIDI file',
                                                                                         visible=True)
                        else:
                            number_of_lines = 0
                            try:
                                if values['-fix_lines-']:
                                    number_of_lines = max(int(values['-max_line_number-']), 0)
                                if event == '-semiquaver_generate_button-':
                                    self.__trajectoryOfFifthsMidi.calculate_cpms_array_semiquaver_notes(midi_path,
                                                                                                     number_of_samples)
                                elif event == '-quaver_generate_button-':
                                    self.__trajectoryOfFifthsMidi.calculate_cpms_array_quaver_notes(midi_path,
                                                                                                     number_of_samples)
                                elif event == '-quarter_generate_button-':
                                    self.__trajectoryOfFifthsMidi.calculate_cpms_array_quarter_notes(midi_path, number_of_samples)
                                elif event == '-half_generate_button-':
                                    self.__trajectoryOfFifthsMidi.calculate_cpms_array_half_notes(midi_path,
                                                                                                     number_of_samples)
                                elif event == '-whole_generate_button-':
                                    self.__trajectoryOfFifthsMidi.calculate_cpms_array_whole_notes(midi_path,
                                                                                                     number_of_samples)
                                self.__show_trajectory_of_fifths(show_axes, number_of_lines)
                                self.__window.Element('-signature_options_frame-').update(visible=True)
                                self.__update_key()
                            except ValueError:  # integer cast exception
                                self.__window.Element('-trajectory_validation_text-').update(
                                    'Incorrect number of circles', visible=True)
                    except:
                        self.__window.Element('-trajectory_validation_text-').update('Incorrect name of file',
                                                                                     visible=True)
                except ValueError:  # integer cast exception
                    self.__window.Element('-trajectory_validation_text-').update('Incorrect number of samples',
                                                                                 visible=True)
            elif event == '-signature_button-' or event == '-prev_signature-' or event == '-next_signature-':
                try:
                    index_string_value = values['-signature_index-']
                    maximum_index = len(self.__trajectoryOfFifthsMidi.get_note_class_duration_array())
                    show_axes = values['-show_axes-']
                    show_trajectory = values['-signature_on_trajectory-']
                    if index_string_value == '':
                        signature_index = 1
                    else:
                        signature_index = int(index_string_value)
                        if event == '-prev_signature-':
                            if signature_index > 1:
                                signature_index -= 1
                            else:
                                self.__window.Element('-signature_validation_text-').update(
                                    'Signature index range: 1 to {}'.format(maximum_index),
                                    visible=True)
                        elif event == '-next_signature-':
                            if signature_index < maximum_index:
                                signature_index += 1
                            else:
                                self.__window.Element('-signature_validation_text-').update(
                                    'Signature index range: 1 to {}'.format(maximum_index),
                                    visible=True)
                    self.__window.Element('-signature_index-').update(signature_index)
                    if 0 < signature_index <= maximum_index:
                        self.__window['-graph-'].erase()
                        number_of_lines = 0
                        try:
                            if values['-fix_lines-']:
                                number_of_lines = max(int(values['-max_line_number-']), 0)
                            if show_trajectory:
                                self.__show_music_signature_on_trajectory(signature_index - 1, number_of_lines, show_axes)
                            else:
                                if show_axes:
                                    self.__show_music_signature_for_point_with_axis(signature_index - 1, number_of_lines)
                                else:
                                    self.__show_music_signature_for_point(signature_index - 1, number_of_lines)
                            self.__window.Element('-signature_options_frame-').update(visible=True)
                        except ValueError:  # integer cast exception
                            self.__window.Element('-trajectory_validation_text-').update('Incorrect number of circles',
                                                                                         visible=True)
                    else:
                        self.__window.Element('-signature_validation_text-').update(
                            'Signature index range: 1 to {}'.format(maximum_index),
                            visible=True)
                except ValueError:  # integer cast exception
                    self.__window.Element('-signature_validation_text-').update('Type correct index of signature',
                                                                                visible=True)
            elif event == '-fix_lines-':
                self.__window.Element('-max_line_number-').update(visible=values['-fix_lines-'])
            elif event == '-csv_file-':
                try:
                    midi_path = values['-browse_path-']
                    self.__save_all_data_to_csv(midi_path)
                except:
                    self.__window.Element('-trajectory_validation_text-').update('Incorrect name of file',
                                                                             visible=True)
        self.__window.close()

    def __show_trajectory_of_fifths(self, show_axes, number_of_lines):
        if show_axes:
            self.__chart.generate_trajectory_of_fifths_graph_with_directed_axis(
                self.__trajectoryOfFifthsMidi.get_cpms_array(),
                number_of_lines, self.__trajectoryOfFifthsMidi.get_points_count_between_vectors(),
                                                            self.__trajectoryOfFifthsMidi.get_quarter_point_counts(),
                self.__trajectoryOfFifthsMidi.get_main_axis_pitch_class())
        else:
            self.__chart.generate_trajectory_of_fifths_graph(self.__trajectoryOfFifthsMidi.get_cpms_array(),
                                                             number_of_lines,
                                                             self.__trajectoryOfFifthsMidi.get_points_count_between_vectors(),
                                                            self.__trajectoryOfFifthsMidi.get_quarter_point_counts())

    def __show_music_signature_for_point(self, point_index, number_of_lines):
        self.__chart.generate_music_signature_graph_for_note_class_durations(
            self.__trajectoryOfFifthsMidi.get_note_class_durations(point_index), number_of_lines)

    def __show_music_signature_for_point_with_axis(self, point_index, number_of_lines):
        self.__chart.generate_music_signature_graph_for_note_class_durations_with_directed_axis(
            self.__trajectoryOfFifthsMidi.get_note_class_durations(point_index), number_of_lines)

    def __show_music_signature_on_trajectory(self, signature_index, number_of_lines, show_axes):
        self.__chart.generate_music_signature_on_trajectory_of_fifths_graph(signature_index, number_of_lines,
                                                                            self.__trajectoryOfFifthsMidi.get_cpms_array(),
                                                                            self.__trajectoryOfFifthsMidi.get_note_class_duration_array(),
                                                                            show_axes,
                                                                            self.__trajectoryOfFifthsMidi.get_points_count_between_vectors(),
                                                                            self.__trajectoryOfFifthsMidi.get_quarter_point_counts(),
                                                                            self.__trajectoryOfFifthsMidi.get_main_axis_pitch_class())
        self.__update_key()

    def __update_key(self):
        key = self.__trajectoryOfFifthsMidi.get_signature_key_label()
        self.__window.Element('-signature_key-').update(value=key if key is not None else 'Could not be designated')

    def __save_all_data_to_csv(self, midi_path):
        csv_manager = CsvManager()
        # 32
        self.__trajectoryOfFifthsMidi.calculate_cpms_array_semiquaver_notes(midi_path, 32)
        csv_manager.fill_data_32_semiquaver(self.__trajectoryOfFifthsMidi.get_signature_key_label_utf8(), self.__trajectoryOfFifthsMidi.get_quarter_point_counts())
        self.__trajectoryOfFifthsMidi.calculate_cpms_array_quaver_notes(midi_path, 32)
        csv_manager.fill_data_32_quaver(self.__trajectoryOfFifthsMidi.get_signature_key_label_utf8(),
                                     self.__trajectoryOfFifthsMidi.get_quarter_point_counts())
        self.__trajectoryOfFifthsMidi.calculate_cpms_array_quarter_notes(midi_path, 32)
        csv_manager.fill_data_32_quarter(self.__trajectoryOfFifthsMidi.get_signature_key_label_utf8(),
                                     self.__trajectoryOfFifthsMidi.get_quarter_point_counts())
        self.__trajectoryOfFifthsMidi.calculate_cpms_array_half_notes(midi_path, 32)
        csv_manager.fill_data_32_half(self.__trajectoryOfFifthsMidi.get_signature_key_label_utf8(),
                                     self.__trajectoryOfFifthsMidi.get_quarter_point_counts())
        self.__trajectoryOfFifthsMidi.calculate_cpms_array_whole_notes(midi_path, 32)
        csv_manager.fill_data_32_whole(self.__trajectoryOfFifthsMidi.get_signature_key_label_utf8(),
                                     self.__trajectoryOfFifthsMidi.get_quarter_point_counts())
        #16
        # self.__trajectoryOfFifthsMidi.calculate_cpms_array_semiquaver_notes(midi_path, 16)
        # csv_manager.fill_data_8_semiquaver(self.__trajectoryOfFifthsMidi.get_signature_key_label_utf8(),
        #                                     self.__trajectoryOfFifthsMidi.get_quarter_point_counts())
        # self.__trajectoryOfFifthsMidi.calculate_cpms_array_quaver_notes(midi_path, 16)
        # csv_manager.fill_data_8_quaver(self.__trajectoryOfFifthsMidi.get_signature_key_label_utf8(),
        #                                 self.__trajectoryOfFifthsMidi.get_quarter_point_counts())
        # self.__trajectoryOfFifthsMidi.calculate_cpms_array_quarter_notes(midi_path, 16)
        # csv_manager.fill_data_8_quarter(self.__trajectoryOfFifthsMidi.get_signature_key_label_utf8(),
        #                                  self.__trajectoryOfFifthsMidi.get_quarter_point_counts())
        # self.__trajectoryOfFifthsMidi.calculate_cpms_array_half_notes(midi_path, 16)
        # csv_manager.fill_data_8_half(self.__trajectoryOfFifthsMidi.get_signature_key_label_utf8(),
        #                               self.__trajectoryOfFifthsMidi.get_quarter_point_counts())
        # self.__trajectoryOfFifthsMidi.calculate_cpms_array_whole_notes(midi_path, 16)
        # csv_manager.fill_data_8_whole(self.__trajectoryOfFifthsMidi.get_signature_key_label_utf8(),
        #                                self.__trajectoryOfFifthsMidi.get_quarter_point_counts())
        #8
        # self.__trajectoryOfFifthsMidi.calculate_cpms_array_semiquaver_notes(midi_path, 8)
        # csv_manager.fill_data_16_semiquaver(self.__trajectoryOfFifthsMidi.get_signature_key_label_utf8(),
        #                                     self.__trajectoryOfFifthsMidi.get_quarter_point_counts())
        # self.__trajectoryOfFifthsMidi.calculate_cpms_array_quaver_notes(midi_path, 8)
        # csv_manager.fill_data_16_quaver(self.__trajectoryOfFifthsMidi.get_signature_key_label_utf8(),
        #                                 self.__trajectoryOfFifthsMidi.get_quarter_point_counts())
        # self.__trajectoryOfFifthsMidi.calculate_cpms_array_quarter_notes(midi_path, 8)
        # csv_manager.fill_data_16_quarter(self.__trajectoryOfFifthsMidi.get_signature_key_label_utf8(),
        #                                  self.__trajectoryOfFifthsMidi.get_quarter_point_counts())
        # self.__trajectoryOfFifthsMidi.calculate_cpms_array_half_notes(midi_path, 8)
        # csv_manager.fill_data_16_half(self.__trajectoryOfFifthsMidi.get_signature_key_label_utf8(),
        #                               self.__trajectoryOfFifthsMidi.get_quarter_point_counts())
        # self.__trajectoryOfFifthsMidi.calculate_cpms_array_whole_notes(midi_path, 8)
        # csv_manager.fill_data_16_whole(self.__trajectoryOfFifthsMidi.get_signature_key_label_utf8(),
        #                                self.__trajectoryOfFifthsMidi.get_quarter_point_counts())

        csv_manager.save_data_to_csv(self.__trajectoryOfFifthsMidi.get_track_name())
