from fraction import Fraction
# assumes vector/matrix inputs are made of fraction objects

def format_fraction(f):
    """ f is a fraction object. returns string which looks like
        3/2 --> 3
               ⎯⎯⎯
                2 """
    if isinstance(f, Fraction) and not f.flt and f.denominator != 1:
        num = str(f.numerator)
        den = str(f.denominator)
        num_len = len(num)
        den_len = len(den)
        max_len = max(num_len, den_len)
        min_len = min(num_len, den_len)
        diff = max_len - min_len

        len_of_line = max_len + 2
        line = "⎯" * len_of_line
        space = " " * diff
        if max_len == num_len:
            n = f" {num} "
            d = f" {space}{den} "
        else:
            n = f" {space}{num} "
            d = f" {den} "

        result = f"{n}\n{line}\n{d}"
        return result

    elif f.flt:
        return str(round(float(f), 3))
    elif f.denominator == 1:
        return str(f)
    else: raise TypeError("format_fraction() only takes fraction objects as arguments")

def is_frac_in_row(row):
    frac_exists = False
    for f in row:
        if '\n' in f:
            frac_exists = True
    return frac_exists

def format_vector(v):
    new_v = []
    for i,f in enumerate(v):
        new_v.append(format_fraction(f))
    frac_exists = is_frac_in_row(new_v)
    line_1 = '  '
    line_2 = '[ '
    line_3 = '  '
    for n in new_v:
        if '\n' in n:
            a = n.split('\n')
            line_1 += a[0] + '  '
            line_2 += a[1] + ', '
            line_3 += a[2] + '  '
        else:
            length = len(n)
            line_1 += ' ' * length + '  '
            line_2 += n + ', '
            line_3 += ' ' * length + '  '
    line_1 = line_1[:-2]
    line_2 = line_2[:-2]
    line_3 = line_3[:-2]
    # line_1 += ']'
    line_2 += ' ]'
    # line_3 += ']'
    if frac_exists:
        final = '\n'.join([line_1, line_2, line_3])
    else:
        final = line_2
    return final

def find_longest_strs(m):
    max_lengths = []
    for i in range(len(m[0])):
        max_lengths.append(0)
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
    new_m = []
    for i,row in enumerate(m):
        new_m.append([])
        for j,f in enumerate(row):
            new_m[i].append(format_fraction(f))
    max_lengths = find_longest_strs(new_m)
    # format rows similar to vectors but with spaces between columns
    # according to max_lengths
    final = ''
    for i,row in enumerate(new_m):
        frac_exists = is_frac_in_row(row)
        line_1 = '   '
        line_2 = ' [ '
        line_3 = '   '
        for j,f in enumerate(row):
            if (0,0) == (i,j):
                line_1 = '   '
                line_2 = '[[ '
                line_3 = '   '
            if frac_exists:
                if '\n' in f:
                    a = f.split('\n')
                    # add spaces if not longest item in col
                    if len(a[1]) != max_lengths[j]:
                        diff = max_lengths[j] - len(a[1])
                        line_1 += ' ' * diff
                        line_2 += ' ' * diff
                        line_3 += ' ' * diff
                    line_1 += a[0] + '  '
                    line_2 += a[1] + ', '
                    line_3 += a[2] + '  '  
                else:
                    length = len(f)
                    if length != max_lengths[j]:
                        diff = max_lengths[j] - length
                        line_1 += ' ' * diff
                        line_2 += ' ' * diff
                        line_3 += ' ' * diff
                    line_1 += ' ' * length + '  '
                    line_2 += f + ', '
                    line_3 += ' ' * length + '  '
            # no fractions in row (just use line 2)
            else:
                length = len(f)
                # add spaces if not longest item in col
                if length != max_lengths[j]:
                    diff = max_lengths[j] - length
                    line_2 += ' ' * diff
                line_2 += f + ', '
                
        line_2 = line_2[:-2]
        line_2 += ' ]'
        if len(new_m) - 1 == i:
            line_2 += ']'
        if frac_exists:
            line_1 = line_1[:-2]
            line_3 = line_3[:-2]
            final += '\n'.join([line_1, line_2, line_3])
        else:
            final += line_2
        final += '\n'
    final = final[:-1]
    return final


if __name__ == "__main__":
    print()