# see https://medium.com/@steveYeah/using-generics-in-python-99010e5056eb
from typing import Generic, List, TypeVar

T = TypeVar("T")  # allows variable T to be used to represent a generic type

class EmptyError(Exception):
    ''' class extending Exception to better document stack errors '''
    def __init__(self, message: str):
        self.message = message

class Stack(Generic[T]):
    ''' class to implement a stack ADT using a Python list '''

    __slots__ = ("_data")           # will be a Python list

    def __init__(self):
        self._data: List[T] = []    # typing _data to be a list of type T

    def __len__(self) -> int:
        ''' allows the len function to be called using an ArrayStack object, e.g.,
               stack = ArrayStack()
               print(len(stack))
        Returns:
            number of elements in the stack, as an integer
        '''
        return len(self._data)

    def push(self, item: T) -> None: 
        ''' pushes a given item of arbitrary type onto the stack
        Args:
            item: an item of arbitrary type
        Returns:
            None
        '''
        self._data.append(item)

    def pop(self) -> T:
        ''' removes the topmost element from the stack and returns that element
        Returns:
            the topmost item, of arbitrary type
        Raises:
            EmptyError exception if the stack is empty
        '''
        if len(self._data) == 0:
            raise EmptyError('Error in ArrayStack.pop(): stack is empty')
        return self._data.pop()  # calling Python list pop()

    def top(self) -> T:
        ''' returns the topmost element from the stack without modifying the stack
        Returns:
            the topmost item, of arbitrary type
        Raises:
            EmptyError exception if the stack is empty
        '''
        if len(self._data) == 0:
            raise EmptyError('Error in ArrayStack.top(): stack is empty')
        return self._data[-1]

    def is_empty(self) -> bool:
        ''' indicates whether the stack is empty
        Returns:
            True if the stack is empty, False otherwise
        '''
        return len(self._data) == 0

    def __str__(self) -> str:
        ''' returns an str implementation of the ArrayStack '''
        string = "---top---\n"
        for i in range(len(self._data) - 1, -1, -1):
            string += str(self._data[i]) + "\n"
        string += "---bot---"
        return string

'''
def main():
   # example using int as the generic type
   s = Stack[int]()
   s.push(8)
   s.push(6)
   s.push(7)
   print(s)

   # example using str as the generic type
   s2 = Stack[str]()
   s2.push("a")
   s2.push("b")
   s2.push("c")
   print(s2)
'''
