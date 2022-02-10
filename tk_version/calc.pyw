# Tynan McGee
# 3/15/2021 - 5/18/2021
# linear algebra calculator

import tkinter as tk
from tkinter import messagebox
import numpy as np
import random
from fraction import *
from calc_funcs import *
from input_funcs import *
from matrix_format import *

# https://www.tutorialspoint.com/python3/python_gui_programming.htm

class Func:
    def __init__(self, func, variables, text, info):
        self.func = func # this is a function
        self.variables = variables # this is a string
        self.text = text # this is a string
        self.info = info # this is a string

# -- non-tkinter global vars --
CURRENT_RESULT = ''
FUNCS = {
        'Add':                          Func(vec_add,        'vecs',     'v1 + v2 =\n',                             'Adds v1 and v2 together.'),
        'Subtract':                     Func(vec_add,        'vecs',     'v1 - v2 =\n',                             'Subtracts v2 from v1.'),
        'Matrix-Vector Multiply':       Func(vec_mat_mult,   'vecmat',   'M1 * v1 =\n',                             'Multiplies M1 by v1.'),
        'Inner Product':                Func(inner_product,  'vecs',     '<v1, v2> =\n',                            'Inner product (aka dot product) of v1 and v2 (multiplies components and adds them). For example, if v1 = [a, b] and v2 = [c, d] the inner product is ac + bd.'),
        'Determinant':                  Func(det,            'mat',      'Det(M1) =\n',                             'Takes the determinant of M1. Only works if M1 is square. Uses Gaussian Elimination, so it is pretty fast.'),
        'Determinant (slow)':           Func(det_slow,       'mat',      'Det(M1) =\n',                             'Takes the determinant of M1. Only works if M1 is square. Uses the Leibniz formula, which works incredibly slow for large matrices (if a matrix is n x n, the computer must perform more than n factorial operations).'),
        'REF':                          Func(ref,            'mat',      'REF(M1) =\n',                             'Puts M1 into row echelon form (upper triangular). If there is a 0 on one of the diagonals, the matrix is not invertible.'),
        'RREF':                         Func(rref,           'mat',      'RREF(M1) =\n',                            'Puts M1 into reduced row echelon form (1 on the diagonals where possible). If there is a 0 on one of the diagonals, the matrix is not invertible.'),
        'Solve Ax = b':                 Func(solve,          'vecmat',   'x = \n',                                  'Uses Gaussian Elimination (via row reduction) to solve Ax = b, where A is M1 and b is v1. Does not work if the matrix is not invertible.'),
        'Inverse':                      Func(inverse,        'mat',      'M1^(-1) =\n',                             'Finds the inverse of M1 using Gaussian Elimination (via row reduction). If det(M1) = 0, there is no inverse.'),
        'Matrix Multiply':              Func(mat_mult,       'mats',     'M1 * M2 =\n',                             'Multiplies M1 by M2 (on the right).'),
        'Project (vec on vec)':         Func(project,        'vecs',     'Proj_{v2}(v1) =\n',                       'Projects v1 onto v2.'),
        'Project (vec on mat)':         Func(project,        'vecmat',   'Proj_{M1}(v1) =\n',                       'Projects v1 onto the subspace spanned by the columns of M1.'),
        'M^T * M':                      Func(aTa,            'mat',      'M^T * M =\n',                             'Multiplies the transpose of M1 by M1 (on the right). The resulting matrix is both square and symmetric.'),
        'GS Algorithm':                 Func(gs,             'mat',      'orthogonal matrix\n(spans col(M1))\n',    'The Gram Schmidt Algorithm is an algorithm which produces an orthogonal matrix which spans the same column space as the given matrix. It steals the first column of the original matrix, then uses a projection of the subsequent columns onto the current result to create orthogonal columns.'),
        'QR-Factorization':             Func(qr,             'mat',      'Q,R =\n',                                 'Factorizes M1 into Q and R, where Q is orthogonal and R is upper-triangular.'),
        'Normalize Vector':             Func(normalize_vec,  'vec',      'norm(v1) =\n',                            'Normalizes v1.'),
        'Normalize Matrix':             Func(normalize_mat,  'mat',      'norm(M1) =\n',                            'Normalizes the columns of M1.'),
        'Eigen Matrix':                 Func(eigen_matrix,   'mat',      'eigenvalues on diagonal:\n',              'Uses the QR-algorithm to create a (hopefully) upper-triangular matrix with the eigenvalues of M1 on the diagonal. May not work all of the time depending on M1, does not work if M1 has complex eigenvalues.')
    }

