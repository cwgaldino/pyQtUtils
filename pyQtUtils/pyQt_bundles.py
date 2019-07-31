#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Easily create bundles of pyqt widgets."""

from pyqtgraph.Qt import QtCore
from pyqtgraph.Qt import QtGui
from functools import partial
from .pyQt_FSlider import FSlider, FSlider_win, setFSlider


def FSliderBundle(self, label, min, max, step, value, dict2connect=None, extra_text=None):
    """Create FSlider with an label, lineEdit, and a set button.

    Value can be edit from the slider and the lineEdit.

    Set button goes first, then the FSlider, the label, and finally the
    lineEdit.

    .. note:: Upon a change in the FSlider value (or lineEdit) the new value is
    updated in dict2connect[label]['value']. Thefore your your dictionary must
    have a key exactly as 'label' and dict2connect[label] is expected the have
    a key: 'value', where the value is stored.

    .. warning:: FSliderBundle connects a change in FSlider value (or lineEdit)
    to your "app's update method". Therefore if FSlider value is changed it
    tries to run app.update(). If app.update() does not exists nothing heppens.

    .. note:: lineEdit does not respect min and max limits of the slider.

    Args:
        label (str): text label.
        min (int/float): minimum value of the slider.
        max (int/float): maximum value of the slider.
        step (int/float): step change of the slider.
        value (int/float): initial value.
        extra_text (str): extra text to be writen in front of label.
        dict2connect (dict): dictionary to update value see note above.

    Returns:
        dictionary of pyqt5 objects: keys are 'btn', 'slider', 'txt', and
        'lineEdit'. Each of then points to the respective pyqt5 object.
    """
    slider = dict()

    # button
    slider['btn'] = QtGui.QPushButton('Set', self)
    slider['btn'].setFixedWidth(40)

    # slider
    slider['slider'] = FSlider(QtCore.Qt.Horizontal, self)
    setFSlider(slider['slider'], value, min, max, step)

    # label
    if extra_text is None:
        slider['txt'] = QtGui.QLabel(label, self)
    else:
        slider['txt'] = QtGui.QLabel(label+' '+extra_text, self)
    slider['txt'].adjustSize()
    # slider['txt'].setContentsMargins(0, 0, 0, 0)

    # editbox
    slider['lineEdit'] = QtGui.QLineEdit(self)
    slider['lineEdit'].setFixedWidth(100)
    slider['lineEdit'].setContentsMargins(20, 0, 20, 0)
    slider['lineEdit'].setText('{0}'.format(value))

    # Connect
    slider['btn'].clicked.connect(partial(openFSlider_win, self, slider['slider']))
    slider['lineEdit'].editingFinished.connect(partial(update_slider_from_text, self, label, slider['lineEdit'], slider['slider'], dict2connect=dict2connect))
    slider['slider'].valueChanged.connect(partial(update_lineEdit_from_slider, self, label, slider['slider'], slider['lineEdit'], dict2connect=dict2connect))

    return slider


def openFSlider_win(self, FSlider):
    """Open window to change FSlider parameters."""
    self.dialog = FSlider_win(FSlider)
    self.dialog.show()


def update_slider_from_text(self, label, lineEdit, slider, dict2connect=None):
    """Update FSlider value based on change of lineEdit."""
    value = float(lineEdit.text())
    if dict2connect is not None:
        try:
            dict2connect[label]['value'] = value
        except KeyError:
            print('ERROR: Cannot assign value to variable.')
            print('Maybe {0} is not in the variables dictionary (dict2connect)'.format(label))
    slider.blockSignals(True)
    slider.setVal(value)
    slider.blockSignals(False)
    try:
        self.update()
    except Exception as e:
        print('====pyQt_bundles.update_slider_from_text warning====')
        print('WARNING: Cannot run self.update()')
        print(e)


def update_lineEdit_from_slider(self, label, slider, lineEdit, dict2connect=None):
    """Update lineEdit based on change of FSlider."""
    value = round(slider.val(), 9)
    if dict2connect is not None:
        try:
            dict2connect[label]['value'] = value
        except KeyError:
            print('ERROR: Cannot assign value to variable.')
            print('Maybe {0} is not in the variables dictionary (dict2connect)'.format(label))
    lineEdit.blockSignals(True)
    lineEdit.setText('{0}'.format(value))
    lineEdit.setCursorPosition(0)
    lineEdit.blockSignals(False)
    try:
        self.update()
    except Exception as e:
        print('====pyQt_bundles.update_lineEdit_from_slider warning====')
        print('WARNING: Cannot run self.update()')
        print(e)


