def check_matrix(list_2D):
    assert isinstance(list_2D, list)
    assert all(map(lambda l: isinstance(l, list), list_2D))
    assert len(set([len(l) for l in list_2D])) == 1

def display_mat(mat):
    for i in range(rows_num(mat)):
        for j in range(cols_num(mat)):
            print(mat[i][j], end=' ')
        print()
    print('------------------')

def print_latex_code(mat):
    print('\\begin{bmatrix}')
    print(' \\\\ '.join([' & '.join(map(str,row)) for row in mat]))
    print('\\end{bmatrix}')

def rows_num(rows):
    return len(rows)

def cols_num(rows):
    return len(rows[0])

def row(rows, k):
    assert k < rows_num(rows)
    return rows[k]

def col(rows, k):
    assert k < cols_num(rows)
    return [row[k] for row in rows]

def dotp(v1, v2):
    assert len(v1) == len(v2)
    return sum([a1*a2 for a1,a2 in zip(v1, v2)])

def mult_mat(m1, m2):
    assert cols_num(m1) == rows_num(m2)
    return [[dotp(row, col(m2, c)) for c in range(cols_num(m2))] for row in m1]