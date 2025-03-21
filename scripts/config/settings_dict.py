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


class SettingsDictionary:
    """
    A class to create and manage settings dictionaries from QLineEdit values.
    Allows for flexible configuration of key-value pairs.
    """
    def __init__(self):
        """Initialize an empty mapping dictionary"""
        self.mapping = {}

    def add_mapping(self, display_name: str, line_edit) -> None:
        """
        Add a new key-value mapping.
        
        Args:
            display_name (str): The key name for the dictionary
            line_edit: QLineEdit widget to extract value from
        """
        self.mapping[display_name] = line_edit

    def add_multiple_mappings(self, mapping_dict: dict) -> None:
        """
        Add multiple mappings at once.
        
        Args:
            mapping_dict (dict): Dictionary of display_name: line_edit pairs
        """
        self.mapping.update(mapping_dict)

    def clear_mappings(self) -> None:
        """Clear all existing mappings"""
        self.mapping.clear()

    def create_dictionary(self, validate_empty: bool = True) -> dict:
        """
        Create a dictionary from the current mappings.
        
        Args:
            validate_empty (bool): If True, checks for empty values
            
        Returns:
            Dictionary containing the mapped values
            
        Raises:
            ValueError: If validate_empty is True and empty values are found
        """
        settings_dict = {
            key: line_edit.text().strip()
            for key, line_edit in self.mapping.items()
        }
        
        if validate_empty:
            empty_fields = [key for key, value in settings_dict.items() if not value]
            if empty_fields:
                raise ValueError(f"The following fields are empty: {', '.join(empty_fields)}")
                
        return settings_dict

