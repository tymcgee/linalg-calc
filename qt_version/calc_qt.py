# Tynan McGee
# 9/15/2021
# Qt version of the linear algebra calculator

import random
import sys

import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets

import qt_window
from calc_funcs_qt import *
from fraction_qt import *
from input_funcs_qt import *
from matrix_format_qt import *


class Func:
    def __init__(self, func, active_boxes, text, info):
        self.func = func  # this is a function
        self.active_boxes = active_boxes  # this is a list of 4 bools
        self.text = text  # this is a string
        self.info = info  # this is a string


class MainWindow(qt_window.calcWindow):
    def __init__(self):
        super().__init__()
        self.currentResult = Fraction()
        self.clip = QtGui.QClipboard()
        self.errorDialog = QtWidgets.QMessageBox()
        self.errorDialog.setIcon(QtWidgets.QMessageBox.Critical)
        self.errorDialog.setText("Something went wrong:")
        self.errorDialog.setWindowTitle("Error")
        self.FUNCS = {
            'Add':                     Func(vec_add,        [1, 1, 0, 0],  'v1 + v2 =\n',                             'Adds v1 and v2 together.'),
            'Subtract':                Func(vec_sub,        [1, 1, 0, 0],  'v1 - v2 =\n',                             'Subtracts v2 from v1.'),
            'Matrix-Vector Multiply':  Func(vec_mat_mult,   [1, 0, 1, 0],  'M1 * v1 =\n',                             'Multiplies M1 by v1.'),
            'Inner Product':           Func(inner_product,  [1, 1, 0, 0],  '<v1, v2> =\n',                            'Inner product (aka dot product) of v1 and v2 (multiplies components and adds them). For example, if v1 = [a, b] and v2 = [c, d] the inner product is ac + bd.'),
            'Determinant':             Func(det,            [0, 0, 1, 0],  'Det(M1) =\n',                             'Takes the determinant of M1. Only works if M1 is square. Uses Gaussian Elimination, so it is pretty fast.'),
            'Determinant (slow)':      Func(det_slow,       [0, 0, 1, 0],  'Det(M1) =\n',                             'Takes the determinant of M1. Only works if M1 is square. Uses the Leibniz formula, which works incredibly slow for large matrices (if a matrix is n x n, the computer must perform more than n factorial operations).'),
            'REF':                     Func(ref,            [0, 0, 1, 0],  'REF(M1) =\n',                             'Puts M1 into row echelon form (upper triangular). If there is a 0 on one of the diagonals, the matrix is not invertible.'),
            'RREF':                    Func(rref,           [0, 0, 1, 0],  'RREF(M1) =\n',                            'Puts M1 into reduced row echelon form (1 on the diagonals where possible). If there is a 0 on one of the diagonals, the matrix is not invertible.'),
            'Solve Ax = b':            Func(solve,          [1, 0, 1, 0],  'x = \n',                                  'Uses Gaussian Elimination (via row reduction) to solve Ax = b, where A is M1 and b is v1. Does not work if the matrix is not invertible.'),
            'Inverse':                 Func(inverse,        [0, 0, 1, 0],  'M1^(-1) =\n',                             'Finds the inverse of M1 using Gaussian Elimination (via row reduction). If det(M1) = 0, there is no inverse.'),
            'Matrix Multiply':         Func(mat_mult,       [0, 0, 1, 1],  'M1 * M2 =\n',                             'Multiplies M1 by M2 (on the right).'),
            'Project (vec on vec)':    Func(project,        [1, 1, 0, 0],  'Proj_{v2}(v1) =\n',                       'Projects v1 onto v2.'),
            'Project (vec on mat)':    Func(project,        [1, 0, 1, 0],  'Proj_{M1}(v1) =\n',                       'Projects v1 onto the subspace spanned by the columns of M1.'),
            'M^T * M':                 Func(aTa,            [0, 0, 1, 0],  'M^T * M =\n',                             'Multiplies the transpose of M1 by M1 (on the right). The resulting matrix is both square and symmetric.'),
            'GS Algorithm':            Func(gs,             [0, 0, 1, 0],  'orthogonal matrix\n(spans col(M1))\n',    'The Gram Schmidt Algorithm is an algorithm which produces an orthogonal matrix which spans the same column space as the given matrix. It steals the first column of the original matrix, then uses a projection of the subsequent columns onto the current result to create orthogonal columns.'),
            'QR-Factorization':        Func(qr,             [0, 0, 1, 0],  'Q,R =\n',                                 'Factorizes M1 into Q and R, where Q is orthogonal and R is upper-triangular.'),
            'Normalize Vector':        Func(normalize_vec,  [1, 0, 0, 0],  'norm(v1) =\n',                            'Normalizes v1.'),
            'Normalize Matrix':        Func(normalize_mat,  [0, 0, 1, 0],  'norm(M1) =\n',                            'Normalizes the columns of M1.'),
            'Eigen Matrix':            Func(eigen_matrix,   [0, 0, 1, 0],  'eigenvalues on diagonal:\n',              'Uses the QR-algorithm to create a (hopefully) upper-triangular matrix with the eigenvalues of M1 on the diagonal. May not work all of the time depending on M1, does not work if M1 has complex eigenvalues.')
        }
        self.cb.addItems([*[key for key in self.FUNCS]])

    def dropdownEvent(self, drop_index):
        active = self.FUNCS[self.cb.currentText()].active_boxes
        boxes = [self.v1, self.v2, self.m1, self.m2]
        for i in range(4):
            boxes[i].setEnabled(active[i])
        self.active_boxes = active

    def clearText(self):
        for t in self.textBoxes:
            t.clear()

    def calculate(self):
        # things to check:
        # provided vectors are vectors (maybe not necessary with validators)
        # provided matrices are matrices
        # vectors operated on each other have the same length
        # is matrix invertible for: inverse, solve
        # is matrix square for determinant and eigen matrix
        # projecting on to a matrix, vec must have same # of rows as matrix (since we do inner product with cols of matrix)
        # matvec multiplication, vec must have same # of rows as matrix has columns
        # matrix multiplication, M1 has same # of cols as M2 has rows.
        current_op = self.cb.currentText()
        current_func = self.FUNCS[current_op]
        f = current_func.func
        active_items = current_func.active_boxes

        v1 = return_vector(self.v1)
        v2 = return_vector(self.v2)
        m1 = return_matrix(self.m1)
        m2 = return_matrix(self.m2)

        # only check active boxes for errors
        errored = False
        error_msg = ""
        for i in zip((v1, v2, m1, m2), self.active_boxes):
            # i is a tuple that looks like (v1, True)
            # if no error, v1 should be a list of fractions
            # if error, it should be a string
            if i[1] and isinstance(i[0], str):
                errored = True
                self.errorDialog.setInformativeText(i[0])
                self.errorDialog.exec()

        if active_items == [1, 1, 0, 0]:
            if not isinstance((a := valid_vecs(v1, v2)), str):
                result = f(v1, v2)
            else:
                errored = True
                error_msg += a

        elif active_items == [1, 0, 1, 0]:
            if not isinstance((a := matvec_valid(v1, m1, current_op)), str):
                result = f(v1, m1)
            else:
                errored = True
                error_msg += a

        elif active_items == [1, 0, 0, 0]:
            if is_vector(v1):
                result = f(v1)
            else:
                errored = True
                error_msg += "The input (v1) is not a vector."

        elif active_items == [0, 0, 1, 0]:
            if not isinstance((a := mat_valid(m1, current_op)), str):
                if f == qr:
                    result_1, result_2 = f(m1)
                    msg = current_func.text
                    msg += format_answer(result_1) + '\n'
                    msg += format_answer(result_2)
                    self.resultBox.clear()
                    self.resultBox.insertPlainText(msg)
                    return
                result = f(m1)
            else:
                errored = True
                error_msg += a

        elif active_items == [0, 0, 1, 1]:
            if not isinstance((a := valid_mats(m1, m2)), str):
                result = f(m1, m2)
            else:
                errored = True
                error_msg += a

        else:
            # error
            print('something went wrong.')
            return

        if errored:
            self.errorDialog.setInformativeText(error_msg)
            self.errorDialog.exec()
            return

        msg = current_func.text
        msg += format_answer(result)
        self.resultBox.clear()
        self.resultBox.insertPlainText(msg)
        self.currentResult = result

    def randomVec(self):
        m = self.mSpin.value()
        r_max = self.maxRand.value()
        r_min = self.minRand.value()

        final_string = ''
        for row in range(m):
            if self.useFractions.isChecked():
                final_string += str(Fraction(random.randint(r_min, r_max),
                                    random.randint(max(1, r_min), r_max)))
            else:
                final_string += str(random.randint(r_min, r_max))
            final_string += ', '
        final_string = final_string[:-2]

        self.v1.clear()
        self.v1.setText(final_string)

    def randomMat(self):
        m = self.mSpin.value()
        n = self.nSpin.value()
        r_max = self.maxRand.value()
        r_min = self.minRand.value()

        final_string = ''
        for row in range(m):
            for col in range(n):
                if self.useFractions.isChecked():
                    final_string += str(Fraction(random.randint(r_min, r_max),
                                        random.randint(max(1, r_min), r_max)))
                else:
                    final_string += str(random.randint(r_min, r_max))
                final_string += ', '
            final_string = final_string[:-2]
            final_string += '\n'
        final_string = final_string[:-1]

        self.m1.clear()
        self.m1.setText(final_string)

    def copyResult(self):
        if self.FUNCS[self.cb.currentText()].func == qr:
            # not supported
            self.errorDialog.setInformativeText(
                "You cannot copy the result when it contains more than one matrix or vector.")
            self.errorDialog.exec()
            return
        txt = get_csv(self.currentResult)
        self.clip.setText(txt)

    def toFraction(self):
        if self.FUNCS[self.cb.currentText()].func == qr:
            self.errorDialog.setInformativeText(
                "You cannot do that to a result with more than one matrix or vector.")
            self.errorDialog.exec()
            return
        if isinstance(self.currentResult, (list, np.ndarray)):
            if isinstance(self.currentResult[0], (list, np.ndarray)):
                # current result is a matrix
                row_size = len(self.currentResult)
                col_size = len(self.currentResult[0])
                result = [[dec_to_frac_approx(self.currentResult[i][j]) for j in range(
                    col_size)] for i in range(row_size)]
            else:
                # current result is a vector
                size = len(self.currentResult)
                result = [dec_to_frac_approx(
                    self.currentResult[i]) for i in range(size)]
        else:
            # current result is a scalar
            result = dec_to_frac_approx(self.currentResult)
        self.currentResult = result
        msg = self.FUNCS[self.cb.currentText()].text
        self.resultBox.clear()
        self.resultBox.insertPlainText(msg + format_answer(result))

    def toDecimal(self):
        if self.FUNCS[self.cb.currentText()].func == qr:
            self.errorDialog.setInformativeText(
                "You cannot do that to a result with more than one matrix or vector.")
            self.errorDialog.exec()
            return
        if isinstance(self.currentResult, (list, np.ndarray)):
            if isinstance(self.currentResult[0], (list, np.ndarray)):
                # current result is a matrix
                row_size = len(self.currentResult)
                col_size = len(self.currentResult[0])
                result = [[Fraction(float(self.currentResult[i][j]))
                           for j in range(col_size)] for i in range(row_size)]
            else:
                # current result is a vector
                size = len(self.currentResult)
                result = [Fraction(float(self.currentResult[i]))
                          for i in range(size)]
        else:
            # current result is a scalar
            result = Fraction(float(self.currentResult))
        self.currentResult = result
        msg = self.FUNCS[self.cb.currentText()].text
        self.resultBox.clear()
        self.resultBox.insertPlainText(msg + format_answer(result))

    def maxRandValueChanged(self, v):
        if self.maxRand.value() < self.minRand.value():
            self.maxRand.setValue(self.minRand.value())

    def minRandValueChanged(self, v):
        if self.maxRand.value() < self.minRand.value():
            self.minRand.setValue(self.maxRand.value())


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    win = MainWindow()
    win.show()

    sys.exit(app.exec())
