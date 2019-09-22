from matrix import *
from fractions import Fraction

def swap_row(rows, i, j, LaTeX_code):
    rows[i], rows[j] = rows[j], rows[i]
    if LaTeX_code:
        print('\\overset{E_{%d, %d}}{\\longrightarrow}'%(i+1, j+1))
        print_latex_code(rows)
    else:
        print('swap row {}, {}:'.format(i, j))
        display_mat(rows)

def scale_row(rows, k, s, LaTeX_code):
    rows[k] = [s*e for e in rows[k]]
    if LaTeX_code:
        print('\\overset{E_{\\left(%s\\right)%d}}{\\longrightarrow}'%(str(s), k+1))
        print_latex_code(rows)
    else:
        print('scale row {} by {}:'.format(k, s))
        display_mat(rows)

def scale_and_add(rows, src, scale, dest, LaTeX_code):
    rows[dest] = [scale*oe+de for oe, de in zip(rows[src], rows[dest])]
    if LaTeX_code:
        print('\\overset{E_{\\left(%s\\right)%d,%d}}{\\longrightarrow}'%(str(scale), src+1, dest+1))
        print_latex_code(rows)
    else:
        print('add row {} multiplied by {} to row {}:'.format(src, scale, dest))
        display_mat(rows)


def all_zero(vect):
    return all(map(lambda x: x == 0, vect))

def pivot_col_pos(rows):
    c_num = cols_num(rows)
    for i in range(c_num):
        if not all_zero(col(rows, i)):
            return i

def Gauss_Jordan(mat, fraction_mode=True, LaTeX_code=False):
    check_matrix(mat)
    if LaTeX_code:
        print_latex_code(mat)
    else:
        display_mat(mat)

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
            swap_row(mat, r, pivrow, LaTeX_code)
        if pivot != 1:
            if fraction_mode:
                scale_row(mat, r, Fraction(1, pivot), LaTeX_code)
            else:
                scale_row(mat, r, 1/pivot, LaTeX_code)
        for i in range(r+1, r_num):
            entry = mat[i][pivcol]
            if entry == 0: continue
            scale_and_add(mat, r, -entry, i, LaTeX_code)

    for r in range(r_num-1, 0, -1):
        c = pivot_col_pos(mat[r:])
        if not c: continue
        for i in range(r):
            entry = mat[i][c]
            if entry != 0:
                scale_and_add(mat, r, -entry, i, LaTeX_code)
