#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pyQt_utils test window."""

import sys
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from pyQtUtils.pyQt_bundles import FSliderBundle, comboBoxBundle


class Window(QtGui.QMainWindow):
    """Temporary docstring."""

    def __init__(self, parent=None):
        super().__init__()

        self.setGeometry(600, 600, 400, 150)
        self.setWindowTitle('test app')

        self.slider = FSliderBundle(self, 'var1', 0, 10, 0.3, 5, dict2connect=None, extra_text='(arb. units)')
        self.slider['txt'].move(0, 5)
        self.slider['btn'].move(130, 0)
        self.slider['slider'].move(180, 0)
        self.slider['lineEdit'].move(280, 0)

        self.comboBox = comboBoxBundle(self, 'var2', 'option1', ['option3', 'option1', 'option2'], dict2connect=None, extra_text='(extra)')
        self.comboBox['txt'].move(0, 45)
        self.comboBox['txt'].setAlignment(QtCore.Qt.AlignLeft)
        self.comboBox['txt'].setStyleSheet("QLabel {background-color: red;}")
        self.comboBox['btn'].move(130, 40)
        self.comboBox['comboBox'].move(180, 40)
        self.comboBox['lineEdit'].move(280, 40)

        self.show()


    def update(self):
        print('something changed')

if __name__ == '__main__':
    print('main')
    root = QtWidgets.QApplication(sys.argv)
    app = Window()
    sys.exit(root.exec_())
