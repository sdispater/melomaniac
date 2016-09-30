# -*- coding: utf-8 -*-


class Playlist(object):

    def __init__(self, library, id, name):
        self._library = library
        self._id = id
        self._name = name
        self._tracks = []
        self._position = 0

    @property
    def name(self):
        return self._name

    @property
    def tracks(self):
        return self._tracks

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    def add_tracks(self, tracks):
        for track in tracks:
            self.add_track(track)

        return self

    def add_track(self, track):
        self._tracks.append(track)

        return self

    def count(self):
        return len(self._tracks)

    def __repr__(self):
        return '<Playlist {}>'.format(self._name)
