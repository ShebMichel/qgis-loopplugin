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


import json
import os
from PyQt5.QtWidgets import QComboBox,QLineEdit
class JSONDataHandler:
    def __init__(self, file_path):
        """
        Initializes the JSONDataHandler with the given file path.
        
        :param file_path: Path to the JSON file
        """
        self.file_path = file_path
        self.folder_path = os.path.dirname(file_path)
        # Ensure the folder exists
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
            print(f"Folder created at: {self.folder_path}")
    
    def read_data(self):
        """
        Reads data from the JSON file. If the file doesn't exist, returns an empty dictionary.
        
        :return: Dictionary containing data from the JSON file
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                try:
                    data = json.load(file)
                    return data
                except json.JSONDecodeError:
                    print("Error reading the JSON file.")
                    return {}
        else:
            print("File not found, returning empty dictionary.")
            return {}

    def save_data(self, data):
        """
        Saves the given data to the JSON file. If the file exists, it will overwrite it.
        
        :param data: Dictionary to save to the file
        """
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)
            #print("Data saved successfully.")

    def add_data(self, new_data):
        """
        Adds new data to the existing JSON file. If the file does not exist, it will create it.
        
        :param new_data: Dictionary containing the data to add to the file
        """
        existing_data = self.read_data()
        
        # Add new data to the existing data (if not empty)
        existing_data.update(new_data)
        
        # Save the updated data back to the file
        self.save_data(existing_data)



