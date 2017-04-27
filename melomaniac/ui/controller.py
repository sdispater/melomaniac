# -*- coding: utf-8 -*-

import curses

from ..player.list import List
from ..player.playlist import Playlist
from ..player.track import Track
from ..player.artist import Artist


class Controller(object):

    def __init__(self, view):
        self.view = view
        self.player = view.player
        self.scr = view.scr

    def handle(self):
        question = None
        while True:
            c = self.scr.getch()
            if self.view.in_search_mode():
                if not question:
                    question = self.view.ask(0, 0, 'Search for: ')

                if c == 27:
                    self.view.search_mode(False)
                    continue

                if not c == ord('\n'):
                    self.view.refresh()
                    continue

                query = question.response()

                menu = self.player.library.search(query)
                if self.view.previous:
                    self.view.current = self.view.previous[0]
                    self.view.previous = []

                self.view.current_item = menu
                self.view.enter()
                question = None
                self.view.search_mode(False)

            elif c == -1:
                if (not self.player.is_playing()
                    and not self.player.is_paused()
                    and self.player.has_next()):
                    self.player.next()
            elif c == ord('q'):
                self.player.stop()
                break
            elif c == ord('\n') or c == ord(']'):
                if self.view.current_item:
                    self.player.stop()
                    self.player.queue = []

                    if c == ord('\n'):
                        if not self.play():
                            self.switch()

                    if (self.player.queue != []
                            and self.player.queue_number < self.player.queue_length):
                        self.player.play()
            elif c == ord('.'):
                self.player.stop()
                self.player.next()
            elif c == ord(','):
                self.player.stop()
                self.player.previous()
            elif c == curses.KEY_LEFT:
                self.switch('back')
            elif c == curses.KEY_RIGHT:
                self.switch()
            elif c == curses.KEY_DOWN:
                count = len(self.view.elements)
                if self.view.item < count - 1:
                    self.view.set_item(self.view.item + 1)
                else:
                    self.view.set_item(0)

                if isinstance(self.view.current, Playlist):
                    self.view.current.position = self.view.item
                elif isinstance(self.view.current, Artist):
                    self.view.current_album = self.view.item
            elif c == curses.KEY_UP:
                if self.view.item > 0:
                    self.view.set_item(self.view.item - 1)
                else:
                    self.view.set_item(len(self.view.elements) - 1)

                if isinstance(self.view.current, Playlist):
                    self.view.current.position = self.view.item
                elif isinstance(self.view.current, Artist):
                    self.view.current_album = self.view.item
            elif c == ord(' '):
                self.player.toggle()
            elif c == curses.KEY_RESIZE:
                self.view.resize()
            elif c == ord('f'):
                self.player.forward()
            elif c == ord('r'):
                self.player.rewind()
            elif c == ord('s'):
                self.view.search_mode(True)

            # Redraw the screen
            self.view.display()

    def play(self):
        if isinstance(self.view.current_item, Track):
            self.player.queue = self.view.current.tracks
            self.player.queue_number = self.view.item
            self.player.queue_length = len(self.player.queue)

            return True

        return False

    def switch(self, direction='enter'):
        if direction == 'back':
            if self.view.previous:
                self.view.back()
        else:
            self.view.enter()
