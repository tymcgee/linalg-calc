from fraction import Fraction
from matrix_format import format_matrix, format_vector, format_fraction
import numpy as np

def transpose(m):
    """
    Returns the transpose of a matrix.
    - m is a matrix.
    - Returns a matrix.
    """
    result = [[0 for _ in range(len(m))] for _ in range(len(m[0]))]
    for i in range(len(m)):
        for j in range(len(m[0])):
            result[j][i] = m[i][j]
    return result

def vec_add(v1, v2):
    """
    Adds two vectors together.
    - v1 and v2 are vectors.
    - Returns a vector (the sum of v1 and v2).
    """
    result = []
    for i in range(len(v1)):
        result.append(v1[i] + v2[i])
    return result

def neg_vec(v):
    """
    Negates a vector.
    - v is a vector.
    - Returns a vector (the negation of v).
    """
    result = []
    for i in range(len(v)):
        result.append(-v[i])
    return result

def vec_mult(v, c):
    """
    Multiplies a vector by a constant.
    - v is a vector.
    - c is a constant (int, float, fraction).
    - Returns a vector (v * c).
    """
    result = []
    for i in range(len(v)):
        result.append(v[i] * c)
    return result
    
def vec_mat_mult(m, v):
    """
    Multiplies a matrix by a vector (on the right).
    - m is a matrix.
    - v is a vector.
    - Returns a vector (m * v).
    """
    result = [0 for _ in range(len(m))]
    m_t = transpose(m)
    for i,c in enumerate(v):
        result = vec_add(vec_mult(m_t[i], c), result)
    return result

def inner_product(v1, v2):
    """
    Takes the inner product (dot product) of v1 and v2.
    - v1 and v2 are vectors.
    - Returns a scalar (v1 dotted with v2).
    """
    result = Fraction()
    for i in range(len(v1)):
        result += v1[i] * v2[i]
    return result

def mat_mult(m1, m2):
    """
    Multiplies two matrices together.
    - m1 is a matrix (on the left).
    - m2 is a matrix (on the right).
    - Returns a matrix (m1 * m2, in that order).
    """
    m2_t = transpose(m2)
    row_num = len(m1)
    col_num = len(m2_t)
    # create empty row_num x col_num matrix
    result = [[0 for _ in range(col_num)] for _ in range(row_num)]
    for i in range(row_num):
        for j in range(col_num):
            result[i][j] = inner_product(m1[i], m2_t[j])
    return result

def normalize_vec(v):
    """
    Normalizes a vector so that its length is 1
    (the squares of its components add to 1).
    - v is a vector.
    - Returns a vector (norm(v)).
    """
    result = []
    div = 0
    for n in v:
        div += float(n) ** 2
    div = np.sqrt(div)
    if div != 0:
        for n in v:
            result.append(Fraction(float(n) / div))
    else:
        for n in range(len(v)):
            result.append(Fraction())
    return result

def normalize_mat(m):
    """
    Normalizes a matrix so that the length of its
    columns are 1 (the squares of their components
    add to 1).
    - m is a matrix.
    - Returns a matrix (norm(m)).
    """
    result = []
    m_t = transpose(m)
    for i in m_t:
        result.append(normalize_vec(i))
    return transpose(result)

def gs(m):
    """
    Does the gram-schmidt algorithm on a matrix to obtain
    an orthogonal matrix which spans the same space as
    the column space of the original matrix.
    - m is a matrix.
    - Returns a matrix (gs(m)).
    """
    result = []
    m_t = transpose(m)
    col_num = len(m_t)
    # use first column as first vector
    for i in m_t[0]: result.append([i])
    for i in range(col_num - 1):
        n = i + 1
        col = m_t[n]
        vec = vec_add(col, neg_vec(project(col, result)))
        for j in range(len(vec)):
            result[j].append(vec[j])
    return result

def qr(m):
    """
    Finds a QR-factorization of a matrix, where Q is orthogonal
    and R is upper-triangular. Creates Q with the gram-schmidt
    algorithm and then solves for R.
    - m is a matrix.
    - Returns (Q, R) where Q is an orthogonal matrix and R is
      an upper-triangular matrix.
    """
    ortho_m = gs(m)
    Q = normalize_mat(ortho_m)
    R = mat_mult(transpose(Q), m)
    return Q,R

def is_orthogonal_set(m):
    """
    Determines whether a matrix is orthogonal (each column
    is orthogonal to each other column).
    - m is a matrix.
    - Returns a bool (True if the matrix is an orthogonal set).
    """
    m_t = transpose(m)
    col_num = len(m_t)
    orth = True
    for i in range(col_num):
        # is each column orthogonal to each other column
        n = i + 1
        while n < col_num:
            if inner_product(m_t[i], m_t[n]) != 0: orth = False
            n += 1
    return orth

