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


try:
    from PyQt5.QtWidgets import QWidget, QLineEdit, QListWidget, QRadioButton, QGroupBox, QTabWidget
    from PyQt5.QtCore import Qt
except ImportError:
    from PyQt6.QtWidgets import QWidget, QLineEdit, QListWidget, QRadioButton, QGroupBox, QTabWidget
    from PyQt6.QtCore import Qt

from qgis.utils import iface
from qgis.core import QgsProject

class QtWidgetResetter:
    def __init__(self, tab_widget):
        self.tab_widget = tab_widget
        self.target_radio_buttons = ['ROI', 'Existing ROI', 'AUS', 'QGIS', 'JSON']
        self.roi_buttons = ['Create ROI', 'Existing ROI']
        print(f"Initialized with tab widget containing {self.tab_widget.count()} tabs")

    def reset_line_edits(self):
        count = 0
        for i in range(self.tab_widget.count()):
            current_tab = self.tab_widget.widget(i)
            for line_edit in current_tab.findChildren(QLineEdit):
                line_edit.clear()
                count += 1
        print(f"Reset {count} line edits")

    def reset_list_widgets(self):
        count = 0
        for i in range(self.tab_widget.count()):
            current_tab = self.tab_widget.widget(i)
            for list_widget in current_tab.findChildren(QListWidget):
                list_widget.clear()
                count += 1
        print(f"Reset {count} list widgets")

    def force_toggle_off_radio_button(self, radio_button):
        """Force toggle off a radio button and disconnect its signals"""
        if radio_button.isChecked():
            try:
                # Temporarily enable to allow unchecking
                was_enabled = radio_button.isEnabled()
                radio_button.setEnabled(True)
                
                # Disconnect all signals
                radio_button.blockSignals(True)
                
                # Force uncheck
                radio_button.setAutoExclusive(False)
                radio_button.setChecked(False)
                radio_button.setAutoExclusive(True)
                
                # Re-enable signals
                radio_button.blockSignals(False)
                
                # Set final enabled state based on whether it's an ROI button
                if (radio_button.text() in self.roi_buttons or 
                    radio_button.objectName() in self.roi_buttons):
                    radio_button.setEnabled(False)
                else:
                    radio_button.setEnabled(True)
                
                print(f"Toggled off and disconnected: {radio_button.text() or radio_button.objectName()}")
                return True
            except Exception as e:
                print(f"Error handling radio button: {e}")
                return False
        return False

    def reset_all_radio_buttons(self):
        """Reset all radio buttons in all tabs"""
        count = 0
        for i in range(self.tab_widget.count()):
            current_tab = self.tab_widget.widget(i)
            
            # Get all radio buttons in current tab
            radio_buttons = current_tab.findChildren(QRadioButton)
            
            for radio_button in radio_buttons:
                if self.force_toggle_off_radio_button(radio_button):
                    count += 1
        
        print(f"Reset {count} radio buttons")

    def set_final_states(self):
        """Set final enabled states for all widgets"""
        for i in range(self.tab_widget.count()):
            current_tab = self.tab_widget.widget(i)
            for widget in current_tab.findChildren(QWidget):
                # Enable all widgets by default
                widget.setEnabled(True)
                
                # Special handling for ROI buttons
                if isinstance(widget, QRadioButton):
                    if (widget.text() in self.roi_buttons or 
                        widget.objectName() in self.roi_buttons):
                        widget.setEnabled(False)

    def reset_all(self):
        """Reset all widgets in the tab widget"""
        print("\nStarting full reset...")
        self.reset_line_edits()
        self.reset_list_widgets()
        self.reset_all_radio_buttons()
        self.set_final_states()
        print("Reset completed")