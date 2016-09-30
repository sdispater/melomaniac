# -*- coding: utf-8 -*-

from cleo import Command

from ..manager import Manager


class CacheClearCommand(Command):
    """
    Clear cache.

    cache:clear
        {backends?* : The backends to clear the cache for.}
    """

    def handle(self):
        manager = Manager(self)

        backends = self.argument('backends')
        if backends:
            for backend in backends:
                self.line('<comment>Clearing cache</> for <fg=cyan>{}</>'.format(backend))
                manager.get(backend).clear_cache()
        else:
            for backend in manager.all():
                self.line('<comment>Clearing cache</> for <fg=cyan>{}</>'.format(backend.name))
                backend.clear_cache()
