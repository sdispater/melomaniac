# -*- coding: utf-8 -*-

import requests

from .client import Client
from ..player.library import Library as BaseLibrary
from ..player.playlist import Playlist
from ..player.track import Track
from ..player.list import List


class Library(BaseLibrary):

    def __init__(self, backend):
        super(Library, self).__init__(backend)

        self._favorites = None
        self._stream = None
        self._playlists = None

    @property
    def api(self):
        return self._backend.api

    def get_favorites(self):
        if self._favorites is not None:
            return self._favorites

        favorites_ = self.get('/me/favorites', limit=200)

        favorites = Playlist(self, 'Favorites', 'Favorites')
        for track_ in favorites_:
            if track_.streamable:
                track = Track(
                    self,
                    track_.id, track_.title, track_.user['username'], '',
                    0, 0, metadata=track_.obj
                )

                favorites.add_track(track)

        self._favorites = favorites

        return self._favorites

    def get_stream(self):
        stream = Playlist(self, 'Stream', 'Stream')

        if self._stream is not None:
            return self._stream

        stream_ = self.get('/me/activities', limit=100).collection

        for track_ in stream_:
            if track_.type not in ['track', 'track-repost'] or not track_.origin:
                continue

            track_ = track_.origin

            if not track_.streamable:
                continue

            track = Track(
                self,
                track_.id, track_.title, track_.user['username'], '',
                0, 0, metadata=track_.obj
            )

            stream.add_track(track)

        self._stream = stream

        return self._stream

    def get_playlists(self):
        playlists = List('Playlists')

        if self._playlists is not None:
            return self._playlists

        playlists_ = self.get('/me/playlists')

        for playlist_ in playlists_:
            playlist = Playlist(self, playlist_.id, playlist_.title)
            for track_ in playlist_.tracks:
                if not track_['streamable']:
                    continue

                track = Track(
                    self,
                    track_['id'], track_['title'], track_['user']['username'], '',
                    0, 0, metadata=track_
                )

                playlist.add_track(track)

            playlists.add_item(playlist)

        self._playlists = playlists

        return self._playlists

    def get_url(self, track):
        return self.get('/tracks/{}/stream'.format(track.id), allow_redirects=False).location

    def get(self, url, **kwargs):
        return self._backend.get(url, **kwargs)
