from collections import OrderedDict


class LRUCache:

    def __init__(self, capacity):
        self.k = capacity
        self.d = OrderedDict()

    def get(self, key: int):
        if key not in self.d:
            return -1

        item = self.d[key]
        self.d.move_to_end(key)
        return item

    def put(self, key: int, value) -> None:
        if key in self.d:
            self.d.move_to_end(key)

        self.d[key] = value
        if len(self.d) > self.k:
            self.d.popitem(last=False)

    def remove(self, key):
        if key in self.d:
            self.d.pop(key)
