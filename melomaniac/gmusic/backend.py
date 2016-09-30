# -*- coding: utf-8 -*-

from gmusicapi import Mobileclient
from ..contracts.backend import Backend as BaseBackend
from ..player.player import Player
from .library import Library
from .test_library import TestLibrary
from .ui import UI


class Backend(BaseBackend):

    NAME = 'gmusic'

    LIBRARY_CLASS = Library
    UI_CLASS = UI

    CACHE_KEYS = [
        'library'
    ]

    def __init__(self, manager=None, test=False):
        super(Backend, self).__init__(manager, test)

        self._api = Mobileclient()

    @property
    def api(self):
        return self._api

    def launch(self):
        library = self.load()
        ui = self.UI_CLASS(Player(library))
        ui.launch()

    def load(self):
        if self._test:
            return TestLibrary

        self.c.line('<comment>-</> Loading config.')
        self.config = self.load_config()

        self.c.line('<comment>-</> Connecting to Google Play Music.')
        self._api.login(
            self.config['user'], self.config['password'],
            self.config.get('device_id', Mobileclient.FROM_MAC_ADDRESS)
        )

        if not self._api.is_authenticated():
            raise RuntimeError('Unable to authenticate. Please verify your credentials.')

        library = Library(self)

        self.c.line('<comment>-</> Loading library.')
        l = library.get()
        self.c.line('<comment>-</> Loaded <info>{}</info> albums, <info>{}</> tracks'.format(len(l['albums']), len(l['_default'])))
        self.c.line('<comment>-</> Loading playlists.')
        library.get_playlists()

        return library

    def is_configured(self):
        if self._test:
            return True

        if not self.config_exists():
            return False

        config = self.load_config()
        if config is None:
            return False

        return self.check_config(config)

    def check_config(self, config):
        errors = []
        if 'user' not in config:
            errors.append('<comment>Missing [<info>user</>] in config.</>')

        if 'password' not in config:
            errors.append('<comment>Missing [<info>password</>] in config.</>')

        if not errors:
            return True

        self.c.list(errors)

        return False

    def configure(self):
        self.c.output.title('Welcome to <fg=cyan>Melomaniac</>')
        self.c.line('It seems that this your first time using the <fg=cyan>{}</> backend.'.format(self.NAME))
        self.c.line('Please respond to the next few questions.'
                    'The responses will be saved in <comment>~/.melomaniac.yml</>.')

        user_question = '<question>Please enter your username:</> '
        user = self.c.ask(user_question)

        password_question = '<question>Please enter your password:</> '
        password = self.c.secret(password_question)

        self.save_config({
            'user': user,
            'password': password
        })

    def close(self):
        if self.api:
            self.api.logout()
