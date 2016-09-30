# -*- coding: utf-8 -*-

import curses

from ..player.playlist import Playlist
from ..player.track import Track
from ..player.artist import Artist
from ..player.album import Album
from ..player.list import List
from ..player.item import Item


class View(object):

    def __init__(self, ui):
        self.ui = ui
        self.scr = ui.stdscr
        self.player = ui.player
        self.colors = ui.colors
        self.height, self.width = self.scr.getmaxyx()
        self.header_height = 2
        self.footer_height = 2
        self.viewheight = self.height - self.header_height - self.footer_height
        self.current = None
        self.previous = []
        self.item = 0
        self.current_item = None
        self._search_mode = False

        curses.curs_set(0)

        self.scr.timeout(17)

    @property
    def elements(self):
        elements = []
        if isinstance(self.current, List):
            elements = self.current.items
        elif isinstance(self.current, Artist):
            elements = self.current.albums
        elif isinstance(self.current, Playlist):
            elements = self.current.tracks
        else:
            elements = self.current[1]

        return elements

    def display(self):
        self.erase()
        if not self.in_search_mode():
            self.header()

        self.footer()

        self.main()
        self.refresh()

    def header(self):
        locstring = [('Melomaniac', 'blue')]
        for i in self.previous[1:]:
            i = i[0]
            locstring.append((' > ', 'header-sep'))
            if isinstance(i, Artist):
                locstring.append((i.name, 'cyan'))
            elif isinstance(i, Playlist):
                locstring.append((i.name, 'magenta'))
            elif isinstance(i, List):
                locstring.append((i.name, ''))
            elif isinstance(i, Item):
                locstring.append((i.name, ''))
            else:
                if isinstance(i, tuple):
                    locstring.append((i[0], 'header-text'))
                else:
                    locstring.append((i, 'header-text'))

        if self.previous:
            locstring.append((' > ', 'header-sep'))
            if isinstance(self.current, List):
                locstring.append((self.current.name, ''))
            elif isinstance(self.current, Item):
                locstring.append((self.current.name, ''))
            elif isinstance(self.current, Playlist):
                locstring.append((self.current.name, 'magenta'))
            elif isinstance(self.current, Artist):
                locstring.append((self.current.name, 'cyan'))
            else:
                locstring.append((self.current[0], 'header-text'))

        self.string(locstring, 0, 0)
        for i in range(0, self.width):
            self.scr.addch(1, i, '-')

    def footer(self):
        if self.player.track is not None:
            self.track_footer()
        else:
            for i in range(0, self.width):
                self.scr.addch(self.height - 10, i, ' ')

        self.string(self.player.status, self.height - 1, 0)

    def get_search(self):
        curses.setsyx(0, 13)
        search = self.scr.getstr()
        curses.noecho()
        curses.curs_set(0)

        return search

    def search_mode(self, search_mode):
        self._search_mode = search_mode

        if search_mode is True:
            curses.setsyx(0, 0)
            self.scr.clrtoeol()
            self.string([('Search for: ', 'blue')], 0, 0)
            curses.echo()
            curses.curs_set(1)

        return self

    def in_search_mode(self):
        return self._search_mode

    def main(self):
        elements = self.elements

        count = len(elements)
        top_half = self.viewheight // 2
        bottom_half = self.viewheight - top_half
        if count <= self.viewheight:
            cl = 0
        elif (self.item - top_half) < 0:
            cl = 0
        elif (self.item + bottom_half) > (count - 1):
            cl = count - self.viewheight
        else:
            cl = self.item - top_half

        for i in range(cl, cl + self.viewheight):
            if i < count:
                element = elements[i]
                if isinstance(element, Playlist):
                    if not element.name:
                        continue

                    s = ' {} '.format(element.name)
                elif isinstance(element, List):
                    s = ' {} '.format(element.name)
                elif isinstance(element, Item):
                    s = ' {} '.format(element.name)
                elif isinstance(element, Artist):
                    s = ' {} '.format(element.name)
                elif isinstance(element, Track):
                    if isinstance(self.current, Album):
                        number = element.number
                        s = ' {:3d}. {}'.format(number, element.title, element.artist)
                    elif isinstance(self.current, Playlist):
                        number = i + 1
                        s = ' {:3d}. {} - {}'.format(number, element.title, element.artist)
                    else:
                        number = element.number
                        s = ' {:3d}. {} - {}'.format(number, element.title, element.artist)

                    max_song_width = self.width - 6
                    s = s[:max_song_width] + ' ' * (self.width - 6 - len(s)) + element.duration_string + ' '

                    if i == self.item:
                        self.scr.addnstr(self.header_height + i - cl, 0, s, self.width, self.colors.get('cyan_reverse'))
                    elif self.player.track is not None and self.player.track.id == element.id:
                        self.scr.addnstr(self.header_height + i - cl, 0, s, self.width, self.colors.get('yellow'))
                    else:
                        self.scr.addnstr(self.header_height + i - cl, 0, s, self.width)

                    continue
                else:
                    # Assuming main menu tuple
                    s = element[0]

                slen = len(s)
                s = s + ' ' * (self.width - slen)
                try:
                    if i == self.item:
                        self.scr.addnstr(self.header_height + i - cl, 0, s, self.width, self.colors.get('cyan_reverse'))
                    else:
                        self.scr.addnstr(self.header_height + i - cl, 0, s, self.width)
                except curses.error:
                    pass
            else:
                break

    def track_footer(self):
        done = int(self.width * self.player.track_percent / 100)
        for i in range(0, done):
            self.scr.addch(self.height - 2, i, '-', self.colors.get('green'))

        for i in range(done, self.width):
            self.scr.addch(self.height - 2, i, '-')

        self.string(
            [self.player.status, ' > ',
             (self.player.track.artist, 'cyan'), ' - ', (self.player.track.title, 'yellow')],
            self.height - 1, 0, self.width - 6)

        # Current time
        current_time = '{:02d}:{:02d}'.format(
            self.player.track_current // 60,
            self.player.track_current % 60
        )
        self.scr.addstr(
            self.height - 1, self.width - 6,
            current_time, self.colors.get('green')
        )

    def string(self, string, y, x, width=None):
        if width is None:
            width = self.width

        if not isinstance(string, (list, tuple)):
            string = [(string, '')]

        for i in string:
            if isinstance(i, str):
                s = i
                col = None
            else:
                s = i[0]
                if len(i) == 2:
                    col = i[1]
                else:
                    col = None

            if (self.width - x) > 0:
                if col and col in self.colors:
                    self.scr.addnstr(y, x, s, width - x, self.colors.get(col))
                else:
                    self.scr.addstr(y, x, s, width - x)

            x += len(s)

    def line(self, string, y, slen, width=None, color='white'):
        if width is None:
            width = self.width

        self.scr.addnstr(y, 0, string, width, self.colors.get(color))
        for i in range(slen, width):
            self.scr.addstr(y, slen, ' ')

        slen += 1

    def clear(self):
        self.scr.clear()

    def erase(self):
        self.scr.erase()

    def refresh(self):
        self.scr.refresh()

    def resize(self):
        self.width, self.heigth = self.scr.getmaxyx()
        self.viewheight = self.height - self.header_height - self.footer_height

    def set_item(self, item):
        self.item = item
        if isinstance(self.current, List):
            self.current_item = self.current.items[item]
        elif isinstance(self.current, Playlist):
            self.current_item = self.current.tracks[item]
        elif isinstance(self.current, Artist):
            self.current_item = self.current.albums[item]
        elif isinstance(self.current, list):
            self.current_item = self.current[item]
        elif isinstance(self.current, tuple):
            self.current_item = self.current[1][item]

    def back(self):
        self.current = self.previous[-1][0]
        self.set_item(self.previous[-1][1])
        self.previous.pop()

    def enter(self):
        if isinstance(self.current_item, Track):
            return

        self.previous.append((self.current, self.item))

        self.current = self.current_item
        self.set_item(0)
