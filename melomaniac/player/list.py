# -*- coding: utf-8 -*-


class List(object):

    def __init__(self, name, items=None):
        self.name = name
        if items is None:
            items = []

        self.items = items

    def add_items(self, items):
        for item in items:
            self.add_item(item)

        return self

    def add_item(self, item):
        self.items.append(item)

        return self
