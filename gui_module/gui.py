import PySimpleGUI as sg
from gui_module.layouts import Layouts
from chart_display_module.chart_display import TrajectoryOfFifthsChart
from midi_module.midi_analyzer import TrajectoryOfFifthsMidi


class Gui:
    __graph_size = 0
    __layout = []
    __window = None
    __trajectoryOfFifthsMidi = None
    __chart = None

    def __init__(self, graph_size, margin):
        self.__graph_size = graph_size
        layouts = Layouts(self.__graph_size)
        self.__layout = [
            [
                [sg.Frame('Options', layouts.options_layout, key='FRAME', vertical_alignment='top'),
                 sg.Frame('', layouts.graph_layout, key='FRAME3', visible=True)]
            ],
        ]
        self.__window = sg.Window('Trajectory of fifths generator', self.__layout, size=(1400, 900), finalize=True)
        self.__trajectoryOfFifthsMidi = TrajectoryOfFifthsMidi()
        self.__chart = TrajectoryOfFifthsChart(self.__window['-graph-'], self.__graph_size, margin)
        while True:
            event, values = self.__window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == '-generate_button-':
                self.__window['-graph-'].erase()
                try:
                    number_of_fragments = int(values['-number_of_fragments-'])
                    try:
                        midi_path = values['-browse_path-']
                        show_axes = values['-show_axes-']
                        if midi_path == '':
                            self.__window.Element('-trajectory_validation_text-').update('Choose MIDI file',
                                                                                         visible=True)
                        else:
                            self.__window.Element('-trajectory_validation_text-').update(visible=False)
                            number_of_lines = 0
                            try:
                                if values['-fix_lines-']:
                                    number_of_lines = max(int(values['-max_line_number-']), 0)
                                self.__show_trajectory_of_fifths_quarter_notes(midi_path, show_axes,
                                                                               number_of_fragments, number_of_lines)
                                self.__window.Element('-signature_options_frame-').update(visible=True)
                            except ValueError:  # integer cast exception
                                self.__window.Element('-trajectory_validation_text-').update(
                                    'Incorrect number of circles', visible=True)
                    except:
                        self.__window.Element('-trajectory_validation_text-').update('Incorrect name of file',
                                                                                     visible=True)
                except ValueError:  # integer cast exception
                    self.__window.Element('-trajectory_validation_text-').update('Incorrect number of fragments',
                                                                                 visible=True)
            elif event == '-signature_button-':
                try:
                    signature_index = int(values['-signature_index-'])
                    maximum_index = len(self.__trajectoryOfFifthsMidi.get_note_class_duration_array())
                    if 0 < signature_index <= maximum_index:
                        self.__window['-graph-'].erase()
                        self.__window.Element('-signature_validation_text-').update(visible=False)
                        number_of_lines = 0
                        try:
                            if values['-fix_lines-']:
                                number_of_lines = max(int(values['-max_line_number-']), 0)
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
            elif event == '-signature_axis_button-':
                try:
                    signature_index = int(values['-signature_index-'])
                    maximum_index = len(self.__trajectoryOfFifthsMidi.get_note_class_duration_array())
                    if 0 < signature_index <= maximum_index:
                        self.__window['-graph-'].erase()
                        self.__window.Element('-signature_validation_text-').update(visible=False)
                        number_of_lines = 0
                        try:
                            if values['-fix_lines-']:
                                number_of_lines = max(int(values['-max_line_number-']), 0)
                            self.__show_music_signature_for_point_with_axis(signature_index - 1, number_of_lines)
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
        self.__window.close()

    def __show_trajectory_of_fifths_quarter_notes(self, midi_path, show_axes, number_of_fragments, number_of_lines):
        self.__trajectoryOfFifthsMidi.calculate_cpms_array_quarter_notes(midi_path, number_of_fragments)
        if show_axes:
            self.__chart.generate_trajectory_of_fifths_graph_with_directed_axis(
                self.__trajectoryOfFifthsMidi.get_cpms_array(),
                self.__trajectoryOfFifthsMidi.get_note_class_duration_array(),
                number_of_lines)
        else:
            self.__chart.generate_trajectory_of_fifths_graph(self.__trajectoryOfFifthsMidi.get_cpms_array(),
                                                             number_of_lines)

    def __show_music_signature_for_point(self, point_index, number_of_lines):
        self.__chart.generate_music_signature_graph_for_note_class_durations(
            self.__trajectoryOfFifthsMidi.get_note_class_durations(point_index), number_of_lines)

    def __show_music_signature_for_point_with_axis(self, point_index, number_of_lines):
        self.__chart.generate_music_signature_graph_for_note_class_durations_with_directed_axis(
            self.__trajectoryOfFifthsMidi.get_note_class_durations(point_index), number_of_lines)