def project(v1, s):
    """
    Projects a vector onto another vector or a subspace.
    - v1 is a vector.
    - s is either a vector or a matrix (if a matrix, it
      must be orthogonal).
    - Returns a vector (proj_s(v1))
    """
    result = [0 for _ in range(len(s))]
    if isinstance(s[0], (list, np.ndarray)): # s is a matrix
        # s must be orthogonal matrix for this to work
        if not is_orthogonal_set(s):
            s_t = transpose(gs(s))
        s_t = transpose(s)
        for col in s_t:
            # val is <v1, col> / <col, col>
            val = inner_product(v1, col) / inner_product(col, col)
            result = vec_add(result, vec_mult(col, val))
    else:
        # val is <v1, s> / <s, s>
        val = inner_product(v1, s) / inner_product(s, s)
        result = vec_mult(s, val)
    return result

def diagonal_product(m):
    """
    Finds the product along the diagonal of a square matrix.
    - m is a square matrix.
    - Returns a scalar (the product along the diagonal of m).
    """
    # m must be square
    result = 1
    for i in range(len(m)):
        result *= m[i][i]
    return result

def det(m):
    """
    Finds the determinant of a square matrix using Gaussian Elimination.
    - m is a square matrix.
    - Returns a scalar (det(m)).
    """
    if len(m) != len(m[0]):
        return 0
    reduced, d = ref(m, True)
    determinant = diagonal_product(reduced) * d
    return determinant

def aTa(m):
    """
    Multiplies a matrix by its tranpose (on the left). The resulting
    matrix is square and symmetric.
    - m is a matrix.
    - Returns a square symmetric matrix (m^T * m).
    """
    mT = transpose(m)
    result = mat_mult(mT, m)
    return result

def ref(m, return_d=False):
    """
    Finds row-echelon form of a matrix (while keeping track 
    of row operations for use in determinant calculation).
    - m is a matrix.
    - return_d is a bool for whether to return the product of the row
      operations' effect on the determinant.
    - Returns a matrix (ref(m)) and, if return_d is True,
      also returns either 1 or -1 depending on the number
      of row swaps (for use in calculating determinant).
    """
    lead = 0 # column?
    d = 1 # determinant multiplier
    col_num = len(m[0])
    row_num = len(m)
    result = [x[:] for x in m] # copy m without referencing it
    for r in range(row_num): # iterate through the rows
        if col_num <= lead:
            if return_d: return result, d
            return result
        # if the row has a 0 on the diagonal, go to the next row until it doesn't
        i = r
        while result[i][lead] == 0:
            i += 1
            if i == row_num: # gone through all the rows
                i = r # reset i back to rth row
                lead += 1 # go to next column
                if lead == col_num: # gone through all the columns
                    if return_d: return result, d
                    return result
        # swap rows i and r
        if i != r: d *= -1 # determinant is multiplied by -1 for each row swap
        result[r], result[i] = result[i], result[r]

        # zero out other rows on lead column
        i = r
        while i < row_num - 1: # only do this to rows that are below r
            i += 1
            # result[i][lead] is the (supposedly) nonzero number we want to zero out
            m = -result[i][lead] / result[r][lead]
            for k in range(col_num):
                result[i][k] += result[r][k] * m # when k = lead, this zeroes result[i][k].
        # determinant doesn't change
        lead += 1
    if return_d: return result, d
    return result

def rref(m):
    """
    Finds reduced row echelon form of a matrix.
    - m is a matrix.
    - Returns a matrix (rref(m)).
    """
    lead = 0 # this is like the column i guess
    col_num = len(m[0])
    row_num = len(m)
    result = [x[:] for x in m] # copy m without referencing it
    for r in range(row_num): # iterate through all rows
        if col_num <= lead:
            return result
        
        # if the row has a 0 where it should have a 1 in RREF, go to 
        # the next row until it doesn't
        i = r
        while result[i][lead] == 0:
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
        if temp_m != 0:
            for k in range(col_num):
                result[r][k] /= temp_m
        
        # do row operations
        for i in range(row_num):
            if i != r: # only do this to rows that aren't r
                temp_m = result[i][lead]
                for k in range(col_num):
                    result[i][k] += result[r][k] * -temp_m
        lead += 1
    return result

def solve(A, b):
    """
    Solves matrix equation Ax = b for x using Gauss-Jordan Elimination (RREF).
    - A is a matrix.
    - b is a vector.
    - Returns a vector (the solution to Ax = b, if it exists). If no solution
      exists, returns 0.
    """
    if len(A) != len(A[0]): return 0
    A_t = transpose(A)
    A_t.append(b) # augmented matrix
    aug_A = transpose(A_t)
    sol = transpose(rref(aug_A))
    if sol[:len(A)] != identity(len(A)):
        return 0
    sol = sol[-1] # solution is the last column of rref
    return sol