# -- button functions
def clr_text_fields():
    """ Clears all text fields. """
    for t in text_list:
        t.config(state = tk.NORMAL)
        t.delete("1.0", tk.END)
        if current_operation_text.get() != "None Selected":
            set_active_boxes(FUNCS[current_operation_text.get()].variables)
    RESULT.config(state = tk.DISABLED)

def random_matrix():
    """
    Creates random m x n matrix where n and m are gotten from their respective
    text boxes and inputs it into the matrix 1 text field. Range of values
    from 0 to 100, will create fractions if fraction checkbox is checked.
    """
    # make sure maxsize and minsize are ints
    try:
        r_max = int(random_maxsize.get())
        r_min = int(random_minsize.get())
    except:
        messagebox.showerror('Error: Invalid Input', "Your randomness settings are invalid. Make sure your max/min settings are integers.")
        return
    n = int(n_text.get())
    m = int(m_text.get())
    show_frac = bool(show_fractions_in_random.get())

    final_string = ''
    for row in range(m):
        for col in range(n):
            if show_frac:
                final_string += str(Fraction(random.randint(r_min, r_max), random.randint(max(1, r_min), r_max)))
            else:
                final_string += str(random.randint(r_min, r_max))
            final_string += ', '
        final_string = final_string[:-2]
        final_string += '\n'

    final_string = final_string[:-1]
    M1.config(state = tk.NORMAL)
    M1.delete("1.0", tk.END)
    M1.insert(tk.END, final_string)
    if current_operation_text.get() != "None Selected":
        set_active_boxes(FUNCS[current_operation_text.get()].variables)

def random_vector():
    """
    Creates random m x 1 vector where n is gotten from its respective
    text box and inputs it into the vector 1 text field. Range of values
    from 0 - 100, will create fractions if fraction checkbox is checked.
    """
    # make sure maxsize and minsize are ints
    try:
        r_max = int(random_maxsize.get())
        r_min = int(random_minsize.get())
    except:
        messagebox.showerror('Error: Invalid Input', "Your randomness settings are invalid. Make sure your max/min settings are integers.")
        return
    m = int(m_text.get())
    show_frac = bool(show_fractions_in_random.get())

    final_string = ''
    for row in range(m):
        if show_frac:
            final_string += str(Fraction(random.randint(r_min, r_max), random.randint(max(1, r_min), r_max)))
        else:
            final_string += str(random.randint(r_min, r_max))
        final_string += ', '
    final_string = final_string[:-2]
    V1.config(state = tk.NORMAL)
    V1.delete("1.0", tk.END)
    V1.insert(tk.END, final_string)
    if current_operation_text.get() != "None Selected":
        set_active_boxes(FUNCS[current_operation_text.get()].variables)

def set_default_random_settings():
    random_maxsize.set("10")
    random_minsize.set("0")
    show_fractions_in_random.set(1)

