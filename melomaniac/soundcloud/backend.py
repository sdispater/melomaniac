# -*- coding: utf-8 -*-

import os
import requests

from ..contracts.backend import Backend as BaseBackend
from .client import Client
from ..player.player import Player
from .library import Library
from .ui import UI


class Backend(BaseBackend):

    NAME = 'soundcloud'

    LIBRARY_CLASS = Library
    UI_CLASS = UI

    def __init__(self, manager=None, test=False):
        super(Backend, self).__init__(manager, test)

        self._api = None

    @property
    def api(self):
        return self._api

    def launch(self):
        library = self.load()
        ui = self.UI_CLASS(Player(library))
        ui.launch()

    def load(self):
        self.c.line('<comment>-</> Loading config.')
        config = self.load_config()

        self.c.line('<comment>-</> Connecting to SoundCloud.')
        self._api = Client(access_token=config['access_token'])

        library = Library(self)

        self.c.line('<comment>-</> Loading stream.')
        library.get_stream()

        self.c.line('<comment>-</> Loading favorites.')
        library.get_favorites()

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

        if not errors:
            return True

        self.c.list(errors)

        return False

    def configure(self):
        self.c.output.title('Welcome to <fg=cyan>Melomaniac</>')
        self.c.line('It seems that this your first time using the <fg=cyan>{}</> backend.'.format(self.NAME))
        self.c.line('Please respond to the next few questions.'
                    'The responses will be saved in <comment>~/.melomaniac.yml</>.')

        client_id_question = '<question>Please enter your client ID:</> '
        client_id = self.c.ask(client_id_question)

        client_secret_question = '<question>Please enter your client secret:</> '
        client_secret = self.c.secret(client_secret_question)

        # Asking for credentials
        self.c.line('The next few questions will ask for a username and a passwword.')
        self.c.line('They will just be used once to get an access token and will never be stored.')

        user_question = '<question>Please enter your username:</> '
        user = self.c.ask(user_question)

        password_question = '<question>Please enter your password:</> '
        password = self.c.secret(password_question)

        api = Client(
            client_id=client_id,
            client_secret=client_secret,
            username=user,
            password=password
        )

        access_token = api.access_token
        refresh_token = api.token.refresh_token

        self.save_config({
            'client_id': client_id,
            'client_secret': client_secret,
            'access_token': access_token,
            'refresh_token': refresh_token,
        })

    def close(self):
        pass

    def get(self, url, **kwargs):
        try:
            return self.api.get(url, **kwargs)
        except requests.HTTPError as e:
            if e.response.status_code in [401, 503]:
                if self.try_reconnect():
                    return self.get(url, **kwargs)

            raise

    def try_reconnect(self):
        config = self.load_config()
        refresh_token = config['refresh_token']
        client_secret = config['client_secret']

        api = Client(
            client_id=config['client_id'],
            client_secret=client_secret,
            refresh_token=refresh_token
        )

        config['access_token'] = api.access_token
        config['refresh_token'] = api.token.refresh_token

        self.save_config(config)
        self._api = Client(access_token=api.access_token)

        return True
