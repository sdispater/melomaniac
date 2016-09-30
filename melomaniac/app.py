# -*- coding: utf-8 -*-

from cleo import Application

from .version import VERSION
from .commands.listen import ListenCommand
from .commands.cache_clear import CacheClearCommand


app = Application('Melomaniac', VERSION)

app.add(ListenCommand())
app.add(CacheClearCommand())