def show_random_settings():
    """ Shows the random settings window. """
    settings_win = tk.Toplevel(win)
    settings_win.title("Random Settings")
    settings_win.grab_set()
    settings_win.minsize(240, 140)
    settings_win.columnconfigure(0, weight = 1)
    settings_win.columnconfigure(1, weight = 1)

    maxsize_label = tk.Label(settings_win, text = "Maximum Random Number:")
    minsize_label = tk.Label(settings_win, text = "Minimum Random Number (>= 0):")
    maxsize_text = tk.Entry(settings_win, textvariable = random_maxsize, width = 6)
    minsize_text = tk.Entry(settings_win, textvariable = random_minsize, width = 6)
    fractions_check = tk.Checkbutton(settings_win, text = "Use Fractions in Random Generation?", variable = show_fractions_in_random)
    default_button = tk.Button(settings_win, text = "Reset to Default", command = set_default_random_settings)
    exit_button = tk.Button(settings_win, text = "Exit Settings", command = settings_win.destroy)

    maxsize_label.grid(row = 0, column = 0, pady = 5, sticky = 'e')
    minsize_label.grid(row = 1, column = 0, pady = 5, sticky = 'e')
    maxsize_text.grid(row = 0, column = 1, pady = 5, sticky = 'w')
    minsize_text.grid(row = 1, column = 1, pady = 5, sticky = 'w')
    fractions_check.grid(row = 2, column = 0, pady = 5, columnspan = 2)
    default_button.grid(row = 3, column = 0, pady = 5, columnspan = 2)
    exit_button.grid(row = 4, column = 0, pady = 5, columnspan = 2)

def display_info():
    """ Displays info about currently selected function. """
    current_op = current_operation_text.get()
    if current_op == "None Selected":
        return
    messagebox.showinfo(current_op, FUNCS[current_op].info)


def show_result(result):
    """
    Puts result on the screen in the result box.
    - result is a string.
    """
    RESULT.config(state = tk.NORMAL)
    RESULT.delete("1.0", tk.END)
    RESULT.insert(tk.END, result)
    RESULT.config(state = tk.DISABLED)

def copy():
    """ Copy current result box text to clipboard. """
    if FUNCS[current_operation_text.get()].func == qr:
        messagebox.showerror("Not supported", "Currently cannot do that when the result is multiple answers.")
        return
    win.clipboard_clear()
    txt_to_copy = CURRENT_RESULT
    if txt_to_copy != '':
        txt = get_csv(txt_to_copy)
        win.clipboard_append(txt)

def convert_to_frac(exact):
    """
    Converts current result from decimal to fractions. exact is a bool, if true,
    the conversion will 100% accurate down to the decimal point rounding. if false,
    conversion will be approximated.
    """
    if FUNCS[current_operation_text.get()].func == qr:
        messagebox.showerror("Not supported", "Currently cannot do that when the result is multiple answers.")
        return
    global CURRENT_RESULT
    if CURRENT_RESULT != '':
        current = CURRENT_RESULT
        if isinstance(current, (list, np.ndarray)):
            if isinstance(current[0], (list, np.ndarray)):
                # current result is a matrix
                row_size = len(current)
                col_size = len(current[0])
                if exact: result = [[dec_to_frac_exact(current[i][j]) for j in range(col_size)] for i in range(row_size)]
                else: result = [[dec_to_frac_approx(current[i][j]) for j in range(col_size)] for i in range(row_size)]
            else:
                # current result is a vector
                size = len(current)
                if exact: result = [dec_to_frac_exact(current[i]) for i in range(size)]
                else: result = [dec_to_frac_approx(current[i]) for i in range(size)]
        else:
            # current result is a scalar
            if exact: result = dec_to_frac_exact(current)
            else: result = dec_to_frac_approx(current)
        CURRENT_RESULT = result
        msg = FUNCS[current_operation_text.get()].text
        show_result(msg + format_answer(result))

