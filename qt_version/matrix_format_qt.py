from fraction_qt import Fraction
import numpy as np
# assumes vector/matrix inputs are made of fraction objects
## WARNING
## THIS FILE CONTAINS COPIOUS AMOUNTS OF DISGUSTING STRING MANIPULATION
## READ AT YOUR OWN RISK

def format_answer(n):
    """
    Decides whether n is a scalar, vector, or matrix,
    and formats it into a nice looking multi-line string.
    - n can be a scalar (int/float), vector (list), or 
      matrix (list of lists).
    - Returns a string (or False if n is invalid).
    """
    if isinstance(n, (list, np.ndarray)):
        if isinstance(n[0], (list, np.ndarray)):
            # n is a matrix
            return format_matrix(n)
        # n is a vector
        return format_vector(n)
    # n is a scalar
    if isinstance(n, (Fraction, float, int, np.floating, np.integer)):
        return format_fraction(n)
    return False

def format_fraction(f):
    """
    Formats a fraction object into a nice looking multi-line string.
    For example, 3/2 gets turned into 
      3
     ―――
      2  .
    - f is a fraction object.
    - Returns a string.
    """
    if isinstance(f, Fraction) and not f.flt and f.denominator != 1:
        num = str(f.numerator)
        den = str(f.denominator)
        num_len = len(num)
        den_len = len(den)
        max_len = max(num_len, den_len)
        min_len = min(num_len, den_len)
        diff = max_len - min_len

        len_of_line = max_len + 2
        line = "―" * len_of_line
        space = " " * (diff // 2)
        afterspace = " " * (diff - (diff // 2))
        if max_len == num_len:
            n = f" {num} "
            d = f" {space}{den}{afterspace} "
        else:
            n = f" {space}{num}{afterspace} "
            d = f" {den} "

        result = f"{n}\n{line}\n{d}"
        return result

    if f.flt:
        return str(round(float(f), 3))
    if f.denominator == 1:
        return str(f)
    raise TypeError("format_fraction() only takes fraction objects as arguments")

def is_frac_in_row(row):
    frac_exists = False
    for f in row:
        if '\n' in f:
            frac_exists = True
    return frac_exists

def get_lines(len_col, i, frac_exists):
    """
    Returns starts and ends of lines 1, 2, and 3, 
    depending on the length of the column, the current row, 
    and whether the row has a fraction.
    - len_col is the length of the column (int).
    - i is the index of the current position in the row (int).
    - frac_exists is a bool for whether there's a fraction in the row.
    - returns six strings:
    -- line_1, line_2, line_3 are the starts of each line.
    -- end_1, end_2, end_3 are the ends of each line.
    """
    line_1 = None
    line_2 = None
    line_3 = None
    eol1 = None
    eol2 = None
    eol3 = None
    if i == 0:
        # first row
        if frac_exists:
            line_1 = ' ⌈ '
            line_2 = ' ⏐ '
            line_3 = ' ⏐ '
            eol1 = ' ⌉'
            eol2 = ' ⏐'
            eol3 = ' ⏐'
        else:
            line_1 = ' ⌈ '
            eol1 = ' ⌉'
    elif i == len_col - 1:
        # last row
        if frac_exists:
            line_1 = ' ⏐ '
            line_2 = ' ⏐ '
            line_3 = ' ⌊ '
            eol1 = ' ⏐'
            eol2 = ' ⏐'
            eol3 = ' ⌋'
        else:
            line_1 = ' ⌊ '
            eol1 = ' ⌋'
    else:
        if frac_exists:
            line_1 = ' ⏐ '
            line_2 = ' ⏐ '
            line_3 = ' ⏐ '
            eol1 = ' ⏐'
            eol2 = ' ⏐'
            eol3 = ' ⏐'
        else:
            line_1 = ' ⏐ '
            eol1 = ' ⏐'
    return line_1, line_2, line_3, eol1, eol2, eol3

def format_vector(v):
    """
    Formats a vector into a vertical string.
    - v is a vector (list of fraction objects).
    - Returns a string.
    """
    new_v = [format_fraction(f) for f in v]
    max_length = 0
    final = ''
    for i in range(len(new_v)):
        if '\n' in new_v[i]:
            if (x := (len(new_v[i].split('\n')[1]))) > max_length:
                max_length = x
        elif len(new_v[i]) > max_length:
            max_length = len(new_v[i])
    for i in range(len(new_v)):
        diff = 0
        frac_exists = '\n' in new_v[i]
        line_1, line_2, line_3, eol1, eol2, eol3 = get_lines(len(new_v), i, frac_exists)
        if '\n' in new_v[i]:
            a = new_v[i].split('\n')
            if len(a[1]) < max_length:
                diff = max_length - len(a[1])
                # i'm doing diff // 2 in an attempt to center the items in the vector
                line_1 += ' ' * (diff // 2)
                line_2 += ' ' * (diff // 2)
                line_3 += ' ' * (diff // 2)
            line_1 += a[0]
            line_2 += a[1]
            line_3 += a[2]
        else:
            if len(new_v[i]) < max_length:
                diff = max_length - len(new_v[i])
                line_1 += ' ' * (diff // 2)
            line_1 += new_v[i]

        line_1 += (' ' * (diff - (diff // 2))) + eol1
        if frac_exists:
            line_2 += (' ' * (diff - (diff // 2))) + eol2
            line_3 += (' ' * (diff - (diff // 2))) + eol3
            final += '\n'.join([line_1, line_2, line_3])
        else:
            final += line_1
        final += '\n ⏐ ' + (' ' * max_length) + ' ⏐\n'
    final = final[:-(max_length + 6)] # remove ^that extra line
    return final

def find_longest_strs(m):
    """
    Finds the longest strings in the columns of a matrix.
    - m is a matrix (list of lists of fraction objects)
    - Returns a list containing a number for each column in
      m, where the numbers represent the longest string
      in that column.
    """
    max_lengths = [0 for _ in range(len(m[0]))]
    # find longest string in each column
    for row in range(len(m)):
        for col in range(len(m[0])):
            if '\n' not in m[row][col]:
                max_lengths[col] = max(max_lengths[col], len(m[row][col]))
            else:
                dashes = m[row][col].split('\n')[1]
                dash_len = len(dashes)
                max_lengths[col] = max(max_lengths[col], dash_len)
    return max_lengths

def format_matrix(m):
    """
    Formats a matrix into a nice looking multi-line string.
    - m is a matrix (list of vectors).
    - Returns a string.
    """
    new_m = [[format_fraction(f) for f in m[i]] for i in range(len(m))]
    max_lengths = find_longest_strs(new_m)
    # format rows similar to vectors but with spaces between columns
    # according to max_lengths
    final = ''
    for i,row in enumerate(new_m):
        frac_exists = is_frac_in_row(row)
        line_1, line_2, line_3, eol1, eol2, eol3 = get_lines(len(new_m), i, frac_exists)
        for j,f in enumerate(row):
            diff = max_lengths[j] - len(f)
            if frac_exists:
                if '\n' in f:
                    a = f.split('\n')
                    # add spaces if not longest item in col
                    diff = max_lengths[j] - len(a[1])
                    prespace = diff // 2
                    postspace = diff - (diff // 2)
                    line_1 += ' ' * prespace
                    line_2 += ' ' * prespace
                    line_3 += ' ' * prespace
                    line_1 += a[0] + (' ' * postspace) + '   '
                    line_2 += a[1] + (' ' * postspace) + '   '
                    line_3 += a[2] + (' ' * postspace) + '   '  
                else:
                    length = len(f)
                    prespace = diff // 2
                    postspace = diff - (diff // 2)
                    line_1 += ' ' * prespace
                    line_2 += ' ' * prespace
                    line_3 += ' ' * prespace
                    line_1 += ' ' * length + (' ' * postspace) + '   '
                    line_2 += f + (' ' * postspace) + '   '
                    line_3 += ' ' * length + (' ' * postspace) + '   '
            # no fractions in row (just use line 1)
            else:
                # add spaces if not longest item in col
                prespace = diff // 2
                postspace = diff - (diff // 2)
                line_1 += ' ' * prespace
                line_1 += f + (' ' * postspace) + '   '

        line_1 = line_1[:-3]
        line_1 += eol1
        if frac_exists:
            line_2 = line_2[:-3]
            line_3 = line_3[:-3]
            line_2 += eol2
            line_3 += eol3
            final += '\n'.join([line_1, line_2, line_3])
        else:
            final += line_1
        final += '\n ⏐ ' + (' ' * (len(line_1) - 5)) + ' ⏐\n'
    final = final[:-(len(line_1) + 1)]
    return final

def get_csv(m):
    """
    Extracts the numbers from a scalar/vector/matrix 
    and puts them in csv format.
    - m is either a scalar, vector, or matrix.
    - Returns a string (comma separated list of numbers)
    """
    final = ''
    if isinstance(m, list):
        if isinstance(m[0], list):
            # m is a matrix
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
        # m is a vector
        for n in m:
            if n.flt:
                final += str(round(n.decimal(), 3)) + ', '
            else: 
                final += str(n) + ', '
        final = final[:-2]
        return final
    if m.flt: return str(round(m.decimal(), 3))
    return str(m)

if __name__ == "__main__":
    print(format_fraction(Fraction(111,2)))