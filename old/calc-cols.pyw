# Tynan McGee
# 2/23/2021
# linear algebra calculator (input is transpose of matrix)

from tkinter import *
from tkinter import messagebox
from fractions import Fraction
from copy import deepcopy
from numpy import array,set_printoptions,sqrt,linalg
# https://www.tutorialspoint.com/python3/python_gui_programming.htm

# -----------------------------
# --  VECTOR FUNCTIONS! -------
def vec_add(v1,v2):
    """ adds vector v1 to vector v2 and returns the result (vector)."""
    result = []
    for i in range(len(v1)):
        result.append(v1[i] + v2[i])
    return result

def neg_vec(v):
    """ negates the values in vector v and returns the result (vector)."""
    result = []
    for i in range(len(v)):
        result.append(-v[i])
    return result

def vec_mult(c,v):
    """ multiplies vector v by constant c and returns the result (vector)."""
    result = []
    for i in range(len(v)):
        result.append(c * v[i])
    return result

def vec_mat_mult(v, m):
    """ multiplies matrix m by vector v. returns resulting vector. """
    result = []
    for i in v:
        result.append(0)
    for i,c in enumerate(v):
        result = vec_add(vec_mult(c, m[i]), result)
    return result

def inner_product(v1,v2):
    """ takes the inner product of the two vectors v1 and v2
        and returns the result (number)."""
    result = 0
    for i in range(len(v1)):
        result += v1[i] * v2[i]
    return result

def fill(l):
    """ return a 0 vector with l entries."""
    result = []
    for i in range(l):
        result.append(0)
    return result

def project(v1,s):
    """ projects the vector v1 onto the subspace s (either a vector or matrix)
        and returns the result (vector)."""
    if type(s[0]) == list:
        result = fill(len(s[0]))
        for i in range(len(s)): # for every column in s, do this
            val = inner_product(v1, s[i]) / inner_product(s[i],s[i])
            m = vec_mult(val, s[i])
            result = vec_add(result, m)
    else:
        result = fill(len(s))
        val = inner_product(v1, s) / inner_product(s,s)
        result = vec_mult(val, s)
    return result

def mat_mult(M1, M2):
    """ multiplies matrix M1 (m x n) to M2 (n x p) (on the left) and returns 
        the resulting matrix (m x p)."""
    result = []
    M1t = transpose(M1)
    num_of_rows = len(M1t)
    num_of_cols = len(M2)
    # create an empty m x p matrix
    for i in range(num_of_cols): # p columns
        result.append([])
    for i in range(num_of_cols):
        for j in range(num_of_rows):
            result[i].append(inner_product(M1t[j], M2[i]))
    return result
    
def gs_alg(mat):
    """ does the gram-schmidt algorithm on the given matrix.
        returns orthogonal matrix which spans the same space
        as the given matrix."""
    result = []
    num_of_cols = len(mat)
    result.append(mat[0]) # choose first vector
    for i in range(num_of_cols - 1):
        n = i + 1
        result.append(vec_add(mat[n], neg_vec(project(mat[n], result))))  
    return result

def normalize(v):
    """ takes vector input and returns normalized vector."""
    div = 0
    for n in v:
        div += n**2
    for i,n in enumerate(v):
        v[i] = n / sqrt(div)
    return v

def QR_factor(A):
    """ returns the QR factorization of given n by n matrix A. Q is orthogonal
        (it forms an orthonormal basis) and R is an upper-triangular matrix.
        Returns two matrices Q, R."""
    Q = deepcopy(gs_alg(A))
    for i,c in enumerate(Q):
        Q[i] = normalize(c)
    R = mat_mult(transpose(Q), A)
    return Q, R

def transpose(mat):
    """ returns transposed form of given matrix (cols become rows, rows become cols)."""
    result = []
    for i in range(len(mat[0])):
        result.append([])
    for i,c in enumerate(mat):
        for j,v in enumerate(c):
            result[j].append(v)
    return result

def least_squares(v,M):
    aT = transpose(deepcopy(M))
    m = deepcopy(M)
    ata = mat_mult(aT, m)
    atb = vec_mat_mult(v, aT)
    result = linalg.solve(ata, atb)
    return result

