# -*- coding: utf-8 -*-


class Backend(object):
    """
    Base class for all music backends.
    """

    NAME = 'gmusic'

    LIBRARY_CLASS = None
    UI_CLASS = None

    CACHE_KEYS = []

    def __init__(self, manager=None, test=False):
        self._manager = manager
        self._test = test

    @property
    def name(self):
        return self.NAME

    @property
    def command(self):
        return self._manager.command

    @property
    def c(self):
        return self.command

    @property
    def cache(self):
        return self._manager.cache

    def cache_key(self, key):
        return '{}.{}'.format(self.name, key)

    def clear_cache(self):
        for key in self.CACHE_KEYS:
            self.cache.forget(self.cache_key(key))

    def config_exists(self):
        return self._manager.config_exists()

    def set_manager(self, manager):
        self._manager = manager

        return self

    def set_test(self, test):
        self._test = test

        return self

    def launch(self):
        raise NotImplementedError()

    def is_configured(self):
        raise NotImplementedError()

    def configure(self):
        raise NotImplementedError()

    def load_config(self):
        return self._manager.load_config(self.NAME)

    def save_config(self, config):
        self._manager.save_config(config, self.NAME)
