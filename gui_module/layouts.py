import PySimpleGUI as sg

sg.theme("GreenMono")


class Layouts:
    graph_layout = []
    options_layout = []
    __signature_options_frame = []
    __signature_options_layout = []
    __option_buttons_layout = []

    def __init__(self, graph_size):
        self.graph_layout = [
            [
                sg.Graph(canvas_size=(graph_size, graph_size), graph_bottom_left=(-graph_size, -graph_size),
                         graph_top_right=(graph_size, graph_size), background_color='white',
                         enable_events=True, key='-graph-')
            ]
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
                sg.Button(button_text='Show music signature with directed axis', key='-signature_axis_button-')
            ],
            [
                sg.Text('', text_color='red', visible=False, key='-signature_validation_text-')
            ]
        ]
        self.__signature_options_frame = [
            sg.Frame('Signature options', self.__signature_options_layout, key='-signature_options_frame-',
                     vertical_alignment='top', visible=False)
        ]
        self.__option_buttons_layout = [
            sg.Button(button_text='Generate trajectory of fifths', key='-generate_button-'),
            sg.Text('', text_color='red', visible=False, key='-trajectory_validation_text-')
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
                sg.Checkbox(text='Set number of circles', default=False, change_submits=True, key='-fix_lines-'),
                sg.InputText("", key='-max_line_number-', size=(5, 110), visible=False)
            ],
            [
                sg.Text('Number of fragments: '), sg.InputText(size=(34, 110), key='-number_of_fragments-')
            ],
            self.__option_buttons_layout,
            self.__signature_options_frame,
        ]
