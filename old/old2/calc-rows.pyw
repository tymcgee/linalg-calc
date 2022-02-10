# Tynan McGee
# 3/15/2021
# update 4/25/2021 (adding more fraction capability)
# linear algebra calculator (vertical inputs are columns, like normal)

from tkinter import *
from tkinter import messagebox
from fraction import *
import numpy as np
from vec_mat_funcs import *
from matrix_format import *

# https://www.tutorialspoint.com/python3/python_gui_programming.htm

np.set_printoptions(precision=3, suppress=True)


if __name__ == "__main__":
    win = Tk()
    win.title("Linear Algebra Calculator 2.0")
    win.geometry('650x770')
    for i in range(3):
        win.grid_rowconfigure(i, weight=1)
    win.grid_columnconfigure(0, weight=1)
    CURRENT_RESULT = ''
    
    def getText(t):
        inp = t.get("1.0", END)
        inp = inp.replace(' ', '')
        inp = inp.split('\n')
        if inp[0] == '': return 0 # string is empty
        del inp[-1] # remove empty element where \n got split off
        return inp

    def returnVec(t):
        """ takes in text field t, gets its contents, and if it contains a vector, 
            converts it into one and returns it. input is tkinter text field. """
        errmsg = 'Invalid Input.\nExample input: \n"1, 2, 3, 4" \nfor a vector, or\n"1, 2, 3, 4\n 5, 6, 7, 8" \nfor a matrix.\nCommas must be used to separate numbers (except at linebreaks).'
        inp = getText(t)
        if inp == 0: return 0
        inp = inp[0].split(',')
        for i,n in enumerate(inp):
            try: inp[i] = get_frac_from_string(n)
            except ValueError: # if it didn't work, input wasn't exclusively numbers
                messagebox.showerror('Error: Invalid Input', errmsg)
                return 0
        return inp
    
    def returnMat(t):
        """ takes in text field t, gets its contents, and if it contains a matrix,
            converts it into one and returns it. input is a tkinter text field. """
        errmsg = 'Invalid Input.\nExample input: \n"1, 2, 3, 4" \nfor a vector, or\n"1, 2, 3, 4\n 5, 6, 7, 8" \nfor a matrix.\nCommas must be used to separate numbers (except at linebreaks).'
        inp = getText(t)
        if inp == 0: return 0
        for i,l in enumerate(inp):
            inp[i] = l.split(',')
        for i,l in enumerate(inp):
            for j,n in enumerate(l):
                try: inp[i][j] = get_frac_from_string(n)
                except ValueError:
                    messagebox.showerror('Error: Invalid Input', errmsg)
                    return 0
        return inp

    def is_vector(v):
        """ returns bool of whether input v is actually an m x n vector. """
        vec = True
        if isinstance(v, (list, np.ndarray)):
            for n in v:
                if isinstance(n, Fraction):
                    if not isinstance(n.decimal(), (float, int, np.floating, np.integer)): vec = False
                else: vec = False
        else: vec = False
        return vec
    
    def is_matrix(m):
        """ returns bool of whether input m is actually an m x n matrix. """
        mat = True
        if isinstance(m, (list, np.ndarray)) and isinstance(m[0], (list, np.ndarray)):
            l = len(m[0])
            for i in m:
                if len(i) != l: # rows aren't all the same length
                    mat = False
                for j in i:
                    if isinstance(j, Fraction):
                        if not isinstance(j.decimal(), (float, int, np.floating, np.integer)): mat = False
                    else: mat = False
        else: mat = False
        return mat

    def valid_vecs(v1, v2):
        """ returns bool of whether the given vectors are both vectors, 
            and are the same length. """
        if is_vector(v1) and is_vector(v2):
            if len(v1) == len(v2):
                return True
            else:
                messagebox.showerror('Error: Invalid Input', "The vectors must be the same length!")
                return False
        else:
            messagebox.showerror('Error: Invalid Input', "One or both of the vectors are invalid.")
            return False
    
    def valid_vecmat(v, m):
        """ returns bool of whether the given vector v and matrix m are valid for projection 
            (v has the same num of rows as the columns of m). """
        if is_vector(v) and is_matrix(m):
            if len(v) == len(m[0]):
                return True
            else:
                messagebox.showerror('Error: Invalid Input', "The vector must have the same number of rows as the matrix has columns!")
                return False
        else:
            messagebox.showerror('Error: Invalid Input', "One or both of the inputs are invalid.")
            return False
    
    def valid_mats(m1, m2):
        """ returns bool of whether the given matrices are valid for multiplying together. """
        if is_matrix(m1) and is_matrix(m2):
            if len(m1[0]) == len(m2): # m1[0] is num of cols, m2 is num of rows
                return True
            else:
                messagebox.showerror('Error: Invalid Input', "Make sure M1 has the same number of columns as M2 has rows.")
                return False
        else:
            messagebox.showerror('Error: Invalid Input', "One or both of the matrices are invalid.")
            return False

    def clr_text_fields():
        """ clears all text fields. """
        for t in text_list:
            t.config(state = NORMAL)
            t.delete("1.0", END)
            change_text(change_text_dict[current_operation_text.get()])
        RESULT.config(state = DISABLED)
    
    def show_result(result):
        """ puts result on the screen in the result box (input is string). """
        RESULT.config(state = NORMAL)
        RESULT.delete("1.0", END)
        RESULT.insert(END, result)
        RESULT.config(state = DISABLED)

    def get_csv(m):
        """ extracts the numbers from vector/matrix/number m and puts them in csv format. 
            returns resulting comma-separated string. """
        final = ''
        if is_vector(m):
            for n in m:
                if n.flt:
                    final += str(round(n.decimal(), 3)) + ', '
                else: 
                    final += str(n) + ', '
            final = final[:-2]
            return final
        elif is_matrix(m):
            for row in m:
                for n in row:
                    if n.flt:
                        final += str(round(n.decimal(), 3)) + ', '
                    else:
                        final += str(n) + ', '
                final = final[:-2]
                final += '\n'
            final = final[:-1]
            return final
        else:
            if m.flt: return str(round(m.decimal(), 3))
            else: return str(m)
    
    def copy():
        win.clipboard_clear()
        txt_to_copy = CURRENT_RESULT
        if txt_to_copy != '':
            txt = get_csv(txt_to_copy)
            win.clipboard_append(txt)
    
    def set_current_result(result):
        global CURRENT_RESULT
        CURRENT_RESULT = result
    
    #---------------------------------------------------------
    function_dict = {
        'Add':vec_add,
        'Subtract':vec_add,
        'Matrix-Vector Multiply':vec_mat_mult,
        'Inner Product':inner_product,
        'Project (vec on vec)':project,
        'Project (vec on mat)':project,
        'Determinant':det,
        'RREF':rref,
        'Matrix Multiply':mat_mult,
        'M^T * M':aTa,
        'GS Algorithm':gs,
        'Normalize Vector':normalize_vec,
        'Normalize Matrix':normalize_mat,
    }
    change_text_dict = {
        'Add':'vecs',
        'Subtract':'vecs',
        'Matrix-Vector Multiply':'vecmat',
        'Inner Product':'vecs',
        'Project (vec on vec)':'vecs',
        'Project (vec on mat)':'vecmat',
        'Determinant':'mat',
        'RREF':'mat',
        'Matrix Multiply':'mats',
        'M^T * M':'mat',
        'GS Algorithm':'mat',
        'Normalize Vector':'vec',
        'Normalize Matrix':'mat',
    }
    text_dict = {
        'Add':'v1 + v2 =\n',
        'Subtract':'v1 - v2 =\n',
        'Matrix-Vector Multiply':'M1 * v1 =\n',
        'Inner Product':'<v1, v2> =\n',
        'Project (vec on vec)':'Proj_{v2}(v1) =\n',
        'Project (vec on mat)':'Prov_{M1}(v1) =\n',
        'Determinant':'Det(M1) =\n',
        'RREF':'rref(M1) =\n',
        'Matrix Multiply':'M1 * M2 =\n',
        'M^T * M':'M^T * M =\n',
        'GS Algorithm':'orthogonal matrix\n(spans col(M1)):\n',
        'Normalize Vector':'norm(v1) =\n',
        'Normalize Matrix':'norm(M1) =\n',
    }

    def calc():
        current_op = current_operation_text.get()
        f = function_dict[current_op]
        active_items = change_text_dict[current_op]
        v1 = returnVec(V1)
        v2 = returnVec(V2)
        m1 = returnMat(MAT1)
        m2 = returnMat(MAT2)

        if active_items == 'vecs':
            if valid_vecs(v1, v2):
                if current_op == 'Subtract':
                    result = f(v1, neg_vec(v2))
                else:
                    result = f(v1, v2)
            else: return
        elif active_items == 'vecmat':
            if valid_vecmat(v1, m1):
                result = f(v1, m1)
            else: return
        elif active_items == 'vec':
            if is_vector(v1):
                result = f(v1)
            else: return
        elif active_items == 'mat':
            if is_matrix(m1):
                result = f(m1)
            else: return
        elif active_items == 'mats':
            if valid_mats(m1, m2):
                result = f(m1, m2)
            else: return
        else:
            raise ValueError('something went wrong in the calc() function..')
        set_current_result(result)
        msg = text_dict[current_op]
        if is_vector(result):
            msg += format_vector(result)
        elif is_matrix(result):
            msg += format_matrix(result)
        else:
            msg += format_fraction(result)
        show_result(msg)

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
    result_frame = Frame(win)
    frame_list = [button_frame, vector_frame, matrix_frame, result_frame]
    for i,f in enumerate(frame_list):
        f.grid(row = i, column = 0, padx = 5, pady = 3, ipadx = 2, ipady = 4)
        for n in range(len(frame_list)):
            f.grid_columnconfigure(n, weight=1)
            f.grid_rowconfigure(n, weight=1)
    
    # ---- buttons, dropdowns ----
    current_operation_text = StringVar(value = 'None Selected')

    dropdown = OptionMenu(button_frame, current_operation_text, 'Add', 'Subtract', 'Matrix-Vector Multiply', 'Inner Product', 'Project (vec on vec)', 'Project (vec on mat)', 'Determinant', 'RREF', 'Matrix Multiply', 'M^T * M', 'GS Algorithm', 'Normalize Vector', 'Normalize Matrix')
    dropdown.grid(row = 0, column = 1)
    drop_label = Label(button_frame, text = "Select Operation:")
    drop_label.grid(row = 0, column = 0)

    current_operation_text.trace('w', change_dropdown)

    calc_button = Button(button_frame, width = 10, height = 1, text = "Calculate", command = calc)
    calc_button.grid(row = 2, column = 0, columnspan = 2, pady = 3)
    clear_button = Button(button_frame, width = 15, height = 1, text = "Clear text fields", command = clr_text_fields)
    clear_button.grid(row = 1, column = 0, columnspan = 2, pady = 3)

    # ---- text fields ----
    V1 = Text(vector_frame, height = 1, width = 25, state = DISABLED, bg = "gray64", font = default_font)
    V2 = Text(vector_frame, height = 1, width = 25, state = DISABLED, bg = "gray64", font = default_font)
    MAT1 = Text(matrix_frame, height = 6, width = 25, state = DISABLED, bg = "gray64", font = default_font)
    MAT2 = Text(matrix_frame, height = 6, width = 25, state = DISABLED, bg = "gray64", font = default_font)
    V1.grid(row = 1, column = 0, pady = 3, padx = 10)
    V2.grid(row = 1, column = 1, pady = 3, padx = 10)
    MAT1.grid(row = 1, column = 0, padx = 10)
    MAT2.grid(row = 1, column = 1, padx = 10)

    RESULT = Text(result_frame, height = 16, width = 50, state = DISABLED, font = bigger_font)
    RESULT.grid(row = 1, column = 0, pady = 15)
    copy_button = Button(result_frame, width = 10, height = 1, text = "Copy Result", command = copy)
    copy_button.grid(row = 2, column = 0, pady = 5)

    text_list = [V1, V2, MAT1, MAT2, RESULT]

    for t in text_list:
        t.bind("<Tab>", focus_next_widget) # tab moves to next widget

    lbl1 = Label(vector_frame,      text = "Vector 1:")
    lbl2 = Label(vector_frame,      text = "Vector 2:")
    lbl3 = Label(matrix_frame,      text = "Matrix 1:")
    lbl4 = Label(matrix_frame,      text = "Matrix 2:")
    lbl5 = Label(result_frame,      text = "----------------- Result: -----------------")
    lbl1.grid(row = 0, column = 0, padx = 5)
    lbl2.grid(row = 0, column = 1, padx = 5)
    lbl3.grid(row = 0, column = 0, padx = 5)
    lbl4.grid(row = 0, column = 1, padx = 5)
    lbl5.grid(row = 0, column = 0, padx = 5)

    win.mainloop()