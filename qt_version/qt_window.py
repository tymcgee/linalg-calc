# Tynan McGee
# 9/15/2021
# Qt version of the linear algebra calculator

import sys
from PySide6 import QtCore, QtWidgets, QtGui

# https://www.tutorialspoint.com/pyqt/pyqt_basic_widgets.htm
# https://doc.qt.io/qtforpython/PySide6/QtWidgets/index.html#module-PySide6.QtWidgets


# todo:
# include info box? or mouseover stuffs

class calcWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Linear Algebra Calculator")

        self.mainLayout = QtWidgets.QVBoxLayout(self)        
        self.maxPolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.matBoxPolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # set font family and size after creating them, otherwise it doesn't work
        self.bigfnt = QtGui.QFont()
        self.bigfnt.setFamily('Courier New')
        self.bigfnt.setPointSize(12)
        self.smallfnt = QtGui.QFont()
        self.smallfnt.setFamily('Courier New')
        self.smallfnt.setPointSize(11)


        self.mainLayout.addLayout(self.setUpperSection())
        self.mainLayout.addLayout(self.setInputSection())
        self.mainLayout.addLayout(self.setRandomSection())
        self.mainLayout.addLayout(self.setResultBox())
        self.mainLayout.addLayout(self.setBottomButtons())

        self.textBoxes = [self.v1, self.v2, self.m1, self.m2, self.resultBox]


    def setUpperSection(self):
        self.topHorzLayout = QtWidgets.QHBoxLayout()

        self.opText = QtWidgets.QLabel("Select Operation:")
        self.cb = QtWidgets.QComboBox()
        self.textFieldsBtn = QtWidgets.QPushButton("Clear Text Fields")
        self.calculateBtn = QtWidgets.QPushButton("Calculate")

        self.opText.setSizePolicy(self.maxPolicy)

        self.cb.currentIndexChanged.connect(self.dropdownEvent)
        self.textFieldsBtn.clicked.connect(self.clearText)
        self.calculateBtn.clicked.connect(self.calculate)

        self.topHorzLayout.addWidget(self.opText)
        self.topHorzLayout.addWidget(self.cb)
        self.topHorzLayout.addWidget(self.textFieldsBtn)
        self.topHorzLayout.addWidget(self.calculateBtn)
        return self.topHorzLayout

    def setInputSection(self):
        self.inputGrid = QtWidgets.QGridLayout()

        self.v1l = QtWidgets.QLabel("Vector 1:")
        self.v2l = QtWidgets.QLabel("Vector 2:")
        self.m1l = QtWidgets.QLabel("Matrix 1:")
        self.m2l = QtWidgets.QLabel("Matrix 2:")
        self.v1 = QtWidgets.QLineEdit()
        self.v2 = QtWidgets.QLineEdit()
        self.m1 = QtWidgets.QTextEdit()
        self.m2 = QtWidgets.QTextEdit()

        # "disable" the widgets instead of setting them
        # to "read-only" so that they're properly greyed out.
        # self.v1.setEnabled(False)
        # self.v2.setEnabled(False)
        self.m1.setEnabled(False)
        self.m2.setEnabled(False)
        self.m1.setSizePolicy(self.matBoxPolicy)
        self.m2.setSizePolicy(self.matBoxPolicy)
        self.m1.setTabChangesFocus(True)
        self.m2.setTabChangesFocus(True)
        self.m1.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.m2.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)

        self.v1.setFont(self.bigfnt)
        self.v2.setFont(self.bigfnt)
        self.m1.setFont(self.bigfnt)
        self.m2.setFont(self.bigfnt)

        self.vectorValidator = QtGui.QRegularExpressionValidator(r"(-?\d+(\/[1-9]\d*|\.\d+)?, *)*")
        # -? means match between 0 and 1 "-" signs
        # \d+ means any digit between 1 and unlimited times
        # (\/[1-9]\d*|\.\d+)? means optionally include a denominator or a decimal section
        # ,? * means optionally include a comma and include between 0 and infinite spaces
        self.matrixValidator = QtGui.QRegularExpressionValidator(r"(-?\d+(\/[1-9]\d*|\.\d+)?(, *| *\n))+")
        # same idea with validating the fraction
        # (,(?! *\n) *| *\n) means
        # EITHER: match a comma (not followed by a newline)
        # OR: match any number of spaces and then a newline
        self.v1.setValidator(self.vectorValidator)
        self.v2.setValidator(self.vectorValidator)
        self.m1.textChanged.connect(self.validateBoxes)
        self.m2.textChanged.connect(self.validateBoxes)

        self.inputGrid.addWidget(self.v1l, 0, 0)
        self.inputGrid.addWidget(self.v2l, 0, 1)
        self.inputGrid.addWidget(self.m1l, 2, 0)
        self.inputGrid.addWidget(self.m2l, 2, 1)
        self.inputGrid.addWidget(self.v1, 1, 0)
        self.inputGrid.addWidget(self.v2, 1, 1)
        self.inputGrid.addWidget(self.m1, 3, 0)
        self.inputGrid.addWidget(self.m2, 3, 1)
        return self.inputGrid

    def setRandomSection(self):
        self.randomGrid = QtWidgets.QGridLayout()
        self.randSettingsGrid = QtWidgets.QGridLayout()

        self.randVecBtn = QtWidgets.QPushButton("Create Random m x 1 Vector")
        self.randMatBtn = QtWidgets.QPushButton("Create Random m x n Matrix")
        self.nLab = QtWidgets.QLabel("n =")
        self.mLab = QtWidgets.QLabel("m =")
        self.nSpin = QtWidgets.QSpinBox()
        self.mSpin = QtWidgets.QSpinBox()
        self.maxRandLabel = QtWidgets.QLabel("Max Random Num:")
        self.maxRand = QtWidgets.QSpinBox()
        self.minRand = QtWidgets.QSpinBox()
        self.minRandLabel = QtWidgets.QLabel("Min Random Num:")
        self.useFractions = QtWidgets.QCheckBox("Use Fractions?")

        self.nSpin.setRange(1, 99)
        self.nSpin.setValue(3)
        self.mSpin.setRange(1, 99)
        self.mSpin.setValue(3)
        self.maxRand.setValue(10)
        self.maxRand.setMinimum(1)
        self.minRand.setValue(0)
        self.minRand.setMinimum(0)
        self.useFractions.setChecked(True)
        self.maxRand.valueChanged.connect(self.maxRandValueChanged)
        self.minRand.valueChanged.connect(self.minRandValueChanged)
        self.randVecBtn.clicked.connect(self.randomVec)
        self.randMatBtn.clicked.connect(self.randomMat)

        self.nSpin.setSizePolicy(self.maxPolicy)
        self.mSpin.setSizePolicy(self.maxPolicy)
        self.nLab.setSizePolicy(self.maxPolicy)
        self.mLab.setSizePolicy(self.maxPolicy)
        self.maxRandLabel.setSizePolicy(self.maxPolicy)
        self.minRandLabel.setSizePolicy(self.maxPolicy)
        self.maxRand.setSizePolicy(self.maxPolicy)
        self.minRand.setSizePolicy(self.maxPolicy)

        self.randSettingsGrid.addWidget(self.maxRandLabel, 0, 0)
        self.randSettingsGrid.addWidget(self.maxRand, 0, 1)
        self.randSettingsGrid.addWidget(self.minRandLabel, 1, 0)
        self.randSettingsGrid.addWidget(self.minRand, 1, 1)
        self.randSettingsGrid.addWidget(self.useFractions, 2, 0, 2, 1)
        
        self.randomGrid.addWidget(self.randVecBtn, 0, 0)
        self.randomGrid.addWidget(self.randMatBtn, 1, 0)
        self.randomGrid.addWidget(self.nLab, 0, 1)
        self.randomGrid.addWidget(self.mLab, 1, 1)
        self.randomGrid.addWidget(self.nSpin, 0, 2)
        self.randomGrid.addWidget(self.mSpin, 1, 2)
        self.randomGrid.addLayout(self.randSettingsGrid, 0, 3, 2, 1)
        return self.randomGrid

    def setResultBox(self):
        self.resultLayout = QtWidgets.QVBoxLayout()
        self.resultLabel = QtWidgets.QLabel("------------- RESULT: -------------", alignment=QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.resultBox = QtWidgets.QTextEdit()

        self.resultBox.setReadOnly(True)
        self.resultBox.setFont(self.smallfnt)

        self.resultLayout.addWidget(self.resultLabel)
        self.resultLayout.addWidget(self.resultBox)
        return self.resultLayout

    def setBottomButtons(self):
        self.lowerHorzLayout = QtWidgets.QHBoxLayout()
        self.copyBtn = QtWidgets.QPushButton("Copy Result")
        self.toFractionBtn = QtWidgets.QPushButton("Convert to Fraction (approx)")
        self.toDecBtn = QtWidgets.QPushButton("Convert to Decimal")

        self.copyBtn.clicked.connect(self.copyResult)
        self.toFractionBtn.clicked.connect(self.toFraction)
        self.toDecBtn.clicked.connect(self.toDecimal)

        self.lowerHorzLayout.addWidget(self.copyBtn)
        self.lowerHorzLayout.addWidget(self.toFractionBtn)
        self.lowerHorzLayout.addWidget(self.toDecBtn)
        return self.lowerHorzLayout

    
    def validateBoxes(self):
        boxes = [self.m1, self.m2]
        for b in boxes:
            currentText = b.toPlainText()
            state = self.matrixValidator.validate(currentText, 0)
            if state[0] not in (QtGui.QValidator.State.Intermediate, QtGui.QValidator.State.Acceptable):
                b.clear()
                b.append(currentText[:-1])  # remove the text that was just put there

    def dropdownEvent(self, drop_index):
        print('dropdown changed')
        print('current selection is', self.cb.currentText(), 'at index', drop_index)
    
    def clearText(self):
        print('clear text')
    
    def calculate(self):
        print('calculate')

    def randomVec(self):
        print('random vec')

    def randomMat(self):
        print('random mat')

    def copyResult(self):
        print('copy')

    def toFraction(self):
        print('convert to fraction')
    
    def toDecimal(self):
        print('convert to decimal')

    def maxRandValueChanged(self, v):
        print('max random value changed')

    def minRandValueChanged(self, v):
        print('min random value changed')

if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    win = calcWindow()
    win.show()

    sys.exit(app.exec())