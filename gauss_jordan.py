from matrix import *
from functools import reduce


# row operations
def swap_rows(rows, i, j, display=None):
    rows[i], rows[j] = rows[j], rows[i]
    if display == 'latex':
        print('\\overset{E_{%d, %d}}{\\longrightarrow}'%(i+1, j+1))
        print_latex_code(rows)
    elif display == 'display':
        print('swap row {}, {}:'.format(i, j))
        display_mat(rows)

def scale_row(rows, k, s, display=None):
    rows[k] = [s*e for e in rows[k]]
    if display == 'latex':
        print('\\overset{E_{\\left(%s\\right)%d}}{\\longrightarrow}'%(str(s), k+1))
        print_latex_code(rows)
    elif display == 'display':
        print('scale row {} by {}:'.format(k, s))
        display_mat(rows)

def scale_and_add(rows, src, scale, dest, display=None):
    rows[dest] = [scale*oe+de for oe, de in zip(rows[src], rows[dest])]
    if display == 'latex':
        print('\\overset{E_{\\left(%s\\right)%d,%d}}{\\longrightarrow}'%(str(scale), src+1, dest+1))
        print_latex_code(rows)
    elif display == 'display':
        print('add row {} multiplied by {} to row {}:'.format(src, scale, dest))
        display_mat(rows)


def eliminate(mat, back=True, display=None):
    # return the row operation matrix

    check_matrix(mat)

    # display the orginal matrix
    if display == 'latex':
        print_latex_code(mat)
    elif display == 'display':
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
    A = augment(mat, idmat(r_num))

    for r in range(r_num):
        pivcol = pivot_col_pos(A[r:])
        if pivcol is None: break
        pivrow, pivot = 0, 0
        for i in range(r, r_num):
            entry = A[i][pivcol]
            if entry != 0:
                pivrow, pivot = i, entry
                break
        if pivrow != r:
            swap_rows(A, r, pivrow, display)
        if back and pivot != 1:
            scale_row(A, r, Fraction(1, pivot), display)
        for i in range(r+1, r_num):
            entry = A[i][pivcol]
            if entry == 0: continue
            scale_and_add(A, r, Fraction(-entry, A[r][pivcol]), i, display)
    # back substitution
    if back:
        for r in range(r_num-1, 0, -1):
            c = pivot_col_pos(A[r:])
            if not c: continue
            for i in range(r):
                entry = A[i][c]
                if entry != 0:
                    scale_and_add(A, r, -entry, i, display)

    mat[:], E = slice(A, 0, c_num), slice(A, c_num)
    return E


def inverse(m):
    assert(issquare(m))
    n = m.copy()
    inv = eliminate(n)
    assert(mat_eq(n, idmat(len(n))))
    return inv


def LU(m):
    n = m.copy()
    E = eliminate(n, False)
    return inverse(E), n


def det(m):
    assert(issquare(m))
    n = m.copy()
    eliminate(n, False)
    return reduce(lambda x, y: x*y, [n[i][i] for i in range(len(m))])