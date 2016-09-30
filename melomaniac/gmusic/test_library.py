# -*- coding: utf-8 -*-

from ..player.playlist import Playlist
from ..player.album import Album
from ..player.artist import Artist
from ..player.track import Track
from ..player.list import List

from .library import Library


class TestLibrary(Library):

    def __init__(self):
        super(TestLibrary, self).__init__(None)
        self._playlists = [
            Playlist(self, '1', 'My Playlist')
        ]
        dead_can_dance = Artist(self, '1', 'Dead Can Dance')
        alter_bridge = Artist(self, '2', 'Alter Bridge')
        anastasis = Album(self, '1', 'Anastasis', dead_can_dance)
        anastasis.add_tracks([
            Track(self, '1', 'Children Of The Sun', dead_can_dance.name, anastasis.name, 1, 1),
            Track(self, '2', 'Anabasis', dead_can_dance.name, anastasis.name, 2, 1),
        ])
        fortress = Album(self, '1', 'Fortress', alter_bridge)
        fortress.add_tracks([
            Track(self, '11', 'Cry Of Achilles', alter_bridge.name, fortress.name, 1, 1, {'durationMillis': 391000}),
            Track(self, '12', 'Addicted To Pain', alter_bridge.name, fortress.name, 2, 1, {'durationMillis': 257000}),
        ])

        dead_can_dance.add_album(anastasis)
        alter_bridge.add_album(fortress)
        self._library = {
            'artists': [
                dead_can_dance,
                alter_bridge,
            ],
            'albums': [
                anastasis,
                fortress,
            ],
            '_default': {}
        }

    def search(self, query):
        return List(
            'Search Results for [{}]'.format(query.decode()),
            [List('Artists', self._library['artists']),
             List('Albums', self._library['albums'][1:]),
             List('Playlists', self._playlists),]
        )
