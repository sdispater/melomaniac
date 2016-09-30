# -*- coding: utf-8 -*-


class Library(object):

    def __init__(self, api, config):
        self._api = api
        self._config = config

    def get_url(self, track):
        raise NotImplementedError()