def comboBoxBundle(self, label, value, valueList, dict2connect=None, extra_text=None):
    """Create QtGui.QComboBox with an label, lineEdit, and a delete button.

    Value can be edit from the QComboBox and the lineEdit.

    Delete button deletes item from QComboBox.

    .. note:: Upon a change in the QComboBox value (or lineEdit) the new value
    is updated in dict2connect[label]['value']. Thefore your your dictionary
    must have a key exactly as 'label' and dict2connect[label] is expected the
    have a key: 'value', where the value is stored.

    .. note:: Also if you insert a string in lineEdit and this string is not
    one of the options in QComboBox, then the comboBox list is updated and the
    new value is added. Moreover, the list of values is updated in
    dict2connect[label]['valueList']. Therefore  your dictionary must have a
    key exactly as 'label' and dict2connect[label] is expected the have a key:
    'valueList', where the value is stored.

    .. warning:: comboBoxBundle connects a change in QComboBox value (or
    lineEdit) to your "app's update method". Thefore if QComboBox value is
    changed it tries to run app.update(). If app.update() does not exists
    nothing heppens.

    Args:
        label (str): text label.
        value (string): initial value.
        valueList (list): list of strings.
        extra_text (str): extra text to be writen in front of label.
        dict2connect (dict): dictionary to update value see note above.

    Returns:
        dictionary of pyqt5 objects: keys are 'btn', 'comboBox', 'txt', and
        'lineEdit'. Each of then points to the respective pyqt5 object.
    """
    comboBox = dict()

    # button
    comboBox['btn'] = QtGui.QPushButton('Del', self)
    comboBox['btn'].setFixedWidth(40)

    # comboBox
    comboBox['comboBox'] = QtGui.QComboBox(self)
    if value not in valueList:
        valueList.append(value)
    idx = valueList.index(value)
    comboBox['comboBox'].addItems(valueList)
    # index = comboBox['comboBox'].findText(value, QtCore.Qt.MatchFixedString)
    comboBox['comboBox'].setCurrentIndex(idx)

    # text
    if extra_text is None:
        comboBox['txt'] = QtGui.QLabel(label, self)
    else:
        comboBox['txt'] = QtGui.QLabel(label+' '+extra_text, self)
    comboBox['txt'].adjustSize()

    # lineEdit
    comboBox['lineEdit'] = QtGui.QLineEdit(self)
    comboBox['lineEdit'].setFixedWidth(100)
    comboBox['lineEdit'].setContentsMargins(20, 0, 20, 0)
    comboBox['lineEdit'].setText('{0}'.format(value))

    # Connect
    comboBox['btn'].clicked.connect(partial(delComboBoxItem, self, label, comboBox['comboBox'], dict2connect=dict2connect))
    comboBox['lineEdit'].editingFinished.connect(partial(update_comboBox_from_lineEdit, self, label, comboBox['comboBox'], comboBox['lineEdit'], dict2connect=dict2connect))
    comboBox['comboBox'].currentIndexChanged.connect(partial(update_lineEdit_from_comboBox, self, label, comboBox['comboBox'], comboBox['lineEdit'], dict2connect=dict2connect))

    return comboBox


def update_comboBox_from_lineEdit(self, label, comboBox, lineEdit, dict2connect=None):
    """Update comboBox based on change in lineEdit."""
    value = lineEdit.text()
    if dict2connect is not None:
        try:
            dict2connect[label]['value'] = value
        except KeyError:
            print('ERROR: Cannot assign value to variable.')
            print('Maybe {0} is not in the variables dictionary (dict2connect)'.format(label))

    comboBox.blockSignals(True)
    index = comboBox.findText(value, QtCore.Qt.MatchFixedString)
    # if text from lineEdit is not on ValueList, update valueList
    if index == -1:
        comboBox.addItem(value)
        index = comboBox.count()-1
    if dict2connect is not None:
        try:
            dict2connect[label]['valueList'].append(value)
        except KeyError:
            print('ERROR: Cannot append {0} to dict2connect[{1}][\'valueList\']'.format(value, label))
            print('Maybe {0} is not in the variables dictionary (dict2connect)'.format(label))
    comboBox.setCurrentIndex(index)
    comboBox.blockSignals(False)
    try:
        self.update()
    except Exception as e:
        print('====pyQt_bundles.update_comboBox_from_lineEdit warning====')
        print('WARNING: Cannot run self.update()')
        print(e)


def update_lineEdit_from_comboBox(self, label, comboBox, lineEdit, dict2connect=None):
    """Update lineEdit based on change in comboBox."""
    value = comboBox.currentText()
    if dict2connect is not None:
        try:
            dict2connect[label]['value'] = value
        except KeyError:
            print('ERROR: Cannot assign value to variable.')
            print('Maybe {0} is not in the variables dictionary (dict2connect)'.format(label))
    lineEdit.blockSignals(True)
    lineEdit.setText('{0}'.format(value))
    lineEdit.setCursorPosition(0)
    lineEdit.blockSignals(False)
    try:
        self.update()
    except Exception as e:
        print('====pyQt_bundles.update_lineEdit_from_comboBox warning====')
        print('WARNING: Cannot run self.update()')
        print(e)


def delComboBoxItem(self, label, comboBox, dict2connect=None):
    """Delete item from combobox."""
    value = comboBox.currentText()
    valueList = [comboBox.itemText(i) for i in range(comboBox.count())]
    index = comboBox.findText(value, QtCore.Qt.MatchFixedString)
    if index != -1:
        del valueList[index]
        comboBox.clear()
        comboBox.addItems(valueList)
    comboBox.setCurrentIndex(0)
    if dict2connect is not None:
        try:
            dict2connect[label]['valueList'] = valueList
        except KeyError:
            print('ERROR: Cannot assign valueList to variable.')
            print('Maybe {0} is not in the variables dictionary (dict2connect)'.format(label))
