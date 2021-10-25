from Stack import *
from Queue import *
from copy import deepcopy
from enum import Enum
from typing import List, NamedTuple, Optional
import random



class Contents(str, Enum):
    ''' create an enumeration to define what the visual contents of a Cell are;
        using str as a "mixin" forces all the entries to be strings; using an
        enum means no cell entry can be anything other than the options here
    '''
    EMPTY = " "
    START = "⦿"  # "S"
    GOAL = "◆"  # "G"
    BLOCKED = "░"  # "X"
    PATH = "★"  # "*"


class Position(NamedTuple):
    row: int
    col: int


class Cell:
    ''' allows us to use Cell as a data type -- an ordered triple of 
        row, column, cell contents '''

    def __init__(self, row: int, col: int, contents: Contents):
        self._position = Position(row, col)
        self._contents = contents

    def get_position(self) -> Position:
        return Position(self._position.row, self._position.col)

    def mark_on_path(self) -> None:
        self._contents = Contents.PATH

    def is_blocked(self) -> bool:
        return self._contents == Contents.BLOCKED

    def is_goal(self) -> bool:
        return self._contents == Contents.GOAL

    def __str__(self) -> str:
        contents = "[EMPTY]" if self._contents == Contents.EMPTY else self._contents
        return f"({self._position.row}, {self._position.col}): {contents}"

    def __eq__(self, other) -> bool:
        return self._position.row == other._position.row and \
               self._position.col == other._position.col and \
               self._contents == other._contents


class Node:
    def __init__(self, cell: Cell, parent: Optional['Node']):
        self.cell = cell
        self.parent = parent

    def __str__(self):
        parent = "None" if self.parent is None else self.parent.cell
        return f"{self.cell} : parent = {parent}"


