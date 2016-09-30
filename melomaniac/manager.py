# -*- coding: utf-8 -*-

import os
import yaml
from cachy import CacheManager

from .gmusic import Backend as GMusicBackend
from .soundcloud import Backend as SoundcloudBackend


class Manager(object):

    def __init__(self, command):
        self._backends = {}
        self._command = command
        self._home = os.path.join(os.path.expanduser('~'), '.melomaniac')
        self._config_file = os.path.join(self._home, 'config.yml')
        self._cache_dir = os.path.join(self._home, 'cache')
        self._cache = CacheManager({
            'stores': {
                'file': {
                    'driver': 'file',
                    'path': self._cache_dir
                }
            }
        })

        self.register([
            GMusicBackend(),
            SoundcloudBackend()
        ])

    @property
    def command(self):
        return self._command

    @property
    def home(self):
        return self._home

    @property
    def cache(self):
        return self._cache

    def config_exists(self):
        return os.path.exists(self._config_file)

    def register(self, backend):
        """
        Register a new backend.

        :param backend: The backend to register.
        :type backend: Backend

        :rtype: Manager
        """
        if isinstance(backend, list):
            for b in backend:
                self.register(b)
        else:
            self._backends[backend.name] = backend.set_manager(self)

        return self

    def get(self, name):
        """
        Return a backend given its name else None.

        :param name: The name of the backend to retrieve.
        :type name: str

        :rtype: Backend or None
        """
        return self._backends.get(name)

    def all(self):
        """
        Return all backends.

        :rtype: list
        """
        return list(self._backends.values())

    def load_config(self, name=None):
        with open(self._config_file) as fd:
            config = yaml.load(fd)

        if name:
            return config.get(name)

        return config

    def save_config(self, config, name=None):
        if os.path.exists(self._config_file):
            _config = self.load_config()
        else:
            _config = {}

        if name:
            _config[name] = config

        with open(self._config_file, 'w') as fd:
            yaml.dump(_config, fd)
