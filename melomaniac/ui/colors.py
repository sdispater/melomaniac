# -*- coding: utf-8 -*-

import curses


class Colors(object):

    PAIRS = {
        'white': 0,
        'red': 1,
        'blue': 2,
        'green': 3,
        'cyan': 4,
        'yellow': 5,
        'magenta': 6,
    }

    DEFINITION = {
        PAIRS['red']: [curses.COLOR_RED, -1],
        PAIRS['blue']: [curses.COLOR_BLUE, -1],
        PAIRS['green']: [curses.COLOR_GREEN, -1],
        PAIRS['cyan']: [curses.COLOR_CYAN, -1],
        PAIRS['yellow']: [curses.COLOR_YELLOW, -1],
        PAIRS['magenta']: [curses.COLOR_MAGENTA, -1],
    }

    def __init__(self):
        self._colors = {
            'white': curses.color_pair(self.PAIRS['white']),
            'black': curses.color_pair(self.PAIRS['white']) | curses.A_REVERSE,
            'red': curses.color_pair(self.PAIRS['red']),
            'blue': curses.color_pair(self.PAIRS['blue']),
            'green': curses.color_pair(self.PAIRS['green']),
            'green_reverse': (curses.color_pair(self.PAIRS['green'])
                              | curses.A_REVERSE),
            'cyan': curses.color_pair(self.PAIRS['cyan']),
            'cyan_reverse': (curses.color_pair(self.PAIRS['cyan'])
                             | curses.A_REVERSE),
            'yellow': curses.color_pair(self.PAIRS['yellow']),
            'yellow_reverse': (curses.color_pair(self.PAIRS['yellow'])
                               | curses.A_REVERSE),
            'magenta': curses.color_pair(self.PAIRS['magenta']),
            'magenta_reverse': (curses.color_pair(self.PAIRS['magenta'])
                                | curses.A_REVERSE),
        }

        curses.start_color()
        curses.use_default_colors()
        for definition, (color, background) in self.DEFINITION.items():
            curses.init_pair(definition, color, background)

    def get(self, color):
        return self._colors[color]

    def pair(self, color):
        return self.PAIRS[color]

    def __contains__(self, item):
        return item in self._colors
