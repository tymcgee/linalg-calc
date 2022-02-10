from fraction_qt import *
from calc_funcs_qt import det

# -- vector/matrix retrieval and verification
def get_input(t):
    """
    Returns a list containing each line of text from t with spaces removed.
    - t is a Qt text object containing comma separated numbers and fractions.
    - Returns a list of those numbers (each item in the list is a line of text
      from the input (a string)).
    """
    try:
        inp = t.text()
    except:
        inp = t.toPlainText()
    inp = inp.replace(' ', '')
    inp = inp.split('\n')
    if inp[0] == '': return 0 # string is empty
    return inp
        
def return_vector(t):
    """
    Finds out whether the text in t contains a vector, and if it does,
    converts the text to a list of fraction objects and returns it.
    - t is a Qt text object.
    - Returns error message if t doesn't contain a vector, otherwise returns the vector 
      which it contains.
    """
    inp = get_input(t)
    if inp == 0: return 0
    inp = inp[0].split(',')
    for i,n in enumerate(inp):
        try: inp[i] = get_frac_from_string(n)
        except ValueError: # if it didn't work, input wasn't exclusively numbers
            return 'Invalid input. Make sure there are no extra commas at the end of a line.'
    return inp

def return_matrix(t):
    """
    Finds out whether the text in t contains a matrix, and if it does,
    converts it to a list of lists of fraction objects and returns it.
    - t is a Qt text object.
    - Returns error message if t doesn't contain a matrix, otherwise returns the
      matrix which it contains.
    """
    inp = get_input(t)
    if inp == 0: return 0
    for i in range(len(inp)):
        inp[i] = inp[i].split(',')
    for i in range(len(inp)):
        for j in range(len(inp[i])):
            try: inp[i][j] = get_frac_from_string(inp[i][j])
            except ValueError:
                return 'Invalid input. Make sure there are no extra commas at the end of a line.'
    return inp

def is_vector(v):
    """
    Finds out whether v is a valid n x 1 vector.
    - v should be a list of fraction objects.
    - Returns False if v is not a list of fraction objects.
      Returns True if it is.
    """
    vec = True
    if isinstance(v, (list, np.ndarray)):
        for n in v:
            if not isinstance(n, Fraction): vec = False
            # if isinstance(n, Fraction):
            #     if not isinstance(n.decimal(), (float, int, np.floating, np.integer)): vec = False
            # else: vec = False
    else: vec = False
    return vec

def is_matrix(m):
    """
    Finds out whether m is a valid m x n matrix.
    - m should be a list of lists of fraction objects,
      where each list is the same length.
    - Returns False if lists contain anything but fraction
      objects or if all of the rows aren't the same length.
      Returns True otherwise.
    """
    mat = True
    if isinstance(m, (list, np.ndarray)) and isinstance(m[0], (list, np.ndarray)):
        l = len(m[0])
        for i in m:
            if len(i) != l: # rows aren't all the same length
                mat = False
            for j in i:
                if not isinstance(j, Fraction): mat = False
                # if isinstance(j, Fraction):
                #     if not isinstance(j.decimal(), (float, int, np.floating, np.integer)): mat = False
    else: mat = False
    return mat

def valid_vecs(v1, v2):
    """
    Finds out whether v1 and v2 are both vectors of the same length.
    - v1 and v2 should be vectors (lists of fraction objects).
    - Returns a string (error message) if something went wrong,
      or True.
    """
    if is_vector(v1) and is_vector(v2):
        if len(v1) == len(v2):
            return True
        else:
            return "The vectors must be the same length."
    else:
        return "At least one of the inputs is invalid."

def valid_mats(m1, m2):
    """
    Finds out whether m1 and m2 are both matrices where m1 has the
    same number of columns as m2 has rows.
    - m1 and m2 should be matrices (lists of lists of fraction objects).
    - Returns a string (error message) if something went wrong,
      or True.
    """
    if is_matrix(m1) and is_matrix(m2):
        m1_cols = len(m1[0])
        m2_rows = len(m2)
        if m1_cols == m2_rows:
            return True
        else:
            return "Make sure M1 has the same number of columns as M2 has rows."
    else:
        return "At least one of the inputs is invalid."

def matvec_valid(v, m, op):
    """
    Finds out whether vector v and matrix m are valid for operating
    with each other, whether it be solving Ax=b or projecting v on
    to m or whatever else.
    - v is a vector (list of fraction objects).
    - m is a matrix (list of lists of fraction objects).
    - op is a string operation, either "Matrix-Vector Multiply",
     "Solve Ax = b", or "Project (vec on mat)".
    - Returns either a string (error message) if something went wrong,
      or True.
    """
    if is_vector(v) and is_matrix(m):
        if len(v) == len(m[0]):
            if op == "Solve Ax = b":
                if det(m) == 0:
                    return "The provided matrix was not invertible."
                return True
            if op == "Matrix-Vector Multiply":
                return True
        if len(v) == len(m) and op == "Project (vec on mat)":
            return True
        else:
            return "Make sure the vector and matrix dimensions line up.\nFor projection, the vector must have the same number of rows as the matrix.\nFor multiplication, the vector must have the same number of columns as the matrix."
    else:
        return "At least one of the inputs is invalid."
        
def mat_valid(m, op):
    """
    Finds out whether the matrix m is valid for the given operation op.
    - m is a matrix (list of lists of fraction objects).
    - op is a string, any of "Determinant", "Determinant (slow),
      "REF", "RREF", "Inverse", "M^T * M", "GS Algorithm",
    "Normalize Matrix", or "Eigen Matrix".
    - Returns either a string (error message) if something went wrong,
      or True.
    """
    if is_matrix(m):
        if op == "Inverse":
            if det(m) == 0:
                return "The provided matrix was not invertible."
            return True
        elif op in ("Determinant", "Determinant (slow)", "Eigen Matrix"):
            if len(m) != len(m[0]):
                return "The provided matrix was not square, so that operation will not work."
            return True
        else:
            return True
    else:
        return "The input (m1) is not a matrix."