def convert_to_decimal():
    """ Converts current result from fractions to decimals. """
    if FUNCS[current_operation_text.get()].func == qr:
        messagebox.showerror("Not supported", "Currently cannot do that when the result is multiple answers.")
        return
    global CURRENT_RESULT
    if CURRENT_RESULT != '':
        current = CURRENT_RESULT
        if isinstance(current, (list, np.ndarray)):
            if isinstance(current[0], (list, np.ndarray)):
                # current result is a matrix
                row_size = len(current)
                col_size = len(current[0])
                result = [[Fraction(float(current[i][j])) for j in range(col_size)] for i in range(row_size)]
            else:
                # current result is a vector
                size = len(current)
                result = [Fraction(float(current[i])) for i in range(size)]
        else:
            # current result is a scalar
            result = Fraction(float(current))
        CURRENT_RESULT = result
        msg = FUNCS[current_operation_text.get()].text
        show_result(msg + format_answer(result))


#-------------------------------------------------------------------#
# -- longer calculator functions start here
def calc():
    """
    Execute calculation of currently-selected operation and print
    the result onto the screen.
    """
    current_op = current_operation_text.get()
    if current_op == "None Selected": return
    current_func = FUNCS[current_op]
    f = current_func.func
    active_items = current_func.variables
    v1 = return_vector(V1)
    v2 = return_vector(V2)
    m1 = return_matrix(M1)
    m2 = return_matrix(M2)
    result = ''

    if active_items == 'vecs':
        if valid_vecs(v1, v2):
            if current_op == 'Subtract':
                result = f(v1, neg_vec(v2))
            else:
                result = f(v1, v2)
        else: return

    elif active_items == 'vecmat':
        if is_vector(v1) and is_matrix(m1):
            if len(v1) == len(m1[0]) and (f == vec_mat_mult or f == solve):
                result = f(m1, v1)
                if f == solve and not result:
                    messagebox.showerror('Error', "The provided matrix was not invertible.")
                    return
            elif len(v1) == len(m1) and f == project:
                result = f(v1, m1)
            else:
                messagebox.showerror("Error: Invalid Input", "Make sure the vector and matrix have proper lengths. For projection, the size of the vector must be the same as the size of the columns of the matrix. For multiplication, the size of the vector must be the same as the number of columns in the matrix.")
                return
        else:
            messagebox.showerror('Error: Invalid Input', "One or both of the inputs are invalid.")
            return

    elif active_items == 'vec':
        if is_vector(v1):
            result = f(v1)
        else: return

    elif active_items == 'mat':
        if is_matrix(m1):
            if f == qr:
                result_1, result_2 = f(m1)
                msg = current_func.text
                msg += format_answer(result_1) + '\n'
                msg += format_answer(result_2)
                show_result(msg)
                return
            result = f(m1)
            if f == inverse and not result:
                messagebox.showerror('Error', "The provided matrix was not invertible (either determinant = 0, or it was not square).")
                return
            elif (f == det or f == det_slow) and not result:
                messagebox.showerror('Error', "The provided matrix was not square, so it does not have a determinant.")
                return
        else: return

    elif active_items == 'mats':
        if valid_mats(m1, m2):
            result = f(m1, m2)
        else: return

    else:
        tk.messagebox.showerror("Something went wrong...", "Something went wrong during calculation.")
        return
    global CURRENT_RESULT
    CURRENT_RESULT = result
    msg = current_func.text
    msg += format_answer(result)
    show_result(msg)

def set_active_boxes(t):
    """
    Sets active text boxes based on t.
    - t is a string to signify which text boxes should be active.
      Can be either 'vec', 'vecs', 'vecmat', 'mats', or 'mat'.
    """
    if t == 'vecs':
        V1.config(state = tk.NORMAL, bg = "white")
        V2.config(state = tk.NORMAL, bg = "white")
        M1.config(state = tk.DISABLED, bg = "gray64")
        M2.config(state = tk.DISABLED, bg = "gray64")
    elif t == 'vecmat':
        V1.config(state = tk.NORMAL, bg = "white")
        V2.config(state = tk.DISABLED, bg = "gray64")
        M1.config(state = tk.NORMAL, bg = "white")
        M2.config(state = tk.DISABLED, bg = "gray64")
    elif t == 'vec':
        V1.config(state = tk.NORMAL, bg = "white")
        V2.config(state = tk.DISABLED, bg = "gray64")
        M1.config(state = tk.DISABLED, bg = "gray64")
        M2.config(state = tk.DISABLED, bg = "gray64")
    elif t == 'mat':
        V1.config(state = tk.DISABLED, bg = "gray64")
        V2.config(state = tk.DISABLED, bg = "gray64")
        M1.config(state = tk.NORMAL, bg = "white")
        M2.config(state = tk.DISABLED, bg = "gray64")
    elif t == 'mats':
        V1.config(state = tk.DISABLED, bg = "gray64")
        V2.config(state = tk.DISABLED, bg = "gray64")
        M1.config(state = tk.NORMAL, bg = "white")
        M2.config(state = tk.NORMAL, bg = "white")


