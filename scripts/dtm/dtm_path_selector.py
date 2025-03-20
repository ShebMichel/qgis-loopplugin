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

from qgis.core import QgsRasterLayer, QgsProject
from qgis.PyQt.QtWidgets import QMessageBox,QInputDialog
from qgis.PyQt.QtGui import QIcon
from typing import List, Optional
from pathlib import Path

class DTMPathSelector:
	"""
	A class to handle DTM file path selection from QGIS layers panel
	and update a QLineEdit widget with the selected path.
	"""
	def __init__(self,config_log,line_edit):
		"""
		Initialize the DTM path selector.
		
		Args:
			line_edit: QLineEdit widget where the DTM path will be displayed
		"""
		self.line_edit  = line_edit
		self.config_log = config_log

	def get_dtm_paths(self) -> List[str]:
		"""
		Get file paths of all raster layers in QGIS project that could be DTMs.
		
		Returns:
			List of file paths for potential DTM layers
		"""
		project = QgsProject.instance()
		dtm_paths = []
		
		for layer in project.mapLayers().values():
			if isinstance(layer, QgsRasterLayer):
				layer_path = layer.source()
				# You might want to add additional checks here specific to your DTM files
				# For example, checking file extensions or layer properties
				dtm_paths.append(layer_path)
				self.config_log.addItem(f" Select dtm is: {layer_path}")
		return dtm_paths



# from PyQt5.QtWidgets import QInputDialog, QMessageBox
# from typing import Optional

	def select_dtm_path(self) -> Optional[str]:
	    """
	    Select a DTM path from available layers using a combobox if multiple layers exist.

	    Returns:
	        Selected DTM path or None if no selection was made.
	    """
	    dtm_paths = self.get_dtm_paths()

	    if not dtm_paths:
	        QMessageBox.warning(
	            None,
	            "No DTM Found",
	            "No raster layers found in the project. Please add a DTM layer first."
	        )
	        return None

	    if len(dtm_paths) == 1:
	        return dtm_paths[0]

	    # Create a combobox dialog for layer selection
	    layer_names = [Path(path).stem for path in dtm_paths]
	    selected_layer, ok = QInputDialog.getItem(
	        None, "Select DTM", "Multiple potential DTM layers found.\nPlease select one.", layer_names, 0, False
	    )

	    if not ok or selected_layer not in layer_names:
	        return None

	    selected_index = layer_names.index(selected_layer)
	    return dtm_paths[selected_index]


	# def select_dtm_path(self) -> Optional[str]:
	# 	"""
	# 	Select a DTM path from available layers and handle multiple path scenarios.
		
	# 	Returns:
	# 		Selected DTM path or None if no selection was made
	# 	"""
	# 	dtm_paths = self.get_dtm_paths()
		
	# 	if not dtm_paths:
	# 		QMessageBox.warning(
	# 			None,
	# 			"No DTM Found",
	# 			"No raster layers found in the project. Please add a DTM layer first."
	# 		)
	# 		return None
			
	# 	if len(dtm_paths) == 1:
	# 		return dtm_paths[0]
			
	# 	# If multiple DTMs found, show selection dialog
	# 	msg_box = QMessageBox()
	# 	msg_box.setIcon(QMessageBox.Question)
	# 	msg_box.setWindowTitle("Select DTM")
	# 	msg_box.setText("Multiple potential DTM layers found. Please select one:")
		
	# 	# Create buttons for each DTM path
	# 	buttons = []
	# 	for path in dtm_paths:
	# 		filename = Path(path).name.split('.')[0]
	# 		button = msg_box.addButton(filename, QMessageBox.ActionRole)
	# 		#button = msg_box.addButton(path, QMessageBox.ActionRole)
	# 		buttons.append(button)
		
	# 	cancel_button = msg_box.addButton("Cancel", QMessageBox.RejectRole)
		
	# 	msg_box.exec_()
	# 	clicked_button = msg_box.clickedButton()
		
	# 	if clicked_button == cancel_button:
	# 		return None
			
	# 	selected_index = buttons.index(clicked_button)
	# 	return dtm_paths[selected_index]

	def update_line_edit(self) -> None:
		"""
		Update the QLineEdit with the selected DTM path.
		"""
		selected_path = self.select_dtm_path()
		if selected_path:
			self.line_edit.setText(selected_path)
		return selected_path

# Example usage:
'''
# Assuming you have a QLineEdit widget named lineEdit_dtm_path in your UI
selector = DTMPathSelector(self.lineEdit_dtm_path)
selector.update_line_edit()
'''
