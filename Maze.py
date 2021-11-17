# Changes required:
#  4) implement the A* algorithm as given in psuedocode in slides
# Then compare results of your BFS, DFS, and A* vs that shown in slides
# on the generated 10x10.
import copy

from Stack import *
from Queue import *
from PriorityQueue import *

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
    def __init__(self, cell: Cell, parent: Optional['Node'], cost: float, heuristic: float):
        self.cell = cell
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic

    def __str__(self):
        parent = "None" if self.parent is None else self.parent.cell
        return f"{self.cell} : parent = {parent}"

    def __lt__(self, other):
        return self.cost + self.heuristic < other.cost + other.heuristic


def manhattan(from_: Cell, to_: Cell) -> float:
    ''' the heuristic function for a star'''

    col_dist = abs(to_.get_position().col - from_.get_position().col)
    row_dist = abs(to_.get_position().row - from_.get_position().row)
    return row_dist + col_dist


class Maze:
    ''' class representing a 2D maxe of Cell objects '''

    _order = 0

    def __init__(self, rows: int = 10, cols: int = 10, prop_blocked: float = 0.2, start: Position = Position(0, 0),
                 goal: Position = Position(9, 9)):
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
        blocked = random.sample(options, k = round((rows * cols - 2) * prop_blocked))
        for b in blocked: b._contents = Contents.BLOCKED


        # pos = [(1,0),(1,3),(2,1),(2,4),(3,2),(5,1),(5,3),(5,4)]
        '''
        pos = [(1, 1), (1, 3), (2, 4), (3, 2), (5, 1), (5, 3), (5, 4)]
        for p in pos:
            self._grid[p[0]][p[1]]._contents = Contents.BLOCKED
        '''
    def __str__(self) -> str:
        ''' returns a str version of the maze, showing contents, with cells
            deliminted by vertical pipes '''
        maze_str = ""
        for row in self._grid:  # row : List[Cell]
            maze_str += "|" \
                        + "|".join([f"{int(cell._contents):2}" if not isinstance(cell._contents, str) else \
                                        f"{cell._contents:2}" for cell in row]) + "|\n"
        return maze_str[:-1]  # remove the final \n

    def get_start(self):
        return self._start

    def get_goal(self):
        return self._goal

    def get_search_locations(self, cell: Cell) -> List[Cell]:
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

        if row == self._num_rows - 1:
            pass
        else:
            s_cell = grid[row + 1][col]
            if s_cell.is_blocked(): invalid_cells.append(s_cell)
            if s_cell not in invalid_cells:
                cell_list.append(s_cell)
                invalid_cells.append(s_cell)
            if s_cell.is_blocked: invalid_cells.append(s_cell)

        if row == 0:
            pass
        else:
            n_cell = grid[row - 1][col]
            if n_cell.is_blocked(): invalid_cells.append(n_cell)
            if n_cell not in invalid_cells:
                cell_list.append(n_cell)
                invalid_cells.append(n_cell)

        if col == self._num_cols - 1:
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

    def dfs(self) -> tuple[Node, int]:
        search_count = 0
        stack = Stack()
        invalid_cells = [self._start]
        stack.push(Node(self._start, None, None, None))
        while not stack.is_empty():
            node = stack.pop()
            valid_list = self.get_search_locations(node.cell)

            for valid_cell in valid_list:
                if valid_cell not in invalid_cells:
                    search_count += 1
                    stack.push(Node(valid_cell, node, None, None))
                    invalid_cells.append(valid_cell)
                    if valid_cell == self._goal:
                        return Node(self._goal, node, None, None), search_count

    def bfs(self) -> tuple[Node, int]:
        search_count = 0
        queue = Queue()
        invalid_cells = [self._start]
        queue.push(Node(self._start, None, None, None))
        while not queue.is_empty():
            node = queue.pop()
            valid_list = self.get_search_locations(node.cell)

            for valid_cell in valid_list:
                if valid_cell not in invalid_cells:
                    search_count += 1
                    queue.push(Node(valid_cell, node, None, None))

                    invalid_cells.append(valid_cell)
                    if valid_cell == self._goal:
                        return Node(self._goal, node, None, None), search_count

    def a_star(self) -> tuple[Node, int]:
        search_count = 0
        to_explore = PriorityQueue()
        explored = dict()

        n = self._start
        g_n = 0.0
        h_n = manhattan(self._start, self._goal)

        f_n = g_n - h_n

        to_explore.insert(f_n, Node(n, None, g_n, h_n))
        explored[n._position] = g_n  # Cell not hashable, Position is hashable

        while to_explore.is_empty() == False:
            e = to_explore.remove_min()
            n = e._value

            if n.cell == self._goal: return n, search_count

            for m in self.get_search_locations(n.cell):
                g_m = g_n + 1
                if m._position not in explored.keys() or g_m < explored[m._position]:
                    search_count += 1
                    explored[m._position] = g_m
                    h_m = manhattan(m, self._goal)
                    f_m = g_m + h_m
                    to_explore.insert(f_m, Node(m, n, g_m, h_m))

    def show_path(self, node: Node) -> None:
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

    def path_length(self, node: Node) -> int:
        path = []
        while node.parent is not None:
            path.append(node.cell)
            node = node.parent
        path.append(node.cell)

        return len(path)

    def is_path_same(self, other, node, other_node) -> bool:
        path = []
        path2 = []

        while node.parent is not None:
            path.append(node.cell)
            node = node.parent
        path.append(node.cell)

        while other_node.parent is not None:
            path2.append(other_node.cell)
            other_node = other_node.parent
        path2.append(other_node.cell)

        return path == path2




