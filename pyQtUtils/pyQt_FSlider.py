#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QtWidgets.QSlider object that allows float steps."""

import os
from pathlib import Path
from decimal import Decimal

from pyqtgraph.Qt import QtGui
from pyqtgraph.Qt import uic, QtWidgets


class FSlider(QtWidgets.QSlider):
    """Create QtWidgets.QSlider object that allows float steps.

    Attributes: are the same as for QtWidgets.QSlider. Step size is initially
    set as 1. Use FSlider.setStep() to set step size (step size cannot be set
    on creation).

    .. warning:: Do not use regular QtWidgets.QSlider for minimum,
        maximum, and value. Instead use:
        ====                    ====
        Method                  Description
        ======                  =====
        FSlider.setMin()        Set slider minimum value.
        FSlider.setMax()        Set slider maximum value.
        FSlider.setStep()       Set slider step value.
        FSlider.setVal()        Set slider value.
        FSlider.min()           Return slider minimum value.
        FSlider.max()           Return slider maximum value.
        FSlider.step()          Return slider step value.
        FSlider.step()          Return slider value.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._step = 1
        self.val_remainder = 0
        self.min_remainder = 0
        self.max_remainder = 0

    def setStep(self, newStep):
        """Set slider step value."""
        # self.val_remainder = 0
        max = self.max()
        min = self.min()
        oldValue = self.val()
        self._step = newStep
        self.setMax(max)
        self.setMin(min)
        # print('oldvalue---')
        # print(oldValue)
        self.setVal(oldValue)

    def step(self):
        """Return step value."""
        return self._step

    def setMin(self, minValue):
        """Set slider minimum value."""
        self.min_remainder = float(Decimal(str(minValue)) % Decimal(str(self.step())))
        super().setMinimum(int(minValue/self.step()))

    def setMax(self, maxValue):
        """Set slider maximum value."""
        self.max_remainder = float(Decimal(str(maxValue)) % Decimal(str(self.step())))
        super().setMaximum(int(maxValue/self.step()))

    def min(self):
        """Return slider minimum value."""
        return float(super().minimum())*self.step() + self.min_remainder

    def max(self):
        """Return slider maximum value."""
        return float(super().maximum())*self.step() + self.max_remainder

    def val(self):
        """Return slider value."""
        val = float(super().value())*self.step() + self.val_remainder
        print('val==============')
        print(super().value())
        print(self.val_remainder)
        print(self.step())
        if val < self.min():
            val = self.min()
        elif val > self.max():
            val = self.max()
        # print('val function')
        # print(super().value())
        return val

    def setVal(self, val):
        """Set slider value."""
        if val < self.min():
            val = self.min()
        elif val > self.max():
            val = self.max()
        self.val_remainder = float(Decimal(str(val)) % Decimal(str(self.step())))
        # print('setVal==============')
        # print(val)
        # print(self.val_remainder)
        # print(int(val/self.step()))
        return super().setValue(int(val/self.step()))
# float(Decimal(5) % Decimal(0.4))
# 5/0.3
# 5/0.4
# 0.4*12
# 16*0.3

class FSlider_win(QtGui.QWidget):
    """Opens a dedicated window to edit the parameters of a FSlider.

    More than often, I like to edit the parameters of a slider when the app is
    already running. This opens a dedicated window from within the app that
    allows you to change the slider parameters.

    Args:
        slider (FSlider): The slider instance.
    """

    def __init__(self, FSlider, parent=None):
        """Init method.

        Args:
            slider (QtWidgets.QSlider): The slider instance.
        """
        super().__init__()

        folder = Path(os.path.dirname(os.path.abspath(__file__)))
        uic.loadUi(folder / 'FSlider.ui', self)
        self.FSlider = FSlider

        self.set_text()  # data on text boxes

        self.btn1.clicked.connect(self.update)
        self.btn2.clicked.connect(self.close_win)

    def update(self):
        """Update FSlider."""
        self.FSlider.setStep(float(self.lineEdit_2.text()))
        self.FSlider.setMin(float(self.lineEdit.text()))
        self.FSlider.setMax(float(self.lineEdit_1.text()))
        self.set_text()
        self.close()

    def set_text(self):
        """Set text on FSlider_win editbox."""
        self.lineEdit.setText('{0}'.format(self.FSlider.min()))
        self.lineEdit_1.setText('{0}'.format(self.FSlider.max()))
        self.lineEdit_2.setText(str(self.FSlider.step()))

    def close_win(self):
        """Close window."""
        self.close()


def setFSlider(slider, value, min, max, step):
    """Set FSlider parameters with one line of code."""
    slider.setStep(step)
    slider.setMin(min)
    slider.setMax(max)
    slider.setVal(value)
