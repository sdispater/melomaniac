# -*- coding: utf-8 -*-

import threading
import pexpect
from pexpect import TIMEOUT


class Player(object):

    KEY_SPACE = ' '
    KEY_UP = '\x1b[A'
    KEY_DOWN = '\x1b[B'
    KEY_RIGHT = '\x1b[C'
    KEY_LEFT = '\x1b[D'

    def __init__(self, library):
        self._library = library
        self.track = None
        self.track_percent = 0
        self.track_total = 0
        self.track_current = 0
        self.queue = []
        self.queue_number = 0
        self.queue_length = 0
        self.playing = None
        self.active = False
        self.loading = False

    @property
    def library(self):
        return self._library

    @property
    def status(self):
        if self.is_playing():
            return 'Playing'
        elif self.is_paused():
            return 'Paused'
        elif self.loading:
            return 'Loading'
        else:
            return 'Stopped'

    def play(self, n=None):
        if self.is_paused():
            self.active = True
            self.playing.send(' ')
        else:
            self.queue_number = n or self.queue_number
            self.track = self.queue[self.queue_number]

            self._play()

    def _play(self):
        self.track_current = 0
        self.track_percent = 0

        self.loading = True
        url = self.track.url
        self.playing = pexpect.spawn(
            'mpv',
            ["--no-ytdl", "%s" % url],
            timeout=None
        )
        self.active = True
        self.loading = False

        thread = threading.Thread(target=self._monitor, args=(self.playing, self))
        thread.daemon = True
        thread.start()

    def _monitor(self, p, s):
        cpl = p.compile_pattern_list([
            pexpect.EOF,
            "A: (\d{2}):(\d{2}):(\d{2}) \/ (\d{2}):(\d{2}):(\d{2}) \((\d+)%\)"
        ])

        while True:
            try:
                i = p.expect_list(cpl, timeout=5)
            except TIMEOUT:
                continue

            if i == 0:
                # End of song
                s.stop()

                break
            elif i == 1:
                m = p.match

                hour_current = int(m.group(1))
                minute_current = int(m.group(2))
                second_current = int(m.group(3))
                percent = int(m.group(7))

                s.track_current = hour_current * 3600 + minute_current * 60 + second_current
                s.track_percent = int(percent)

    def is_playing(self):
        return self.has_playing() and self.active

    def is_paused(self):
        return self.has_playing() and not self.active

    def has_playing(self):
        return isinstance(self.playing, pexpect.spawn)

    def has_next(self):
        return self.queue_number < len(self.queue) - 1

    def next(self):
        self.play(self.queue_number + 1)

    def previous(self):
        self.play(self.queue_number - 1)

    def stop(self):
        if self.is_playing():
            self.playing.terminate()
            self.playing = None
            self.active = False
            self.track = None

    def toggle(self):
        if self.is_playing():
            self.pause()
        else:
            self.play()

    def pause(self):
        self.playing.send(self.KEY_SPACE)
        self.active = False

    def forward(self):
        if self.is_playing():
            self.playing.send(self.KEY_RIGHT)

    def rewind(self):
        if self.is_playing():
            self.playing.send(self.KEY_LEFT)