class Maze:
    ''' class representing a 2D maxe of Cell objects '''
    rows = random.randint(5,150)
    cols = random.randint(5,150)

    def __init__(self, rows: int = rows, cols: int = cols, prop_blocked: float = 0.6, start: Position = Position(0, 0),
                 goal: Position = Position(rows-1, cols-1)):
        '''
        Args:
            rows:          number of rows in the grid
            cols:          number of columns in the grid
            prop_blocked:  proportion of cells to be blocked
            start:         tuple indicating the (row,col) of the start cell
            goal:          tuple indicating the (row,col) of the goal cell
        '''
        self._num_rows = rows
        self._num_cols = cols
        self._start = Cell(start.row, start.col, Contents.START)
        self._goal = Cell(goal.row, goal.col, Contents.GOAL)

        # create a rows x cols 2D list of Cell objects, intially all empty
        self._grid: List[List[Cell]] = \
            [[Cell(r, c, Contents.EMPTY) for c in range(cols)] for r in range(rows)]

        # set the start and goal cells
        self._grid[start.row][start.col] = self._start
        self._grid[goal.row][goal.col] = self._goal

        # put blocks at random spots in the grid, using given proportion;  
        # start by creating a collapsed 1D version of the grid, then
        #   remove the start and goal, and then randomly pick cells to block;
        # note that we are using identical object references in both 
        #   options and self._grid so that updates to options will be seen
        #   in self._grid (i.e., options is not a deep copy of cells)
        options = [cell for row in self._grid for cell in row]
        options.remove(self._start)
        options.remove(self._goal)
        blocked = random.sample(options, k=round((rows * cols - 2) * prop_blocked))
        for b in blocked: b._contents = Contents.BLOCKED
        '''
        # for example from slides
        pos = [(1,0),(1,3),(2,1),(2,4),(3,2),(5,1),(5,3),(5,4)]
        for p in pos:
            self._grid[p[0]][p[1]]._contents = Contents.BLOCKED
        '''

    def __str__(self) -> str:
        ''' returns a str version of the maze, showing contents, with cells
            deliminted by vertical pipes '''
        maze_str = ""
        for row in self._grid:  # row : List[Cell] 
            maze_str += "|" + "|".join([cell._contents for cell in row]) + "|\n"
        return maze_str[:-1]  # remove the final \n

    def get_start(self):
        return self._start

    def get_goal(self):
        return self._goal

    def get_search_locations(self, cell: Cell) -> List[Cell]:
        ''' return a list of Cell objects of valid places to explore
        Args:
            cell: the current cell being explored
        Returns:
            a list of valid Cell objects for further exploration
        '''
        cell_list = []
        invalid_cells = [self._start]
        grid = self._grid
        '''
        for cells in grid:
            for ccell in cells:
                if ccell.is_blocked() == True:
                    invalid_cells.append(ccell)
        '''
        row = cell._position[0]
        col = cell._position[1]

        if row == self._num_rows -1:
            pass
        else:
            s_cell = grid[row+1][col]
            if s_cell.is_blocked(): invalid_cells.append(s_cell)
            if s_cell not in invalid_cells:
                cell_list.append(s_cell)
                invalid_cells.append(s_cell)
            if s_cell.is_blocked: invalid_cells.append(s_cell)

        if row == 0:
            pass
        else:
            n_cell = grid[row-1][col]
            if n_cell.is_blocked(): invalid_cells.append(n_cell)
            if n_cell not in invalid_cells:
                cell_list.append(n_cell)
                invalid_cells.append(n_cell)

        if col == self._num_cols -1:
            pass
        else:
            e_cell = grid[row][col + 1]
            if e_cell.is_blocked(): invalid_cells.append(e_cell)
            if e_cell not in invalid_cells:
                cell_list.append(e_cell)
                invalid_cells.append(e_cell)

        if col == 0:
            pass
        else:
            w_cell = grid[row][col - 1]
            if w_cell.is_blocked(): invalid_cells.append(w_cell)
            if w_cell not in invalid_cells:
                cell_list.append(w_cell)
                invalid_cells.append(w_cell)


        return cell_list

    def dfs(self) -> bool:
        ''' 
        Use DFS + stack:
            stack: push new cells to be explored
            list:  cells already explored
        Return:
            current node if it is the goal
            None, if no goal can be found
        '''

        stack = Stack()
        invalid_cells = [self._start]
        stack.push(Node(self._start,None))
        while not stack.is_empty():
            node = stack.pop()
            valid_list = self.get_search_locations(node.cell)

            for valid_cell in valid_list:
                if valid_cell not in invalid_cells:
                    stack.push(Node(valid_cell, node))
                    self.show_path(node)
                    invalid_cells.append(valid_cell)
                    if valid_cell == self._goal:
                        return Node(self._goal, node)

    def bfs(self) -> Node:
        '''
        Use BFS + queue:
            queue: push new cells to be explored
            list:  cells already explored
        Return:
            current node if it is the goal
            None, if no goal can be found
        '''
        queue = Queue()
        invalid_cells = [self._start]
        queue.push(Node(self._start, None))
        while not queue.is_empty():
            node = queue.pop()
            valid_list = self.get_search_locations(node.cell)

            for valid_cell in valid_list:
                if valid_cell not in invalid_cells:
                    queue.push(Node(valid_cell, node))

                    invalid_cells.append(valid_cell)
                    if valid_cell == self._goal:
                        return Node(self._goal, node)



    def show_path(self, node: Node) -> None:
        try:
            path = []
            while node.parent is not None:
                path.append(node.cell)
                node = node.parent
            path.append(node.cell)

            path.reverse()

            for cell in path:
                if cell != self._start and cell != self._goal:
                    cell.mark_on_path()
            print(self)
            print()
        except AttributeError: print("Maze is impossible! Please choose a different maze")



def main():
    maze = Maze()
    print(maze)
    #print("Starting dfs")
    #goal = maze.dfs()
    #print(maze.show_path(goal))
    print()
    goal = maze.bfs()
    #print("Starting bfs")
    #print(maze.bfs())
    print(maze.show_path(goal))

main()