#-------------------------------------------------------------------#
#-------------------------------------------------------------------#
#--- tkinter setup
win = tk.Tk()
win.title("Linear Algebra Calculator 2.5")
win.geometry("550x700")
win.minsize(525, 600)
default_font = ('Courier New', '12')
bigger_font = ('Courier New', '13')

# -- define misc functions --
def change_dropdown(*args):
    current_op = current_operation_text.get()
    set_active_boxes(FUNCS[current_op].variables)

def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return("break")

# -- define variables --
current_operation_text = tk.StringVar(value = 'None Selected')
show_fractions_in_random = tk.IntVar(value = 1) # 0 or 1
random_maxsize = tk.StringVar(value = "10")
random_minsize = tk.StringVar(value = "0")

#-------------------------------------------------------------------#
# -- define frames --
# v label frames for debugging ui layout
# button_frame = tk.LabelFrame(win, text = "buttons")
# input_frame = tk.LabelFrame( win, text = "inputs")
# bottom_frame = tk.LabelFrame(win, text = "bottom")
button_frame = tk.Frame(win)
input_frame = tk.Frame( win)
bottom_frame = tk.Frame(win)
# -- layout the frames --
button_frame.grid(row = 0, column = 0, ipady = 3, columnspan = 2)
input_frame.grid( row = 1, column = 0, ipady = 3, columnspan = 2)
bottom_frame.grid(row = 4, column = 0, ipady = 3, columnspan = 2)


# -- widgets for button frame --
dropdown_label = tk.Label(button_frame, text = "Select Operation:")
dropdown = tk.OptionMenu(button_frame, current_operation_text, *[key for key in FUNCS])
info = tk.Button(button_frame, bitmap = "info", command = display_info)
clear_button = tk.Button(button_frame, text = "Clear Text Fields", command = clr_text_fields)
calc_button = tk.Button(button_frame, text = "Calculate", command = calc)
# -- button frame widget layout --
dropdown_label.grid(row = 0, column = 0, sticky = 'e')
dropdown.grid(row = 0, column = 1, sticky = 'w')
info.grid(row = 0, column = 2)
clear_button.grid(row = 1, column = 0, pady = 3, columnspan = 3)
calc_button.grid(row = 2, column = 0, pady = 3, columnspan = 3)


# -- widgets for input frame --
V1_label = tk.Label(input_frame, text = "Vector 1:")
V2_label = tk.Label(input_frame, text = "Vector 2:")
M1_label = tk.Label(input_frame, text = "Matrix 1:")
M2_label = tk.Label(input_frame, text = "Matrix 2:")
V1 = tk.Text(input_frame, state = tk.DISABLED, bg = "gray64", height = 1, width = 25, font = default_font)
V2 = tk.Text(input_frame, state = tk.DISABLED, bg = "gray64", height = 1, width = 25, font = default_font)
M1 = tk.Text(input_frame, state = tk.DISABLED, bg = "gray64", height = 6, width = 25, font = default_font)
M2 = tk.Text(input_frame, state = tk.DISABLED, bg = "gray64", height = 6, width = 25, font = default_font)
# -- input frame widget layout --
V1_label.grid(row = 0, column = 0)
V2_label.grid(row = 0, column = 1)
M1_label.grid(row = 2, column = 0)
M2_label.grid(row = 2, column = 1)
V1.grid(row = 1, column = 0, padx = 5, pady = 5)
V2.grid(row = 1, column = 1, padx = 5, pady = 5)
M1.grid(row = 3, column = 0, padx = 5, pady = 5)
M2.grid(row = 3, column = 1, padx = 5, pady = 5)


