import tkinter as tk
from tkinter import messagebox
from fraction import *

# -- vector/matrix retrieval and verification
def get_input(t):
    """
    Returns a list containing each line of text from t with spaces removed.
    - t is a tk.Text object containing comma separated numbers and fractions.
    - Returns a list of those numbers (each item in the list is a line of text
      from the input (a string)).
    """
    inp = t.get("1.0", tk.END)
    inp = inp.replace(' ', '')
    inp = inp.split('\n')
    if inp[0] == '': return 0 # string is empty
    del inp[-1] # remove empty element where \n got split off
    return inp
        
def return_vector(t):
    """
    Finds out whether the text in t contains a vector, and if it does,
    converts the text to a list of fraction objects and returns it.
    - t is a tk.Text object.
    - Returns 0 if t doesn't contain a vector, otherwise returns the vector 
      which it contains.
    """
    err_msg = 'Invalid input.\nExample input:\n"1, 2, 3, 4"\nfor a vector, or\n"1, 2, 3, 4\n5, 6, 7, 8"\n for a matrix.\nCommas must be used to separate numbers (except at linebreaks).'
    inp = get_input(t)
    if inp == 0: return 0
    inp = inp[0].split(',')
    for i,n in enumerate(inp):
        try: inp[i] = get_frac_from_string(n)
        except ValueError: # if it didn't work, input wasn't exclusively numbers
            messagebox.showerror('Error: Invalid Input', err_msg)
            return 0
    return inp

def return_matrix(t):
    """
    Finds out whether the text in t contains a matrix, and if it does,
    converts it to a list of lists of fraction objects and returns it.
    - t is a tk.Text object.
    - Returns 0 if t doesn't contain a matrix, otherwise returns the
      matrix which it contains.
    """
    err_msg = 'Invalid input.\nExample input:\n"1, 2, 3, 4"\nfor a vector, or\n"1, 2, 3, 4\n5, 6, 7, 8"\n for a matrix.\nCommas must be used to separate numbers (except at linebreaks).'
    inp = get_input(t)
    if inp == 0: return 0
    for i in range(len(inp)):
        inp[i] = inp[i].split(',')
    for i in range(len(inp)):
        for j in range(len(inp[i])):
            try: inp[i][j] = get_frac_from_string(inp[i][j])
            except ValueError:
                messagebox.showerror('Error: Invald Input', err_msg)
                return 0
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
    - Returns True or False depending on if both inputs are vectors
      and the same length.
    """
    if is_vector(v1) and is_vector(v2):
        if len(v1) == len(v2):
            return True
        else:
            messagebox.showerror('Error: Invalid Input', "The vectors must be the same length!")
            return False
    else:
        messagebox.showerror('Error: Invalid Input', "One or both of the vectors are invalid.")
        return False

def valid_mats(m1, m2):
    """
    Finds out whether m1 and m2 are both matrices where m1 has the
    same number of columns as m2 has rows.
    - m1 and m2 should be matrices (lists of lists of fraction objects).
    - Returns True or False depending on if both inputs are matrices
      and m1 has the same number of columns as m2 has rows.
    """
    if is_matrix(m1) and is_matrix(m2):
        m1_cols = len(m1[0])
        m2_rows = len(m2)
        if m1_cols == m2_rows:
            return True
        else:
            messagebox.showerror('Error: Invalid Input', "Make sure M1 has the same number of columns as M2 has rows.")
            return False
    else:
        messagebox.showerror('Error: Invalid Input', "One or both of the matrices are invalid.")
        return False