from solve_system import *

# let a basis be an invertible square matrix, each column of which is a basis vector
# then "a vector v is in the span of a basis B" is equivalent to "Bx = v is consistent"
# the coords of v with regard to B is inv(B)v

def coords_transform(B):
    Inv = inverse(B)
    return lambda v: [dotp(row, v) for row in transpose(B)]

def coords(B, v):
    return coords_transform(B)(v)

def coord_matrix(T, B1, B2):
    S = coords_transform(B2)
    return transpose([S(transpose(v)) for v in multm(T, B1)])


### test
B = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]
v = [3,5,2]
print(coords(v, B))