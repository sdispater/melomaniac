# -*- coding: utf-8 -*-


class Track(object):

    def __init__(self, library, id, title, artist, album, number, disc_number, metadata=None):
        self._library = library
        self.id = id
        self.title = title
        self.artist = artist
        self.album = album
        self.number = number
        self.disc_number = disc_number

        if metadata is None:
            metadata = {}

        self.metadata = metadata

    @property
    def url(self):
        return self._library.get_url(self)

    @property
    def duration(self):
        # gmusic
        if 'durationMillis' in self.metadata:
            return int(self.metadata['durationMillis']) // 1000

        # soundcloud
        if 'duration' in self.metadata:
            return int(self.metadata['duration']) // 1000

        return 0

    @property
    def duration_string(self):
        duration = self.duration
        minute = duration // 60
        second = duration % 60

        return '{:02d}:{:02d}'.format(minute, second)

    def __getitem__(self, item):
        return self.metadata[item]

    def __repr__(self):
        return '<Track {} by {} on {} [#{}]>'.format(
            self.title, self.artist, self.album, self.number
        )
