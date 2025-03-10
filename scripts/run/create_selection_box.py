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


from qgis.PyQt.QtWidgets import QAction
from qgis.utils import iface
from typing import List, Optional
from PyQt5.QtWidgets import QMessageBox,QDialog, QVBoxLayout, QPushButton, QLineEdit,QLabel, QWidget

from PyQt5.QtWidgets import QDialog, QDialog, QVBoxLayout, QPushButton, QDialogButtonBox,QHBoxLayout
from .docker.check_docker_path import find_docker_path,is_docker_running, is_container_running
#from .qgis.map2loop_qgis_button import run_map2loop, m2l_wrapper, Run_test
#from .qgis.Run_test import map_2l
from .qgis.m2l_wrapper import M2l_Wrapper
from .create_user_input import VerticalLayoutForm



from pathlib import Path
import os,subprocess
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel

class ServerInfoPanel:
	#def __init__(self,username,portname,hostname,map2loop_button,run_log_listWidget,config_param):
	def __init__(self,run_log_listWidget,loop_docker_pushButton):
		super().__init__()
		"""
		Initializes the button panel with predefined server options.
		"""
		self.run_log_listWidget     = run_log_listWidget
		self.loop_docker_pushButton = loop_docker_pushButton 
		#self.run_loopstructural_pushButton.clicked.connect(self.show_input_dialog)

	
	def load_docker_credentials(self):
		"""Opens a dialog with labels and QLineEdit fields for user input."""
		self.dialog = QDialog()
		self.dialog.setWindowTitle("Server Credentials")
		layout = QVBoxLayout()

		# Name input
		self.name_label = QLabel("Name:")
		self.name_edit = QLineEdit()
		layout.addWidget(self.name_label)
		layout.addWidget(self.name_edit)

		# Hostname input
		self.hostname_label = QLabel("Hostname:")
		self.hostname_edit = QLineEdit()
		layout.addWidget(self.hostname_label)
		layout.addWidget(self.hostname_edit)

		# Portname input
		self.portname_label = QLabel("Port Number:")
		self.portname_edit = QLineEdit()
		layout.addWidget(self.portname_label)
		layout.addWidget(self.portname_edit)

		# Buttons
		button_layout = QHBoxLayout()
		self.ok_button = QPushButton("OK")
		self.cancel_button = QPushButton("Cancel")
		button_layout.addWidget(self.ok_button)
		button_layout.addWidget(self.cancel_button)
		layout.addLayout(button_layout)

		# Connect buttons
		self.ok_button.clicked.connect(lambda: self.on_ok_button_clicked(self.dialog))
		self.cancel_button.clicked.connect(lambda: self.on_cancel_button_clicked(self.dialog))

		self.dialog.setLayout(layout)
		self.dialog.exec_()
		return 



	def on_ok_button_clicked(self, dialog):
		"""Handles the OK button click."""
		dialog_data = {
			"name": self.name_edit.text(),
			"hostname": self.hostname_edit.text(),
			"port": self.portname_edit.text(),
		}
		self.loop_docker_pushButton.setEnabled(False)
		print("OK button clicked. Dialog will close now.")
		# Perform any necessary actions with the data (e.g., save credentials)
		dialog.accept()  # Closes the dialog

	def on_cancel_button_clicked(self, dialog):
		"""Handles the Cancel button click."""
		print("Cancel button clicked. Dialog will close now.")
		dialog.reject()  # Closes the dialog


	def get_data(self):
		self.docker_credentials = {
			"name": self.name_edit.text(),
			"hostname": self.hostname_edit.text(),
			"portname": self.portname_edit.text()
		}
		return self.docker_credentials


class Map2loopInQGIS:
	def __init__(self,object_button,log_object,m2l_par_dict,config_param,bbox):
		self.object_button = object_button
		self.log_object    = log_object
		self.m2l_par_dict  = m2l_par_dict
		self.config_param  = config_param
		self.bbox          =bbox

	def map2loop_in_qgis(self):
		# this function run map2loop in qgis locally
		#self.config_param={'geology_filename': 'C:/Users/00110138/OneDrive - The University of Western Australia/Project/Testing/2025/Loop/roi_test\\geol_clip.shp', 'fault_filename': 'C:/Users/00110138/OneDrive - The University of Western Australia/Project/Testing/2025/Loop/roi_test\\faults_clip.shp', 'structure_filename': 'C:/Users/00110138/OneDrive - The University of Western Australia/Project/Testing/2025/Loop/roi_test\\structure_clip.shp', 'dtm_filename': 'C:/Users/00110138/OneDrive - The University of Western Australia/Project/Testing/2025/Loop/roi_test\\dtm_rp.tif', 'metadata_filename': 'C:\\Users\\00110138\\OneDrive - The University of Western Australia\\Project\\Testing\\2025\\Loop\\roi_test\\process_data\\output.hjson', 'working_projection': 'EPSG:28350', 'clut_filename': 'C:\\Users\\00110138\\OneDrive - The University of Western Australia\\Project\\Testing\\2025\\Loop\\roi_test\\process_data\\500kibg_colours.csv'}
		
		print(f" QGIS runing map2loop... ... {self.config_param}")

		m2l=M2l_Wrapper(conf_param=self.config_param,log_object=self.log_object, m2l_par_dict=self.m2l_par_dict,bbox=self.bbox)
		m2l.run_all_wrapper()
		return 


# class Loop2structuralOnServer():
# 	def __init__(self):
# 		self.user_data = {}  # Store user input data


# 	def log_input(self):
# 		"""Logs user input."""
# 		if self.user_data:
# 			#print(f"User {self.user_data['name']}, hostname {self.user_data['hostname']}, portname {self.user_data['portname']}")
# 			self.run_log_listWidget.addItem(f"Username: {self.user_data['name']}")
# 			self.run_log_listWidget.addItem(f"Hostname: {self.user_data['hostname']}")
# 			self.run_log_listWidget.addItem(f"Port Name: {self.user_data['portname']}")

# 	def execute_function(self):
# 		"""Uses stored data to execute a function when Run Loop Structural is clicked."""
# 		if self.user_data:
# 			#print(f"Executing function with: {self.user_data}")
# 			self.run_log_listWidget.addItem(f"Executing with: {self.user_data}")
# 		else:
# 			#print("No data available. Please enter details first.")
# 			self.run_log_listWidget.addItem("No data available. Please enter details first.")


