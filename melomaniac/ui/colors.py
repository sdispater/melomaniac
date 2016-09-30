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
        PAIRS['red']: [curses.COLOR_RED, curses.COLOR_BLACK],
        PAIRS['blue']: [curses.COLOR_BLUE, curses.COLOR_BLACK],
        PAIRS['green']: [curses.COLOR_GREEN, curses.COLOR_BLACK],
        PAIRS['cyan']: [curses.COLOR_CYAN, curses.COLOR_BLACK],
        PAIRS['yellow']: [curses.COLOR_YELLOW, curses.COLOR_BLACK],
        PAIRS['magenta']: [curses.COLOR_MAGENTA, curses.COLOR_BLACK],
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
        for definition, (color, background) in self.DEFINITION.items():
            curses.init_pair(definition, color, background)

    def get(self, color):
        return self._colors[color]

    def __contains__(self, item):
        return item in self._colors
