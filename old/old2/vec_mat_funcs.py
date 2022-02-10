# Tynan McGee
# 4/25/2021
# vector/matrix functions using my fraction "library"

from fraction import Fraction
import numpy as np
from copy import deepcopy

def fill(l):
    """ return a 0 vector with l entries. """
    result = []
    for i in range(l):
        result.append(Fraction())
    return result

def vec_add(v1, v2):
    """ adds vector v1 to vector v2, returns resulting vector. inputs are
        assumed to be valid m x 1 vectors. """
    result = []
    for i in range(len(v1)):
        result.append(v1[i] + v2[i])
    return result

def neg_vec(v):
    """ negates the values in vector v and returns the resulting vector. input
        is assumed to be a valid m x 1 vector. """
    result = []
    for i in range(len(v)):
        result.append(-v[i])
    return result

def vec_mult(c, v):
    """ multiplies m x 1 vector v by constant c and returns the resulting vector. """
    result = []
    for i in range(len(v)):
        result.append(v[i] * c)
    return result

def vec_mat_mult(v, m):
    """ multiplies matrix m by vector v and returns resulting vector. inputs
        are assumed to be valid for this operation (length of v = # of cols in m) """
    result = fill(len(m))
    t_m = np.array(m) # temporary array version of m
    for i,c in enumerate(v):
        result = vec_add(vec_mult(c, t_m[:, i]), result)
    return result

def inner_product(v1, v2):
    """ takes the inner product of the two m x 1 vectors v1 and v2
        and returns the resulting scalar. inputs are assumed to be
        valid for this operation (same length). """
    result = Fraction()
    for i in range(len(v1)):
        result += v1[i] * v2[i]
    return result

def project(v1, s):
    """ projects the vector v1 onto the subspace s (which can be either
        a vector or a matrix) and returns the resulting vector. inputs are
        assume to be valid for this operation (same # of rows in vec and space). """
    if type(s[0]) == list: # s is a matrix
        result = fill(len(s))
        t_s = np.array(s)
        for i in range(len(s[0])): # iterate over every column in s
            matrix_col = t_s[:, i]
            # val is <v1, s> / <s, s>
            val = inner_product(v1, matrix_col) * inner_product(matrix_col, matrix_col).invert()
            m = vec_mult(val, matrix_col)
            result = vec_add(result, m)
    else:
        result = fill(len(s))
        # val is <v1, s> / <s, s>
        val = inner_product(v1, s) * inner_product(s, s).invert()
        result = vec_mult(val, s)
    return result

def find_mobile_int(l, d):
    """ l is a list of integers from 1 to n. d is a list of the same
        size representing the direction the integers in l are pointing,
        where 1 means pointed right, -1 means pointed left.
        returns the largest "mobile" integer and its position, where mobile 
        means it is pointed at an integer which is smaller than it. if none 
        exist, returns False. """
    current_max = 0
    current_pos = -1
    for n in range(len(l)):
        index = n + d[n]
        if index < len(l):
            pointing_at = l[index]
        else: continue
        if index != -1 and l[n] > pointing_at and l[n] > current_max:
            current_max = l[n]
            current_pos = n
    return current_pos

def permute(n):
    """ returns permutation matrix with rows as permutations of 
        the list [1, 2, 3, .. , n]. num of rows in the matrix
        is n! = 1 * 2 * 3 * .. * n. index of row is # of swaps
        needed to get there. using johnston-trotter algorithm. """
    initial = [1 + i for i in range(n)]
    directions = [-1 for i in range(n)]
    # -1 is left, 1 is right
    final_list = [initial.copy()]
    while (pos := find_mobile_int(initial, directions)) >= 0:
        # there exists a mobile integer in the list
        mobile_int = initial[pos]
        adj = pos + directions[pos]
        # swap it with the int it's pointing at
        initial[pos], initial[adj] = initial[adj], initial[pos]
        directions[pos], directions[adj] = directions[adj], directions[pos]
        # reverse directions of ints larger than mobile_int
        for n in range(len(initial)):
            if initial[n] > mobile_int:
                directions[n] *= -1
        final_list.append(initial.copy())
    return final_list
    
def det(m):
    """ returns determinant of square nxn matrix m. input
        is assumed to be valid square matrix. using leibniz formula."""
    if len(m) != len(m[0]):
        raise ValueError("you can't take the determinant of a nonsquare matrix.")
    n = len(m)
    p = permute(n)
    D = 0
    sign = 1
    for sigma in p:
        D += sign * np.prod([m[i][sigma[i] - 1] for i in range(len(sigma))])
        sign *= -1
    return D

def transpose(m):
    """ swaps rows of matrix m with columns and returns resulting matrix. 
        input is assumed to be a valid matrix. """
    result = []
    t_m = np.array(m)
    for i in range(len(m[0])):
        result.append(t_m[:, i])
    return result

def mat_mult(m1, m2):
    """ multiplies matrix m1 (m x n) to m2 (n x p) on the left and returns
        the resultng matrix (m x p). inputs are assumed to be valid for this
        operation. """
    result = []
    t_m1 = np.array(m1)
    t_m2 = np.array(m2)
    row_num = len(m1)
    col_num = len(m2[0])
    # create empty m x p matrix
    for i in range(row_num):
        result.append([])
    for i in range(row_num):
        for j in range(col_num):
            result[i].append(inner_product(t_m1[i], t_m2[:, j]))
    return result

