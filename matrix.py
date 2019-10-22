from fractions import Fraction

def check_matrix(list_2D):
    assert isinstance(list_2D, list)
    assert all(map(lambda l: isinstance(l, list), list_2D))
    assert len(set([len(l) for l in list_2D])) == 1

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

# row operations
def swap_rows(rows, i, j, display):
    rows[i], rows[j] = rows[j], rows[i]
    if display == 'latex':
        print('\\overset{E_{%d, %d}}{\\longrightarrow}'%(i+1, j+1))
        print_latex_code(rows)
    elif display == 'normal':
        print('swap row {}, {}:'.format(i, j))
        display_mat(rows)

def scale_row(rows, k, s, display):
    rows[k] = [s*e for e in rows[k]]
    if display == 'latex':
        print('\\overset{E_{\\left(%s\\right)%d}}{\\longrightarrow}'%(str(s), k+1))
        print_latex_code(rows)
    elif display == 'normal':
        print('scale row {} by {}:'.format(k, s))
        display_mat(rows)

def scale_and_add(rows, src, scale, dest, display):
    rows[dest] = [scale*oe+de for oe, de in zip(rows[src], rows[dest])]
    if display == 'latex':
        print('\\overset{E_{\\left(%s\\right)%d,%d}}{\\longrightarrow}'%(str(scale), src+1, dest+1))
        print_latex_code(rows)
    elif display == 'normal':
        print('add row {} multiplied by {} to row {}:'.format(src, scale, dest))
        display_mat(rows)

def eliminate(mat, back=True, fraction_mode=True, display=None):
    check_matrix(mat)

    # display the orginal matrix
    if display == 'latex':
        print_latex_code(mat)
    elif display == 'normal':
        display_mat(mat)

    def all_zero(vect):
        return all(x == 0 for x in vect)
    def pivot_col_pos(rows):
        c_num = cols_num(rows)
        for i in range(c_num):
            if not all_zero(col(rows, i)):
                return i

    r_num = rows_num(mat)
    c_num = cols_num(mat)
    for r in range(r_num):
        pivcol = pivot_col_pos(mat[r:])
        if pivcol is None: break
        pivrow, pivot = 0, 0
        for i in range(r, r_num):
            entry = mat[i][pivcol]
            if entry != 0:
                pivrow, pivot = i, entry
                break
        if pivrow != r:
            swap_rows(mat, r, pivrow, display)
        if pivot != 1:
            if fraction_mode:
                scale_row(mat, r, Fraction(1, pivot), display)
            else:
                scale_row(mat, r, 1/pivot, display)
        for i in range(r+1, r_num):
            entry = mat[i][pivcol]
            if entry == 0: continue
            scale_and_add(mat, r, -entry, i, display)
    # back substitution
    if back:
        for r in range(r_num-1, 0, -1):
            c = pivot_col_pos(mat[r:])
            if not c: continue
            for i in range(r):
                entry = mat[i][c]
                if entry != 0:
                    scale_and_add(mat, r, -entry, i, display)
    return mat


def addv(v1, v2):
    return [a1+a2 for a1, a2 in zip(v1, v2)]

def dotp(v1, v2):
    assert len(v1) == len(v2)
    return sum([a1*a2 for a1,a2 in zip(v1, v2)])

def addm(m1, m2):
    assert rows_num(m1) == rows_num(m2) and cols_num(m1) == cols_num(m2)
    return [addv(v1, v2) for v1, v2 in zip(m1, m2)]

def multm(m1, m2):
    assert cols_num(m1) == rows_num(m2)
    return [[dotp(row, col(m2, c)) for c in range(cols_num(m2))] for row in m1]

def eval_mat(mstr):
    return [[eval(e) for e in r.split(',')] for r in mstr.splitlines()]

m = eval_mat("""1, 0, 3, 4, 0, 0
0, 2, 0, 0, 0, 6
1, 0, 0, 4, 0, 0
0, 0, 3, 4, 5, 0
1, 2, 3, 0, 0, 0
1, 0, 3, 0, 0, 6""")

eliminate(m, False, True, 'normal')