import PySimpleGUI as sg

sg.theme("GreenMono")


class Layouts:
    graph_layout = []
    options_layout = []
    __signature_options_frame = []
    __signature_options_layout = []
    __key_layout = []

    def __init__(self, graph_size):
        self.graph_layout = [
            [
                sg.Graph(canvas_size=(graph_size, graph_size), graph_bottom_left=(-graph_size, -graph_size),
                         graph_top_right=(graph_size, graph_size), background_color='white',
                         enable_events=True, key='-graph-')
            ]
        ]
        self.__key_layout = [
            sg.Text('Music signature key: ', text_color='blue'), sg.Text('A', text_color='blue', key='-signature_key-'),
        ]
        self.__signature_options_layout = [
            [
                sg.Text('Index of music signature: '),
                sg.InputText("", key='-signature_index-', size=(5, 110))
            ],
            [
                sg.Button(button_text='Show music signature', key='-signature_button-')
            ],
            [
                sg.Checkbox(text='Show music signature on trajectory of fifths', key='-signature_on_trajectory-')
            ],
            [
                sg.Text('', text_color='red', visible=False, key='-signature_validation_text-')
            ],
            [
                sg.Button(button_text='Previous', key='-prev_signature-'),
                sg.Button(button_text='Next', key='-next_signature-'),
            ],
            self.__key_layout,
            [
                sg.Button(button_text='Generate .csv file', key='-csv_file-'),
            ],
        ]
        self.__signature_options_frame = [
            sg.Frame('Signature options', self.__signature_options_layout, key='-signature_options_frame-',
                     vertical_alignment='top', visible=False)
        ]
        self.options_layout = [
            [
                sg.Text("Choose a MIDI file: ")
            ],
            [
                sg.FileBrowse(key='-fileBrowse-', file_types=(("MIDI files", "*.mid"),)),
                sg.InputText("", key='-browse_path-')
            ],
            [
                sg.Checkbox(text='Show Main Directed Axis and Mode Axis', default=True, key='-show_axes-')
            ],
            [
                sg.Checkbox(text='Set radius length', default=False, change_submits=True, key='-fix_lines-'),
                sg.InputText("", key='-max_line_number-', size=(5, 110), visible=False)
            ],
            [
                sg.Text('Number of fragments: '), sg.InputText(size=(34, 110), key='-number_of_fragments-')
            ],
            [
                sg.Text('Generate trajectory of fifths: '),
            ],
            [
                sg.Button(button_text='Semiquaver-note resolution',
                          key='-semiquaver_generate_button-'),
            ],
            [
                sg.Button(button_text='Quaver-note resolution',
                          key='-quaver_generate_button-'),
            ],
            [
                sg.Button(button_text='Quarter-note resolution',
                          key='-quarter_generate_button-'),
            ],
            [
                sg.Button(button_text='Half-note resolution',
                          key='-half_generate_button-'),
            ],
            [
                sg.Button(button_text='Note resolution',
                          key='-whole_generate_button-'),
            ],
            [
                sg.Text('', text_color='red', visible=False, key='-trajectory_validation_text-')
            ],
            self.__signature_options_frame,
        ]