def inverse(A):
    """
    Finds the inverse of a matrix using Gauss-Jordan Elimination (RREF).
    - A is a matrix.
    - Returns a matrix (A^-1, if it exists). If there is no inverse,
      returns 0.
    """
    if len(A) != len(A[0]) or det(A) == 0:
        return 0 # inverse DNE
    n = len(A)
    A_t = transpose(A)
    iden = identity(n)
    for i in iden:
        A_t.append(i)
    aug_A = transpose(A_t) # A with identity columns augmented on
    sol = transpose(rref(aug_A))
    if sol[:len(A)] != identity(len(A)):
        return 0
    sol = sol[-len(A):]
    return transpose(sol)

def identity(n):
    """
    Creates an n x n identity matrix.
    - n is an integer.
    - Returns an n x n identity matrix.
    """
    # pretty much stolen from rosettacode.org lol this is sick
    i = [[Fraction(int(i == j)) for i in range(n)] for j in range(n)]
    return i

def eigen_matrix(m):
    """
    Does the QR-algorithm on a matrix and returns the resulting
    upper-triangular matrix (with eigenvalues of the original matrix
    on the diagonal (hopefully)).
    - m is a matrix.
    - Returns an upper-triangular matrix with (hopefully) the eigenvalues
      of m on the diagonal.
    """
    q,r = qr(m)
    for _ in range(500):
        A_n = mat_mult(r,q)
        q,r = qr(A_n)
    return A_n


if __name__ == "__main__":
    mat1 = [
        [Fraction(1), Fraction(2,3)],
        [Fraction(3), Fraction(3,4)],
        [Fraction(2), Fraction(4)]
    ]
    mat2 = [
        [Fraction(2), Fraction(3)],
        [Fraction(1,2), Fraction(4)]
    ]
    mat3 = [
        [Fraction(1), Fraction(1,2), Fraction(3)],
        [Fraction(2), Fraction(2,3), Fraction(1,4)],
        [Fraction(3), Fraction(4,5), Fraction(1)]
    ]
    mat4 = [
        [12, -51, 4],
        [6, 167, -68],
        [-4, 24, -41]
    ]
    ok = [
        [Fraction(1), Fraction(), Fraction()],
        [Fraction(), Fraction(), Fraction(1)],
        [Fraction(), Fraction(1,2), Fraction()]
    ]
    vec1 = [Fraction(1), Fraction(2)]
    vec2 = [Fraction(2), Fraction(13), Fraction(1)]
    ansq, ansr = qr(mat4)
    print(format_matrix(ansq))
    print(format_matrix(ansr))
    # print(format_vector(project(vec2, mat1)))
    # print(format_fraction(det(mat3)))

# v this is old slow determinant stuff, it does work but it's a million times slower than the version using REF. keeping it around cause it's still cool af that it works.

# ---- slow determinant helper funcs ----
def find_mobile_int(l, d):
    """
    Finds the largest "mobile" integer and its position, where
    mobile means it is pointed at an integer which is smaller than
    it.
    - l is a list containing integers from 1 to some number n, with no repeating
      entries.
    - d is a list of the same size as l representing the direction the integers
      in l are pointing. 1 means pointed right, -1 means pointed left.
    - Returns an integer representing the current position of the largest
      mobile integer in l.
    """
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
    """
    Creates a permutation matrix using the Johnston-Trotter algorithm with rows as 
    permutations of the list [1, 2, .. , n]. The number of rows in the matrix is n! 
    (n factorial). The index of the row is the number of row-swaps needed to get there.
    - n is an integer (size of the list).
    - Returns a matrix containing all the permutations of the list [1, 2, .. , n].
    """
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
        for i in range(len(initial)):
            if initial[i] > mobile_int:
                directions[i] *= -1
        final_list.append(initial.copy())
    return final_list

def product(a):
    """
    Finds the product of all the items in a list.
    - a is a list of numbers.
    - Returns a scalar (the product of all the items in a).
    """
    result = 1
    for n in a:
        result *= n
    return result

def det_slow(m):
    """
    Finds the determinant of a square matrix using the 
    leibniz formula (very slow for large matrices).
    - m is a matrix.
    - Returns a scalar (det(m)).
    """
    """ returns determinant of square n x n matrix m. using leibniz formula. """
    if len(m) != len(m[0]):
        return 0
    n = len(m)
    p = permute(n)
    D = 0
    sign = 1
    # sign alternates btwn 1 and -1 because of the way the permutation matrix was created
    # D is the sum over each sigma of the product of m[i][sigma[i] - 1] from i=0 to len(sigma)
    # we do sigma[i] - 1 since matrix is indexed starting at 0 and sigma is indexes starting at 1
    for sigma in p:
        D += sign * product([m[i][sigma[i] - 1] for i in range(len(sigma))])
        sign *= -1
    return D
# ---- end of determinant stuff ----