def make_10x10_maze() -> Maze:
    ''' creates a maze like that shown in slides 28-32 of day 27 slides
    Returns:
        a Maze object
    '''
    rows = 10
    cols = 10
    p = 0

    # same maze as on page 47 of the Kopec book
    maze = Maze(rows, cols, start=Position(0, 0), \
                goal=Position(rows - 1, cols - 1), prop_blocked=p)

    # add the blocks at the appropriate spots
    blocks = [(0, 5), (0, 7), (1, 1), (2, 7), (3, 1), (3, 2), (3, 9), (4, 2), (5, 2), (5, 5), (6, 1), (8, 5), (8, 9)]
    for r, c in blocks:
        maze._grid[r][c]._contents = Contents.BLOCKED

    return maze


def one_experiment(maze_orig: Maze, show: bool = False):
    maze = maze_orig
    mazebfs = copy.deepcopy(maze)
    mazedfs = copy.deepcopy(maze)

    dfs = mazedfs.dfs()

    while dfs is not None:
        dfs_goal = dfs[0]
        dfs_count = dfs[1]
        dfs_length = mazedfs.path_length(dfs_goal)

        bfs = mazebfs.bfs()
        bfs_goal = bfs[0]
        bfs_count = bfs[1]
        bfs_length = mazebfs.path_length(bfs_goal)

        a_star = maze.a_star()
        a_star_goal = a_star[0]
        a_star_count = a_star[1]
        a_star_length = maze.path_length(a_star_goal)

        search_size = [dfs_count, bfs_count, a_star_count]
        path_length = [dfs_length, bfs_length, a_star_length]

        if show == True:
            mazedfs.show_path(dfs_goal)
            mazebfs.show_path(bfs_goal)
            maze.show_path(a_star_goal)

        return [search_size, path_length, a_star_length == bfs_length, mazedfs.is_path_same(maze, bfs_goal, a_star_goal)]
    else:
        return "This maze is not solvable"


def main():
    '''
    maze = make_10x10_maze()
    mazebfs = copy.deepcopy(maze)
    mazedfs = copy.deepcopy(maze)
    print(maze)
    print()

    print("Starting DFS")
    dfs = mazedfs.dfs()
    goal_node = dfs[0]
    count = dfs[1]

    if goal_node is not None:
        mazedfs.show_path(goal_node)
        print(f"DFS considered {count} cells")
    else:
        print("No solution using DFS")
    print()

    #####################################

    print("Starting BFS")
    bfs = mazebfs.bfs()
    goal_node = bfs[0]
    count = bfs[1]
    if goal_node is not None:
        mazebfs.show_path(goal_node)
        print(f"BFS considered {count} cells")
    else:
        print("No solution using BFS")
    print()

    #####################################

    print("Starting A *")
    a_star = maze.a_star()
    goal_node = a_star[0]
    count = a_star[1]
    if goal_node is not None:
        maze.show_path(goal_node)
        print(f"A-Star considered {count} cells")
    else:
        print("No solution using A*")
    print()
    '''
    for i in range(30):
        rows = random.randint(5,30)
        cols = random.randint(5,30)
        maze = Maze(rows, cols, .2, Position(0,0), Position(rows-1, cols-1))
        print(one_experiment(maze, show = False))


main()
