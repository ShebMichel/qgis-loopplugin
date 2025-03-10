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

from typing import Dict, List
from PyQt5.QtWidgets import QComboBox, QLineEdit

class FStateSaver:
    """
    A class to save and restore the state of Qt widgets, specifically handling
    QComboBoxes (both standard and editable) and QLineEdits.
    """
    def __init__(
        self,
        fault_combo_boxes      : List[QComboBox],
        fault_param_boxes      : List[QComboBox],  # These are editable QComboBoxes
        fault_ftext_QLineEdit  : QLineEdit,
        fault_fdipest_QLineEdit: QLineEdit,
        fault_line_edit        : QLineEdit
    ):

        self.fault_combo_boxes       = fault_combo_boxes
        self.fault_param_boxes       = fault_param_boxes
        self.fault_ftext_QLineEdit   = fault_ftext_QLineEdit
        self.fault_fdipest_QLineEdit = fault_fdipest_QLineEdit
        self.fault_QLineEdit         = fault_line_edit


    def save_parameters(self) -> Dict:
        # Get all items from each combo box, with current item first
        fault_front_cbox = ["Default Dip", "Dip Direction", "Feature", "Dip Direction type", "Fdipest", "Point ID", "Dip Dir Convention"]
        fault_alg_keys      = ["fdip", "fdipdir", "f", "fdipdir_flag", "fdipest","o","ftype"]
        user_field_keys =["Fault dip", "Decimate","Min Length"]
        combo_all_items = {}
        for idx, box in enumerate(self.fault_combo_boxes):
            current = box.currentText()
            all_items = [box.itemText(i) for i in range(box.count())]
            # Remove current item from list if it exists
            if current in all_items:
                all_items.remove(current)
            # Add current item at the beginning
            combo_all_items[fault_front_cbox[idx]] = [current] + all_items

        state = {
            'fault_combos': dict(zip(fault_alg_keys,[box.currentText() for box in self.fault_combo_boxes])),
            'fault_params': [param_obj.currentText() if isinstance(param_obj, QComboBox) 
                             else param_obj.text() for param_obj in self.fault_param_boxes]}

        # New dictionary with values from QLineEdit
        new_data = {
            'Fault Text': self.fault_ftext_QLineEdit.text(),
            'fdipest Text': self.fault_fdipest_QLineEdit.text()
        }
        #print(f" state is {state}")
        # Merge dictionaries
        new_state = {**state['fault_combos'], **new_data}
        #print(f" new state : {new_state}")

        new_geol_param = dict(zip(user_field_keys,state['fault_params']))
        #print(f" The data for new_geol_param {new_geol_param}")
      
        full_data_dict ={"fault_head":new_state, "fault_params": new_geol_param, "fault_path":self.fault_QLineEdit.text(),"FAULT JSON": combo_all_items}
        #print(f" The full data is {full_data_dict}")
        return full_data_dict


    def clear_all(self) -> None:
        """
        Clears all widgets to their default state.
        """
        # Clear standard combo boxes
        for box in self.fault_combo_boxes:
            box.setCurrentIndex(0)

        # Clear editable combo boxes
        for box in self.fault_param_boxes:
            if box.isEditable():
                box.lineEdit().clear()
            else:
                box.setCurrentIndex(0)

        # Clear line edits
        self.fault_ftext_QLineEdit.clear()
        self.fault_fdipest_QLineEdit.clear()
 
############################
