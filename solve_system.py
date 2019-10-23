from matrix import *
from gauss_jordan import *


def check_correct(A, X, B):
    if mat_eq(multm(A, X), B):
        print('CORRECT!\n')
    else:
        raise ValueError('I cannot get the correct answer!')


def GJsolve(A, B):
    AUG = augment(A, B)
    eliminate(AUG)
    X = slice(AUG, cols_num(A))
    check_correct(A, X, B)
    return X


def solveTriang(M, B, direction='up', display=None):
    unknowns = cols_num(M)
    eqs = rows_num(M)
    assert(unknowns == eqs == rows_num(B))

    ans = [None] * unknowns
    mulc = 0
    if direction == 'up':
        for i in range(unknowns-1, -1, -1):
            b = B[i]
            for j in range(i+1, unknowns):
                b = subv(b, scalev(ans[j], M[i][j]))
                mulc += 1
            ans[i] = scalev(b, Fraction(1,M[i][i]))
            mulc += 1
    elif direction == 'lo':
        for i in range(unknowns):
            b = B[i]
            for j in range(i):
                b = subv(b, scalev(ans[j], M[i][j]))
                mulc += 1
            ans[i] = scalev(b, Fraction(1,M[i][i]))
            mulc += 1

    # print('uses %s muls' % mulc)
    if display == 'display':
        display_mat(ans)
    elif display == 'latex':
        print_latex_code(ans)
    return ans


def solve(A, B):
    cn = cols_num(A)
    M = augment(A, B)
    eliminate(M, False)
    X = solveTriang(slice(M, 0, cn), slice(M, cn))
    check_correct(A, X, B)
    return X


def Jacobi_iter(A, B, X, n=100):
    D = diag(A)
    invD = map_mat(lambda x: 0 if x == 0 else Fraction(1, x), D)
    yield X
    for i in range(n):
        X = multm(invD, addm(B, multm(subm(D, A), X)))
        yield X

def GaussSeidel_iter(A, B, X, n=100):
    DL = [[A[r][c] if c <= r else 0 for c in range(cols_num(A))] for r in range(len(A))]
    invDL = inverse(DL)
    U = upper(A)
    yield X
    for i in range(n):
        X = multm(invDL, subm(B, multm(U, X)))
        yield X


### TEST ###
A = read_mat("""9 0 3 4 0 0
0 9 0 0 0 6
1 2 9 0 0 0
1 0 0 9 0 0
0 0 3 4 9 0
1 0 3 0 0 9""")
B = read_mat("""16
15
12
10
16
13""")
solve(A, B)
Xinit = [[0] for i in range(6)]
for X in Jacobi_iter(A, B, Xinit, 3):
    pass
for Y in GaussSeidel_iter(A, B, Xinit, 3):
    pass
X_err = [x-1 for x in transpose(X)[0]]
Y_err = [y-1 for y in transpose(Y)[0]]
print(round(float(dotp(X_err, X_err)), 5))
print(round(float(dotp(Y_err, Y_err)), 5))