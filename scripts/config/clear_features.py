# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Loop3DModelGenDockWidget
                                 A QGIS plugin
 This plugin preprocess map layers using map2loop and use its output for 3D modelling using LoopStructural.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2024-12-13
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Center of Exploration Targeting, UWA
        email                : michel.nzikoumamboukou@uwa.edu.au
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""


from PyQt5.QtWidgets import (
    QTabWidget, QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QRadioButton,QApplication
)

class TabWidgetFeatureResetter:
    def __init__(self, tab_widget: QTabWidget):
        """
        Initialize the TabWidgetFeatureResetter with the QTabWidget to reset features.

        :param tab_widget: The QTabWidget instance to manage.
        """
        if not isinstance(tab_widget, QTabWidget):
            raise TypeError("Provided widget must be an instance of QTabWidget")
        self.tab_widget = tab_widget


    def reset_qt_widgets(self,dialog):
    """
    Reset all Qt widgets in a QGIS dialog:
    - Clear line edits and list widgets in tab widgets
    - Uncheck all radio buttons in group boxes
    - Enable all widgets except specific ROI buttons
    
    Args:
        dialog: The main dialog containing the widgets
    """
    # Reset all line edits and list widgets in tab widgets
    for tab_widget in dialog.findChildren(QTabWidget):
        for i in range(tab_widget.count()):
            tab = tab_widget.widget(i)
            
            # Clear line edits
            for line_edit in tab.findChildren(QLineEdit):
                line_edit.clear()
            
            # Clear list widgets
            for list_widget in tab.findChildren(QListWidget):
                list_widget.clear()
    
    # Uncheck radio buttons in group boxes
    for group_box in dialog.findChildren(QGroupBox):
        for radio_button in group_box.findChildren(QRadioButton):
            if radio_button.isChecked():
                radio_button.setChecked(False)
    
    # Enable all widgets
    for widget in dialog.findChildren(QWidget):
        widget.setEnabled(True)
    
    # Disable specific ROI buttons
    roi_widgets = ['Create ROI', 'Existing ROI']
    for widget in dialog.findChildren(QWidget):
        if widget.objectName() in roi_widgets:
            widget.setEnabled(False)