def rref(M):
    """ returns matrix M in reduced row echelon form (without changing m). """
    lead = 0 # this is like the column i guess
    num_of_cols = len(M[0])
    num_of_rows = len(M)
    result = deepcopy(M)
    for r in range(num_of_rows): # iterate through all rows
        if num_of_cols <= lead:
            return

        # if the row has a 0 where it would have a 1 in RREF, go to next row until it doesn't
        i = r
        while result[i][lead] == 0:
            i += 1 # go to the next row
            if i == num_of_rows: # last row
                i = r # reset i back to rth row
                lead += 1 # and go to the next column
                if lead == num_of_cols: # last column
                    return
        
        # swap rows i and r
        result[r],result[i] = result[i],result[r]

        # scale the row down so the lead spot is a 1
        temp_m = result[r][lead]
        if result[r][lead] != 0:
            for k in range(num_of_cols):
                result[r][k] /= temp_m

        # do row operations
        for i in range(num_of_rows):
            if i != r: # only do this to rows that aren't r
                # subtract m[i, lead] multiplied by row r from row i
                temp_m = result[i][lead]
                for k in range(num_of_cols):
                    result[i][k] -= temp_m * result[r][k]
        lead += 1
    return result

# -- end of vector functions --
# -----------------------------
if __name__ == "__main__":
    win = Tk()
    win.title("Linear Algebra Calculator")
    win.geometry('650x600')
    for i in range(3):
        win.grid_rowconfigure(i, weight = 1)
    win.grid_columnconfigure(0, weight = 1)
    set_printoptions(precision=3, suppress=True)

    def returnMat(t):
        """ takes in text field t, gets its contents, and if it contains a matrix or
            a vector, converts it into one and returns that. """
        errmsg = 'Invalid Input.\nExample input: \n"1, 2, 3, 4" \nfor a vector, or\n"1, 2, 3, 4\n 5, 6, 7, 8" \nfor a matrix.\nCommas must be used to separate numbers (except at linebreaks).'
        inp = t.get("1.0", END)
        inp = inp.replace(' ', '')
        inp = inp.split('\n')
        if inp[0] == '':
            return 0
        if len(inp) > 2: # input is a matrix
            for i,l in enumerate(inp):
                inp[i] = l.split(',')
            del inp[-1] # remove empty element
            for i,l in enumerate(inp):
                for j,n in enumerate(l):
                    try:
                        inp[i][j] = float(Fraction(n))
                    except ValueError:
                        messagebox.showerror('Error: Invalid Input', errmsg)
                        return 0
        else:
            del inp[-1] # remove empty element
            inp = inp[0].split(',')
            for i,n in enumerate(inp):
                try:
                    inp[i] = float(Fraction(n))
                except ValueError:
                    messagebox.showerror('Error: Invalid Input', errmsg)
                    return 0
        return inp

    def valid_vecs(v1, v2):
        """ returns bool of whether the vectors are vectors and have the same length. 
            inputs are actual vectors, not text fields. """
        if type(v1) == list and type(v2) == list:
            if len(v1) == len(v2):
                return True
            else:
                messagebox.showerror('Error: Invalid Input', "The vectors must be the same length!")
                return False
        else:
            return False

    def valid_vecmat(v, m):
        """ returns bool of whether the given vector v and matrix m are valid for projection. """
        try:
            if type(v) == list and type(m[0]) == list:
                l = len(m[0])
                for i in m:
                    if len(i) != l:
                        messagebox.showerror('Error: Invalid Input', "The matrix is invalid.")
                        return False
                if len(v) == len(m[0]):
                    return True
                else:
                    messagebox.showerror('Error: Invalid Input', "The vector must have the same number of rows as the matrix!")
                    return False
            else:
                messagebox.showerror('Error: Invalid Input', "The vector must have the same number of rows as the matrix!")
                return False
        except:
            return False

    def valid_mat(m):
        """ returns bool of whether the given matrix is actually a matrix. """
        if type(m) == list and type(m[0] == list):
                l = len(m[0])
                for i in m:
                    if len(i) != l:
                        messagebox.showerror('Error: Invalid Input', "The matrix is invalid.")
                        return False
                return True
        else:
            return False

    def valid_mats(m1, m2):
        """ returns bool of whether the matrices are able to be multiplied. inputs are assumed to be valid matrices. """
        if len(m1) == len(m2[0]): # m1 is cols, m2[0] is rows
            return True
        else:
            messagebox.showerror('Error: Invalid Input', "The number of columns in matrix 1 must match the number of rows in matrix 2.")
            return False

    def clr_text_fields():
        """ clears all text fields. """
        for t in text_list:
            t.config(state = NORMAL)
            t.delete("1.0", END)
            try:
                change_text(change_text_dict[current_operation_text.get()])
            except:
                break
        RESULT.config(state = DISABLED)

    def show_result(result):
        """ puts result on the screen in the result box. """
        RESULT.config(state = NORMAL)
        RESULT.delete("1.0", END)
        RESULT.insert(END, result)
        RESULT.config(state = DISABLED)

    def add(v1, v2, m1, m2):
        """ add v1 and v2 and print it to the screen. """
        vec1 = returnMat(v1)
        vec2 = returnMat(v2)
        if valid_vecs(vec1, vec2):
            result = vec_add(vec1, vec2)
            msg = 'v1 + v2 =\n' + str(array(result))
            show_result(msg)

    def sub(v1, v2, m1, m2):
        """ subtract v2 from v1 and print it to the screen. """
        vec1 = returnMat(v1)
        vec2 = returnMat(v2)
        if valid_vecs(vec1, vec2):
            result = vec_add(vec1, neg_vec(vec2))
            msg = 'v1 - v2 =\n' + str(array(result))
            show_result(msg)

    def vecmatmult(v1, v2, m1, m2):
        """ print vector matrix multiplication between v1 and m1. """
        vec1 = returnMat(v1)
        mat1 = returnMat(m1)
        if len(vec1) == len(mat1) and valid_mat(mat1):
            result = vec_mat_mult(vec1, mat1)
            msg = 'M1 * v1 =\n' + str(array(result))
            show_result(msg)
        else:
            messagebox.showerror('Error: Invalid Input', "Make sure your matrix has the same number of columns as your vector has rows!")
            return 1

    def axb(v1, v2, m1, m2):
        """ prints solution to equation Ax = b for A=m1 and b=v1. """
        vec1 = returnMat(v1)
        mat1 = returnMat(m1)
        if len(vec1) == len(mat1) and valid_mat(mat1) and len(mat1) == len(mat1[0]):
            try: result = linalg.solve(mat1,vec1)
            except: 
                messagebox.showerror('Error: Solution not found', "Could not find solution for given equation.")
                return 1
            msg = 'x =\n' + str(array(result))
            show_result(msg)
        elif len(mat1) != len(mat1[0]):
            messagebox.showerror('Error: Invalid Input', "Your matrix must be square for this function to work.")
            return 1
        else:
            messagebox.showerror('Error: Invalid Input', "Make sure your matrix has the same number of columns as your vector has rows!")
            return 1

    def dot(v1, v2, m1, m2):
        """ print inner product of v1 and v2 to the screen. """
        vec1 = returnMat(v1)
        vec2 = returnMat(v2)
        if valid_vecs(vec1, vec2):
            result = inner_product(vec1, vec2)
            msg = '<v1, v2> =\n' + str(array(result))
            show_result(msg)
        
    def prjct_vec(v1, v2, m1, m2):
        """ project vector v1 onto vector v2 and print it to the screen. """
        vec1 = returnMat(v1)
        vec2 = returnMat(v2)
        if valid_vecs(vec1, vec2):
            result = project(vec1, vec2)
            msg = 'proj_{v2},v1 =\n' + str(array(result))
            show_result(msg)

    def prjct_mat(v1, v2, m1, m2):
        """ project vector v1 onto matrix m and print it to the screen. """
        vec1 = returnMat(v1)
        mat = returnMat(m1)
        if valid_vecmat(vec1, mat):
            result = project(vec1, mat)
            msg = 'proj_{M1},v1 =\n' + str(array(result))
            show_result(msg)

    def gs(v1, v2, m1, m2):
        """ do the gs algorithm on matrix m and print the result to the screen. """
        mat = returnMat(m1)
        if valid_mat(mat):
            result = gs_alg(mat)
            msg = 'orthogonal matrix\n(spans col(M1)):\n' + str(array(transpose(result)))
            show_result(msg)

    def nrmz_vec(v1, v2, m1, m2):
        """ normalize vector v1 and print it to the screen. """
        vec = returnMat(v1)
        if vec != 0 and type(vec) == list:
            result = normalize(vec)
            msg = 'norm(v1) =\n' + str(array(result))
            show_result(msg)

    def nrmz_mat(v1, v2, m1, m2):
        """ normalize matrix m and print it to the screen. """
        mat = returnMat(m1)
        if valid_mat(mat):
            for i,c in enumerate(mat):
                mat[i] = normalize(c)
            msg = 'norm(M1) =\n' + str(array(transpose(mat)))
            show_result(msg)

    def mmult(v1, v2, m1, m2):
        """ multiply m1 by m2 and print it to the screen. """
        mat1 = returnMat(m1)
        mat2 = returnMat(m2)
        if valid_mat(mat1) and valid_mat(mat2):
            if valid_mats(mat1, mat2):
                result = mat_mult(mat1, mat2)
                msg = 'M1 * M2 =\n' + str(array(transpose(result)))
                show_result(msg)

    def qr(v1, v2, m1, m2):
        """ factor matrix m1 into Q and R and print them to the screen. """
        mat = returnMat(m1)
        if valid_mat(mat):
            q, r = QR_factor(mat)
            msg = 'Q =\n' + str(array(transpose(q)))
            msg += '\nR =\n' + str(array(transpose(r)))
            show_result(msg)

    def ls(v1, v2, m1, m2):
        """ print least squares solution to M1x = v1 """
        vec = returnMat(v1)
        mat = returnMat(m1)
        if valid_vecmat(vec, mat):
            result = least_squares(vec, mat)
            msg = 'x_ls =\n' + str(array(result))
            show_result(msg)

    function_dict = {
        'Add':add,
        'Subtract':sub,
        'Matrix-Vector Multiply':vecmatmult,
        'Solve Ax = b':axb,
        'Inner Product':dot,
        'Project (vec on vec)':prjct_vec,
        'Project (vec on mat)':prjct_mat,
        'GS Algorithm':gs,
        'Normalize Vector':nrmz_vec,
        'Normalize Matrix':nrmz_mat,
        'Matrix Multiply':mmult,
        'QR Factor':qr,
        'Least Squares Solution':ls
    }
    change_text_dict = {
        'Add':'vecs',
        'Subtract':'vecs',
        'Matrix-Vector Multiply':'vecmat',
        'Solve Ax = b':'vecmat',
        'Inner Product':'vecs',
        'Project (vec on vec)':'vecs',
        'Project (vec on mat)':'vecmat',
        'GS Algorithm':'mat',
        'Normalize Vector':'vec',
        'Normalize Matrix':'mat',
        'Matrix Multiply':'mats',
        'QR Factor':'mat',
        'Least Squares Solution':'vecmat'
    }

    def calc():
        # try:
        f = function_dict[current_operation_text.get()]
        f(V1, V2, MAT1, MAT2)
        # except:
        #     print('Something went wrong...')
        #     return 1

    def focus_next_widget(event):
        event.widget.tk_focusNext().focus()
        return("break")

    def change_text(t):
        if t == 'vecs':
            V1.config(state = NORMAL, bg = "white")
            V2.config(state = NORMAL, bg = "white")
            MAT1.config(state = DISABLED, bg = "gray64")
            MAT2.config(state = DISABLED, bg = "gray64")
        elif t == 'vecmat':
            V1.config(state = NORMAL, bg = "white")
            V2.config(state = DISABLED, bg = "gray64")
            MAT1.config(state = NORMAL, bg = "white")
            MAT2.config(state = DISABLED, bg = "gray64")
        elif t == 'vec':
            V1.config(state = NORMAL, bg = "white")
            V2.config(state = DISABLED, bg = "gray64")
            MAT1.config(state = DISABLED, bg = "gray64")
            MAT2.config(state = DISABLED, bg = "gray64")
        elif t == 'mat':
            V1.config(state = DISABLED, bg = "gray64")
            V2.config(state = DISABLED, bg = "gray64")
            MAT1.config(state = NORMAL, bg = "white")
            MAT2.config(state = DISABLED, bg = "gray64")
        elif t == 'mats':
            V1.config(state = DISABLED, bg = "gray64")
            V2.config(state = DISABLED, bg = "gray64")
            MAT1.config(state = NORMAL, bg = "white")
            MAT2.config(state = NORMAL, bg = "white")

    def change_dropdown(*args):
        current_op = current_operation_text.get()
        change_text(change_text_dict[current_op])

    default_font = ('Courier New', '12')
    bigger_font = ('Courier New', '14')

    # ---- frames ----
    button_frame = Frame(win)
    vector_frame = Frame(win)
    matrix_frame = Frame(win)
    frame_list = [button_frame, vector_frame, matrix_frame]
    for i,f in enumerate(frame_list):
        f.grid(row = i, column = 0, padx = 5, pady = 5, ipadx = 2, ipady = 2)
        for n in range(len(frame_list)):
            f.grid_columnconfigure(n, weight=1)
            f.grid_rowconfigure(n, weight=1)


    # ---- buttons, dropdowns ----
    current_operation_text = StringVar(value = 'None Selected')

    dropdown = OptionMenu(button_frame, current_operation_text, 'Add', 'Subtract', 'Matrix-Vector Multiply', 'Solve Ax = b', 'Inner Product', 'Project (vec on vec)', 'Project (vec on mat)', 'GS Algorithm', 'Normalize Vector', 'Normalize Matrix', 'Matrix Multiply', 'QR Factor', 'Least Squares Solution')
    dropdown.grid(row = 0, column = 1)
    drop_label = Label(button_frame, text = "Select Operation:")
    drop_label.grid(row = 0, column = 0)

    current_operation_text.trace('w', change_dropdown)

    calc_button = Button(button_frame, width = 10, height = 1, text = "Calculate", command = calc)
    calc_button.grid(row = 1, column = 1, columnspan = 2, pady = 10)
    clear_button = Button(button_frame, width = 15, height = 1, text = "Clear text fields", command = clr_text_fields)
    clear_button.grid(row = 1, column = 0, padx = 5, pady = 10)


    # ---- text fields ----
    V1 = Text(vector_frame, height = 1, width = 25, state = DISABLED, bg = "gray64", font = default_font)
    V2 = Text(vector_frame, height = 1, width = 25, state = DISABLED, bg = "gray64", font = default_font)
    MAT1 = Text(matrix_frame, height = 6, width = 25, state = DISABLED, bg = "gray64", font = default_font)
    MAT2 = Text(matrix_frame, height = 6, width = 25, state = DISABLED, bg = "gray64", font = default_font)
    V1.grid(row = 0, column = 1, pady = 5)
    V2.grid(row = 0, column = 3, pady = 5)
    MAT1.grid(row = 0, column = 1)
    MAT2.grid(row = 0, column = 3)

    RESULT = Text(matrix_frame, height = 12, width = 25, state = DISABLED, font = bigger_font)
    RESULT.grid(row = 1, column = 1, pady = 15)

    text_list = [V1, V2, MAT1, MAT2, RESULT]



    for t in text_list:
        t.bind("<Tab>", focus_next_widget) # tab moves to next widget

    lbl1 = Label(vector_frame, text = "Vector 1:")
    lbl2 = Label(vector_frame, text = "Vector 2:")
    lbl3 = Label(matrix_frame, text = "Matrix 1:")
    lbl4 = Label(matrix_frame, text = "Matrix 2:")
    lbl5 = Label(matrix_frame, text = "Result:")
    lbl1.grid(row = 0, column = 0, padx = 5)
    lbl2.grid(row = 0, column = 2, padx = 5)
    lbl3.grid(row = 0, column = 0, padx = 5)
    lbl4.grid(row = 0, column = 2, padx = 5)
    lbl5.grid(row = 1, column = 0, padx = 5)


    win.mainloop()