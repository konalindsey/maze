# see https://medium.com/@steveYeah/using-generics-in-python-99010e5056eb
from typing import Generic, TypeVar
T = TypeVar("T")  # allows variable T to be used to represent a generic type

from heapq import *
import random
import string

class Entry(Generic[T]):
    def __init__(self, priority: 'float|str', data: T):
        self._key   = priority
        self._value = data
    def __eq__(self, other):
        return self._key == other._key and self._value == other._value
    def __lt__(self, other):
        return self._key < other._key
    # not the Pythonic way to use __repr__ but allows us to print list of Entry
    def __repr__(self):
        key = f"'{self._key}'"   if isinstance(self._key,   str) else f"{self._key}"
        val = f"'{self._value}'" if isinstance(self._value, str) else f"{self._value}"
        return f"({key},{val})"
    def __str__(self):
        return repr(self)

class PriorityQueue(Generic[T]):
    __slots__ = ('_container')

    def __init__(self):
        self._container: List[T] = list()

    def __len__(self):
        return len(self._container)

    def is_empty(self):
        return len(self._container) == 0

    def insert(self, key: 'float|str', item: T):
        e = Entry(key, item)
        heappush(self._container, e)

    def remove_min(self) -> Entry:
        return heappop(self._container)


def main():
    # use PQ to sort integers at random between 1-100

    pq = PriorityQueue()
    for i in range(20):
        entry = Entry(random.randint(1,100), random.choice(string.ascii_letters))

        pq.insert(entry._key, entry._value)
        
    while not pq.is_empty():
        print(pq.remove_min())

#main()