# -- widgets for inner input frame --
# inner_input_frame = tk.LabelFrame(input_frame, text = "inner")
inner_input_frame = tk.Frame(input_frame)
rand_mat_button = tk.Button(inner_input_frame, text = "Create Random m x n Matrix", command = random_matrix)
rand_vec_button = tk.Button(inner_input_frame, text = "Create Random m x 1 Vector", command = random_vector)
n_label = tk.Label(inner_input_frame, text = "n =")
m_label = tk.Label(inner_input_frame, text = "m =")
n_text = tk.Spinbox(inner_input_frame, from_ = 1, to = 10, state = "readonly", width = 3)
m_text = tk.Spinbox(inner_input_frame, from_ = 1, to = 10, state = "readonly", width = 3)
random_settings_button = tk.Button(inner_input_frame, text = "Randomness Settings", command = show_random_settings)
# -- inner input frame layout --
inner_input_frame.grid(row = 4, column = 0, columnspan = 2)
rand_mat_button.grid(row = 1, column = 0, padx = 5, pady = 5)
rand_vec_button.grid(row = 0, column = 0, padx = 5, pady = 5)
n_label.grid(row = 0, column = 1, pady = 5, sticky = 'e')
m_label.grid(row = 1, column = 1, pady = 5, sticky = 'e')
n_text.grid(row = 0, column = 2, pady = 5, sticky = 'w')
m_text.grid(row = 1, column = 2, pady = 5, sticky = 'w')
random_settings_button.grid(row = 0, column = 3, padx = 5, pady = 5, rowspan = 2)


# -- result widgets --
result_label = tk.Label(win, text = "-------------- RESULT: --------------")
RESULT = tk.Text(win, state = tk.DISABLED, height = 20, width = 50, font = bigger_font)
scroll = tk.Scrollbar(win, command = RESULT.yview)
# -- result layout --
result_label.grid(row = 2, column = 0, columnspan = 2)
RESULT.grid(row = 3, column = 0, sticky = 'nswe')
scroll.grid(row = 3, column = 1, sticky = 'nsw')


# -- widgets for bottom button --
copy_button = tk.Button(bottom_frame, text = "Copy Result", command = copy)
approx_frac_button = tk.Button(bottom_frame, text = "Convert to Fraction (approx)", command = lambda: convert_to_frac(False))
decimal_button = tk.Button(bottom_frame, text = "Convert to Decimal", command = convert_to_decimal)
# -- bottom button frame widget layout --
copy_button.grid(row = 0, column = 0, pady = 5, padx = 5)
approx_frac_button.grid(row = 0, column = 1, pady = 5, padx = 5)
decimal_button.grid(row = 0, column = 2, pady = 5, padx = 5)


#-------------------------------------------------------------------#
# -- misc final UI setups --
win.grid_columnconfigure(0, weight = 1) # center every widget
win.grid_rowconfigure(3, weight = 1) # row which contains result box

current_operation_text.trace('w', change_dropdown) # call change_dropdown when current_operation_text changes

n_text.config(state = tk.NORMAL)
m_text.config(state = tk.NORMAL)
n_text.delete(0, tk.END)
m_text.delete(0, tk.END)
n_text.insert(tk.END, '3')
m_text.insert(tk.END, '3')
n_text.config(state = "readonly")
m_text.config(state = "readonly")

text_list = [V1, V2, M1, M2]
for t in text_list:
    t.bind("<Tab>", focus_next_widget)

RESULT['yscrollcommand'] = scroll.set


win.mainloop()