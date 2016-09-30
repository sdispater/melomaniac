# -*- coding: utf-8 -*-


class Library(object):

    def __init__(self, backend):
        self._backend = backend

    @property
    def cache(self):
        return self._backend.cache

    def cache_key(self, key):
        return self._backend.cache_key(key)

    def get_url(self, track):
        raise NotImplementedError()
