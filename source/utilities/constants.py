import platform

class CellStatus:
    BANNED = None
    MARKED = True
    UNMARKED = False

class CellSize:
    WIDTH = 9
    HEIGHT = 4

class Algorithm:
    NONE = -1
    PYSAT = 0
    A_STAR = 1
    BRUTE_FORCE = 2
    BACKTRACKING = 3

class ScrollConst:
    MODIFIER = 120
