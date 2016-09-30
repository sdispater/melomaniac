# -*- coding: utf-8 -*-

import os
import yaml
from cleo import Command
from backpack import collect

from ..manager import Manager


class ListenCommand(Command):
    """
    Launch the player and listen to music :)

    listen
        {backend=gmusic : The backend to connect to. One of <info>gmusic</> or <info>soundcloud</>}
        {--t|test : Activate test mode.}
        {--c|config : Force reconfiguration.}
        {--clear-cache : Clear the cache (if any)}
    """

    def __init__(self):
        super(ListenCommand, self).__init__()

        self.manager = Manager(self)

    def handle(self):
        backend = self.manager.get(self.argument('backend'))
        if not backend:
            raise ValueError('Backend [{}] does not exist.'.format(backend))

        backend.set_test(self.option('test'))

        if self.option('clear-cache'):
            backend.clear_cache()

        if not backend.is_configured() or self.option('config'):
            backend.configure()

        try:
            backend.launch()
        except Exception:
            backend.close()

            raise

        backend.close()

