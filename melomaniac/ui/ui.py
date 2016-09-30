# -*- coding: utf-8 -*-

import curses
from .view import View
from .colors import Colors
from .controller import Controller


class UI(object):

    def __init__(self, player):
        self.player = player
        self.stdscr = None
        self.view = None
        self.colors = None

    def launch(self):
        curses.wrapper(self._launch)

    def _launch(self, stdscr):
        self.stdscr = stdscr
        self.colors = Colors()
        self.view = View(self)
        self.controller = Controller(self.view)

        self._start()

        self.view.clear()
        self.view.display()
        self.controller.handle()

    def _start(self):
        raise NotImplementedError()
