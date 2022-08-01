from utilities.constants import CellStatus


def negate(numbers):
    return [-num for num in numbers]


def calc_no(i, j, cells_a_row):
    return (cells_a_row * i) + j + 1

def getRange(markers, i, j):
    num_rows = len(markers)
    num_cols=len(markers[0])
    row_start = i - 1 if i > 0 else i
    row_end = i + 1 if i < num_rows - 1 else i
    col_start = j - 1 if j > 0 else j
    col_end = j + 1 if j < num_cols - 1 else j
    return row_start,row_end,col_start,col_end

def model_to_matrix(model, rows, cols):
    matrix_out = []
    for i in range(rows):
        matrix_out.append([])
        for j in range(cols):
            num = calc_no(i, j, rows)
            matrix_out[-1].append('1' if model[num - 1] > 0 else '0')
    return matrix_out


def count_cells_marked(markers, i, j):
    
    row_start,row_end,col_start,col_end=getRange(markers, i, j)

    count = 0
    for row in range(row_start, row_end + 1):
        for col in range(col_start, col_end + 1):
            if markers[row][col] == CellStatus.MARKED:
                count += 1

    return count


def validate(matrix, markers, num_rows, num_cols):
    for i in range(num_rows):
        for j in range(num_cols):
            if matrix[i][j] != -1:
                if count_cells_marked(markers, i, j) != matrix[i][j]:
                    return False
    return True


def calc_next_indices(num_rows, num_cols, i, j):
    if i == num_rows - 1 and j == num_cols - 1:
        return num_rows, num_cols

    next_i = i + 1 if j == num_cols - 1 else i
    next_j = 0 if j == num_cols - 1 else j + 1
    return next_i, next_j


def cell_to_indices(num, num_rows, num_cols):
    j = (num - 1) % num_cols
    i = (num - 1 - j) // num_rows
    return i, j


def set_cells(cells, markers, val):
    num_rows, num_cols = len(markers), len(markers[0])
    for num in cells:
        row, col = cell_to_indices(num, num_rows, num_cols)
        markers[row][col] = val


def get_cells(matrix, markers, i, j):
    row_start,row_end,col_start,col_end=getRange(markers, i, j)

    cells = []
    
    for row in range(row_start, row_end + 1):
        for col in range(col_start, col_end + 1):
            if markers[row][col] == CellStatus.UNMARKED:
                cell = calc_no(row, col, len(markers[0]))
                cells.append(cell)
            
    return cells, count_cells_marked(markers, i, j)

    
def remove_duplicate_clauses(clauses):
    clauses_sorted = [list(set(clause)) for clause in clauses]
    clauses_distinct = list(set([''.join(str(clause)) for clause in clauses_sorted]))
    return [list(map(int, clause.lstrip('[').rstrip(']').split(', '))) for clause in clauses_distinct]


def create_markers(matrix):
    markers = [[CellStatus.UNMARKED for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                num_rows = len(matrix)
                row_start = i - 1 if i > 0 else i
                row_end = i + 1 if i < num_rows - 1 else i
                col_start = j - 1 if j > 0 else j
                col_end = j + 1 if j < len(matrix[0]) - 1 else j

                for row in range(row_start, row_end + 1):
                    for col in range(col_start, col_end + 1):
                        markers[row][col] = CellStatus.BANNED
    return markers
