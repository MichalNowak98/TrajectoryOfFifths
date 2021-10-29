import PySimpleGUI


class ComparisonGraphLayout:
    LEFT_GRAPH_KEY = 'left_graph'
    RIGHT_GRAPH_KEY = 'right_graph'
    layout = []

    def __init__(self, graph_size):
        self.layout = [
            PySimpleGUI.Graph(canvas_size=(graph_size, graph_size), graph_bottom_left=(-graph_size, -graph_size),
                              graph_top_right=(graph_size, graph_size), background_color='white',
                              enable_events=True, key=self.RIGHT_GRAPH_KEY),
            PySimpleGUI.Graph(canvas_size=(graph_size, graph_size), graph_bottom_left=(-graph_size, -graph_size),
                              graph_top_right=(graph_size, graph_size), background_color='white',
                              enable_events=True, key=self.LEFT_GRAPH_KEY)
        ]


class GraphLayout:
    GRAPH_KEY = 'graph'
    layout = []

    def __init__(self, graph_size):
        self.layout = [
            [
                PySimpleGUI.Graph(canvas_size=(graph_size, graph_size), graph_bottom_left=(-graph_size, -graph_size),
                                  graph_top_right=(graph_size, graph_size), background_color='white',
                                  enable_events=True, key=self.GRAPH_KEY)
            ]
        ]
