# -*- coding: utf-8 -*-

from ..ui.ui import UI as BaseUI
from ..player.list import List


class UI(BaseUI):

    def _start(self):
        favorites = self.player.library.get_favorites()
        stream = self.player.library.get_stream()
        playlists = self.player.library.get_playlists()
        items = []

        if stream.tracks:
            items.append(stream)

        items.append(favorites)

        if playlists.items:
            items.append(playlists)

        menu = List(
            'Main Menu',
            items
        )
        self.view.current = menu
        self.view.set_item(0)
