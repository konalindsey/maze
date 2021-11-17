# see https://medium.com/@steveYeah/using-generics-in-python-99010e5056eb
from typing import Generic, List, TypeVar

T = TypeVar("T")  # allows variable T to be used to represent a generic type

class EmptyError(Exception):
    ''' class extending Exception to better document queue errors '''
    def __init__(self, message: str):
        self.message = message

class Queue(Generic[T]):
    ''' class to implement a queue ADT using a Python list '''

    __slots__ = ("_data")           # will be a Python list

    def __init__(self):
        self._data: List[T] = []    # typing _data to be a list of type T

    def __len__(self) -> int:
        ''' allows the len function to be called using an Arrayqueue object, e.g.,
               queue = Arrayqueue()
               print(len(queue))
        Returns:
            number of elements in the queue, as an integer
        '''
        return len(self._data)

    def push(self, item: T) -> None: 
        ''' pushes a given item of arbitrary type onto the queue
        Args:
            item: an item of arbitrary type
        Returns:
            None
        '''
        self._data.append(item)

    def pop(self) -> T:
        ''' removes the topmost element from the queue and returns that element
        Returns:
            the topmost item, of arbitrary type
        Raises:
            EmptyError exception if the queue is empty
        '''
        if len(self._data) == 0:
            raise EmptyError('Error in Arrayqueue.pop(): queue is empty')
        return self._data.pop(0)

    def top(self) -> T:
        ''' returns the topmost element from the queue without modifying the queue
        Returns:
            the topmost item, of arbitrary type
        Raises:
            EmptyError exception if the queue is empty
        '''
        if len(self._data) == 0:
            raise EmptyError('Error in Arrayqueue.top(): queue is empty')
        return self._data[-1]

    def is_empty(self) -> bool:
        ''' indicates whether the queue is empty
        Returns:
            True if the queue is empty, False otherwise
        '''
        return len(self._data) == 0

    def __str__(self) -> str:
        ''' returns an str implementation of the Arrayqueue '''
        string = "---top---\n"
        for i in range(len(self._data) - 1, -1, -1):
            string += str(self._data[i]) + "\n"
        string += "---bot---"
        return string

'''
def main():
   # example using int as the generic type
   s = queue[int]()
   s.push(8)
   s.push(6)
   s.push(7)
   print(s)

   # example using str as the generic type
   s2 = queue[str]()
   s2.push("a")
   s2.push("b")
   s2.push("c")
   print(s2)
'''
