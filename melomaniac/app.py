# -*- coding: utf-8 -*-

from cleo import Application

from .version import VERSION
from .commands.listen import ListenCommand


app = Application('Melomaniac', VERSION)

app.add(ListenCommand())
