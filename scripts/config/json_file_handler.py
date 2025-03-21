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


from qgis.PyQt.QtWidgets import QFileDialog
import os

class JSONDataPathHandler:
    def __init__(self):
        self.json_data_path = None
        #self.geology_log    = geology_log

    def ensure_json_data_path(self):
        """
        Check if the JSON data path exists, else prompt the user to select a valid file.
        """
        if not self.json_data_path or not os.path.exists(self.json_data_path):
            #self.geology_log.addItem("JSON data path does not exist or is not set. Please select the file.")
            print("JSON data path does not exist or is not set. Please select the file.")
            
            # Open a file dialog to select a JSON file
            file_dialog = QFileDialog()
            file_dialog.setWindowTitle("Select JSON Data File")
            file_dialog.setNameFilter("JSON Files (*.json)")
            file_dialog.setFileMode(QFileDialog.ExistingFile)

            if file_dialog.exec_():
                selected_file = file_dialog.selectedFiles()
                if selected_file:
                    self.json_data_path = selected_file[0]
                    #self.geology_log.addItem(f"Selected JSON data path: {self.json_data_path}")
                    print(f"Selected JSON data path: {self.json_data_path}")
                else:
                    #self.geology_log.addItem("No file selected.")
                    print("No file selected.")
            else:
                #self.geology_log.addItem("File dialog was canceled.")
                print("File dialog was canceled.")
        else:
            #self.geology_log.addItem(f"JSON data path exists: {self.json_data_path}")
            
            print(f"JSON data path exists: {self.json_data_path}")
        return self.json_data_path

# Usage example
# handler = JSONDataPathHandler()
# self.json_data_path=handler.ensure_json_data_path()