def aTa(m):
    """ multiplies a matrix by its transpose (on the left) and returns the resulting matrix. 
        input is assumed to be a valid matrix. """
    mT = transpose(m)
    result = mat_mult(mT, m)
    return result

def gs(m):
    """ does the gram-schmidt algorithm on the input matrix. returns
        orthogonal matrix which spans the same space as the columns
        of the given matrix. input is assumed to be a valid matrix. """
    result = []
    t_m = np.array(m)
    col_num = len(m[0])
    # use first column as first vector
    for i in t_m[:, 0]: result.append([i])
    for i in range(col_num - 1):
        n = i + 1
        matrix_col = t_m[:, n]
        vec = vec_add(matrix_col, neg_vec(project(matrix_col, result)))
        for j in range(len(vec)):
            result[j].append(vec[j])
    return result

def normalize_vec(v):
    """ takes vector input and returns normalized version. input is
        assumed to be a valid m x 1 vector. """
    result = []
    div = 0
    for n in v:
        div += n.decimal() * n.decimal()
    div = np.sqrt(div)
    for n in v:
        result.append(Fraction(n.decimal() / div))
    return result

def normalize_mat(m):
    """ takes matrix and returns version with normalized columns. input
        is assumed to be a valid matrix. """
    result = []
    t_m = np.array(m)
    for i in range(len(m[0])): # each column
        result.append(normalize_vec(t_m[:, i]))
    return transpose(result)

def rref(m):
    """ returns matrix m in reduced row echelon form. input is assumed to be
        a valid matrix. """
    lead = 0 # this is like the column i guess
    col_num = len(m[0])
    row_num = len(m)
    result = deepcopy(m)
    for r in range(row_num): # iterate through all rows
        if col_num <= lead:
            return result
        
        # if the row has a 0 where it should have a 1 in RREF, go to 
        # the next row until it doesn't
        i = r
        while result[i][lead].decimal() == 0:
            i += 1 # go to the next row
            if i == row_num: # gone through all rows
                i = r # reset i back to rth row
                lead += 1 # go to next column
                if lead == col_num: # gone through all columns
                    return result
        # swap rows i and r
        result[r],result[i] = result[i], result[r]

        # scale the row down so the lead spot is a 1
        temp_m = result[r][lead]
        if temp_m.decimal() != 0:
            for k in range(col_num):
                result[r][k] *= temp_m.invert()
        
        # do row operations
        for i in range(row_num):
            if i != r: # only do this to rows that aren't r
                temp_m = result[i][lead]
                for k in range(col_num):
                    result[i][k] += result[r][k] * - temp_m
        lead += 1
    return result

# def eigenpairs_2x2(m):
#     """ returns the eigenvalue/eigenvector pairs (if they are not imaginary)
#         of the given 2x2 matrix. input is assumed to be valid. """
#     tr_m = m[0][0].add(m[1][1])
#     det_m = det_2x2(m)
#     discriminant = tr_m.mult(tr_m).add(det_m.mult(-4))
#     if discriminant < 0:
#         # imaginary eigenvalues
#         return
#     elif discriminant == 0:
#         r1 = tr_m.mult(Fraction(1,2))
#         r2 = r1
#     elif discriminant > 0:
#         r1 = tr_m.mult(Fraction(1,2)).add(Fraction(1,2).mult(np.sqrt(discriminant)))
#         r2 = tr_m.mult(Fraction(1,2)).add(Fraction(-1,2).mult(np.sqrt(discriminant)))

def ident(n):
    """ returns nxn identity matrix. """
    # stolen from rosettacode.org lol this shits crazy
    i = [[int(i == j) for i in range(n)] for j in range(n)]
    return i

def factorial(n):
    """ returns n! = 1 * 2 * 3 * .. * n. """
    result = 1
    start = n
    while start > 0:
        result *= start
        start -= 1
    return result

if __name__ == "__main__":
    print()
    # vec1 = [Fraction(3), Fraction(1)]
    # vec2 = [Fraction(-3,2), Fraction(5,7)]
    # mat1 = [
    #     [Fraction(), Fraction(1,2), Fraction()],
    #     [Fraction(1,2), Fraction(2,2), Fraction(4,5)],
    #     [Fraction(1,3), Fraction(4,3), Fraction()]
    # ]
    # mat2 = [
    #     [Fraction(), Fraction(2,2)],
    #     [Fraction(4,2), Fraction(3,7)]
    # ]
    # mat3 = [
    #     [Fraction(), Fraction(1,2), Fraction(1), Fraction(18)],
    #     [Fraction(2), Fraction(1,3), Fraction(), Fraction(10)],
    #     [Fraction(-1), Fraction(-1,4), Fraction(2,5), Fraction(7)],
    #     [Fraction(-4,5), Fraction(-10), Fraction(1), Fraction(8)]
    # ]
    # print(det(mat3))