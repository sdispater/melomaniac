# -*- coding: utf-8 -*-

import string
from ..ui.ui import UI as BaseUI
from ..player.list import List


class UI(BaseUI):

    def _start(self):
        playlists = self.player.library.get_playlists()
        library = self.player.library
        artists_by_letter = List('Artists')
        letters = {}
        for artist in library['artists']:
            if artist.name:
                char = artist.name[0].upper()
            else:
                char = ''

            if char not in string.ascii_uppercase:
                if char in string.digits:
                    char = '1-9'
                else:
                    char = 'Other'

            if char not in letters:
                letters[char] = List(char)

            letters[char].add_item(artist)

        for char in sorted(list(letters.keys())):
            if char == 'Other':
                continue

            artists_by_letter.add_item(letters[char])

        artists_by_letter.add_item(letters['Other'])

        albums_by_letter = List('Albums')
        letters = {}
        for album in library['albums']:
            if album.name:
                char = album.name[0].upper()
            else:
                char = ''

            if char not in string.ascii_uppercase:
                if char in string.digits:
                    char = '1-9'
                else:
                    char = 'Other'

            if char not in letters:
                letters[char] = List(char)

            letters[char].add_item(album)

        for char in sorted(list(letters.keys())):
            if char == 'Other':
                continue

            albums_by_letter.add_item(letters[char])

        albums_by_letter.add_item(letters['Other'])

        menu = List(
            'Main Menu',
            [artists_by_letter,
             albums_by_letter,
             List('Playlists', playlists)]
        )
        self.view.current = menu
        self.view.set_item(0)
