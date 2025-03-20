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

from qgis.PyQt.QtWidgets import QTableWidgetItem
from qgis.core import QgsRasterLayer, QgsVectorLayer, QgsProject
from PyQt5.QtWidgets import (
	QComboBox,
	QPushButton,
	QVBoxLayout,
	QWidget,
	QMessageBox,
	QFileDialog,
	QListWidget,
)
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import fiona  # For vector files
import rasterio  # For raster files
from pathlib import Path


class Loop3dConfig:
	def __init__(self,config_log):
		# Placeholder attributes for GUI components
		self.pushButton_param_load_source_path = None
		self.lineEdit_param_load_source_path   = None
		self.config_log                        = config_log

	def select_folder(self, config_pushbutton, config_lineditor):
		"""
		Opens a file dialog to select a folder and updates the QLineEdit with the chosen path.
		# config_pushbutton: The pushbutton to be clicked to open the folder search
		# config_lineditor : The QLineEdit to append the folder path
		"""
		foldername = QFileDialog.getExistingDirectory(
			config_pushbutton,  # Reference to the parent widget
			"Select folder",
			"",  # Default starting directory
		)
		# Check if the QLineEdit is writable
		if config_lineditor.isReadOnly():
			self.config_log.addItem("The QLineEdit is read-only.")
			#print("The QLineEdit is read-only.")
		else:
			pass
			# print("The QLineEdit is writable.")
		existing_text = config_lineditor.text()
		config_lineditor.setText(f"{existing_text}\n{foldername}")
		return foldername

	def populate_list_widget(self, conf_shp_tif_listWidget):
		"""Populate the QListWidget with file names and file paths."""
		# Set the selection mode of the QListWidget to MultiSelection
		conf_shp_tif_listWidget.setSelectionMode(QListWidget.MultiSelection)
		layers = QgsProject.instance().mapLayers().values()

		for layer in layers:
			layer_path = layer.dataProvider().dataSourceUri().split("|", 1)[0]
			file_name = os.path.basename(layer_path)

			if file_name.endswith((".shp", ".tiff", ".tif", ".gif")):
				conf_shp_tif_listWidget.addItem(file_name)
				conf_shp_tif_listWidget.item(
					conf_shp_tif_listWidget.count() - 1
				).setData(
					0, layer_path
				)  # Store file path as data

	def create_file_dict(self, list_widget):
		"""Create a dictionary for all selected files."""
		# Set the selection mode of the QListWidget to MultiSelection
		list_widget.setSelectionMode(QListWidget.MultiSelection)
		selected_items = list_widget.selectedItems()
		if not selected_items:
			QMessageBox.warning(self, "Warning", "No files selected!")
			return
		selected_files = {
			Path(item.text()).name: item.data(0) for item in selected_items
		}
		return selected_files

	def generate_clipped_paths(self, input_files):
		"""
		Generates a dictionary with updated paths for files in a "clipped" folder.
		Ensures the "clipped" folder exists.

		Parameters:
			input_files (dict): A dictionary where keys are filenames and values are file paths.

		Returns:
			dict: A dictionary with updated paths in the "clipped" directory.
		"""
		output_files = {}

		for filename, filepath in input_files.items():
			# Get the directory and filename
			dir_path, file_name = os.path.split(filepath)
			# Create a new directory path for "clipped"
			clipped_dir = os.path.join(dir_path, "clipped")

			# Check if the "clipped" directory exists, and create it if not
			if not os.path.exists(clipped_dir):
				os.makedirs(clipped_dir)

			# Ensure the new name includes "_clip"
			file_base, file_ext = os.path.splitext(file_name)
			clipped_filename = f"{file_base}_clip{file_ext}"
			# Construct the full path for the clipped file
			clipped_filepath = os.path.join(clipped_dir, clipped_filename)
			# Add to the output dictionary
			output_files[filename] = clipped_filepath

		return output_files

	def load_data_in_qgis(self, folder_path):
		"""
		Automatically loads .shp and .tif files from a folder into the QGIS panel.
		:param folder_path: Path to the folder containing shapefiles and raster files.
		"""
		# Check if the folder exists
		if not os.path.exists(folder_path):
			self.config_log.addItem(f"The folder '{folder_path}' does not exist.")
			#print(f"The folder '{folder_path}' does not exist.")
			return

		# Get the current QGIS project
		project = QgsProject.instance()

		# Iterate through files in the folder
		list_of_data = os.listdir(folder_path)
		for idx, file_name in enumerate(list_of_data):
			file_path = os.path.join(folder_path, file_name)

			if file_name.endswith(".shp"):
				# Load shapefiles
				layer = QgsVectorLayer(file_path, file_name, "ogr")
				if layer.isValid():
					project.addMapLayer(layer)
					self.config_log.addItem(f"Loaded shapefile: {file_name}")
					#print(f"Loaded shapefile: {file_name}")
				else:
					self.config_log.addItem(f"Failed to load shapefile: {file_name}")
					#print(f"Failed to load shapefile: {file_name}")

			elif file_name.endswith(".tif"):
				# Load raster files
				layer = QgsRasterLayer(file_path, file_name)
				if layer.isValid():
					project.addMapLayer(layer)
					self.config_log.addItem(f"Loaded raster file: {file_name}")
					#print(f"Loaded raster file: {file_name}")
				else:
					#print(f"Failed to load raster file: {file_name}")
					self.config_log.addItem(f"Failed to load raster file: {file_name}")

	def show_message_box(self, title, msg1, msg2):
		# Create a message box
		msg_box = QMessageBox()
		msg_box.setWindowTitle(str(title))
		# Add Yes and No buttons, but we will modify their text
		msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

		# Change the button text
		msg_box.button(QMessageBox.Yes).setText(str(msg1))
		msg_box.button(QMessageBox.No).setText(str(msg2))
		# Execute the message box and check the result
		reply = msg_box.exec_()
		return reply

	def select_file(self):
		# Open a file dialog to select a file
		selected_ROI_file_path, _ = QFileDialog.getOpenFileName(
			None,
			"Select a File",
			"",
			"All Files (*.*);;Text Files (*.txt);;Shapefiles (*.shp);; GeoJSON Files (*.geojson)",
		)
		if selected_ROI_file_path:
			self.config_log.addItem(f"File selected: {selected_ROI_file_path}")
			#print(f"File selected: {selected_ROI_file_path}")
			# Extract the file name without the path to use as the layer name
			layer_name = selected_ROI_file_path.split("/")[-1].split(".")[0]
			layer = QgsVectorLayer(selected_ROI_file_path, layer_name, "ogr")
			if not layer.isValid():
				self.config_log.addItem("Failed to load the layer.")
				#print("Failed to load the layer.")
			else:
				QgsProject.instance().addMapLayer(layer)
				self.config_log.addItem(f"Layer '{layer_name}' added to QGIS.")
				#print(f"Layer '{layer_name}' added to QGIS.")
			return selected_ROI_file_path
		else:
			self.config_log.addItem("No file selected.")
			#print("No file selected.")
			return None


class CRSAppender:
	def __init__(self):
		# Initialize an empty list to store CRS authid values
		self.crs_list = []

	def populate_crs(self, crs_combo_box):
		"""
		Adds a CRS authid to the list if it's valid.

		Parameters:
			crs_code (str or int): The CRS code (e.g., "EPSG:4326" or 4326).
		"""
		self.crs_list.append(crs_combo_box.crs().authid())
		return self.crs_list


class CheckBoxWidget:
	def on_state_changed(self, state):
		"""
		Slot triggered when the state of the checkbox changes.
		"""
		if state == 2:  # Checked
			self.click_count += 1

			# Toggle off if clicked twice
			if self.click_count == 2:
				self.checkbox.setChecked(False)
				self.click_count = 0  # Reset click count
				self.label.setText("CheckBox State: Unchecked (Toggled Off)")
			else:
				self.label.setText("CheckBox State: Checked")
		elif state == 0:  # Unchecked
			self.click_count = 0  # Reset click count
			self.label.setText("CheckBox State: Unchecked")


class FileSelector:
	def __init__(self, directory):
		"""
		Initialize the FileSelector with a directory to scan for files.

		:param directory: Directory path where files are stored.
		"""
		self.directory = directory

	def list_files(self):
		"""
		List all files in the directory.

		:return: List of file paths.
		"""
		return [
			os.path.join(self.directory, f)
			for f in os.listdir(self.directory)
			if os.path.isfile(os.path.join(self.directory, f))
		]

	def is_raster_file(self, file_path):
		"""
		Check if a file is a valid raster file using Rasterio.

		:param file_path: Path to the file.
		:return: True if the file is a raster file, else False.
		"""
		try:
			with rasterio.open(file_path):
				return True
		except Exception:
			return False

	def is_vector_file(self, file_path):
		"""
		Check if a file is a valid vector file using Fiona.

		:param file_path: Path to the file.
		:return: True if the file is a vector file, else False.
		"""
		try:
			with fiona.open(file_path):
				return True
		except Exception:
			return False

	def select_files_by_type(self, file_type):
		"""
		Select files based on their type: 'vector' or 'raster'.

		:param file_type: Type of files to select ('vector' or 'raster').
		:return: List of file paths matching the given type.
		"""
		all_files = self.list_files()
		if file_type == "vector":
			return [f for f in all_files if self.is_vector_file(f)]
		elif file_type == "raster":
			return [f for f in all_files if self.is_raster_file(f)]
		else:
			raise ValueError("Invalid file_type. Use 'vector' or 'raster'.")

	def check_geometry_type(self, file_path):
		"""
		Check the geometry type of a shapefile using Fiona.
		"""
		try:
			with fiona.open(file_path) as src:
				return src.schema["geometry"]
		except Exception as e:
			print(f"Error: {e}")
			return None

	def inspect_all_shapefiles(self, shapefiles, flag_type):
		"""
		falg_type =[Point,Polygon,LineString, gif,tif]
		Inspect all shapefiles in the directory and print their geometry types.
		"""
		for shp in shapefiles:
			extension = str(os.path.basename(shp)).split(".")[-1]
			fiona_type = self.check_geometry_type(shp)
			if extension == "shp" and str(fiona_type) == flag_type:
				data_path = shp
				return data_path
			else:
				pass


class DataProcessor:
	def __init__(self, table_widget):
		"""
		Constructor to initialize the DataProcessor with a QTableWidget.
		"""
		self.table_widget = table_widget

	def xlayer_reader(self, layer_path):
		"""
		This function reads the layer from a given file path, retrieves its columns and data,
		and appends it to the provided QTableWidget.
		"""
		# Load the layer from the file path
		layer = QgsVectorLayer(layer_path, "Layer", "ogr")

		if not layer.isValid():
			print(f"Failed to load the layer from: {layer_path}")
			return

		# Get column names (headers)
		cols_header = [field.name() for field in layer.fields()]

		# Get the layer data (attributes)
		data = [feature.attributes() for feature in layer.getFeatures()]

		# Load data into the QTableWidget
		self.load_data_to_table(data, cols_header)

	def load_data_to_table(self, data, cols_header):
		"""
		This function appends data to the QTableWidget.
		"""
		# Set table columns headers
		self.table_widget.setColumnCount(len(cols_header))
		self.table_widget.setHorizontalHeaderLabels(cols_header)

		# Set table rows count based on the data
		self.table_widget.setRowCount(len(data))

		# Append data to the table
		for row_index, row_data in enumerate(data):
			for col_index, value in enumerate(row_data):
				self.table_widget.setItem(
					row_index, col_index, QTableWidgetItem(str(value))
				)


class ShapefileColumnExtractor:
	"""
	A class to extract the column headers of a shapefile's attribute table.

	Attributes:
		filepath (str): The file path to the shapefile.
	"""

	def __init__(self, filepath):
		"""
		Initializes the ShapefileColumnExtractor with the shapefile path.

		Args:
			filepath (str): Path to the shapefile.
		"""
		self.filepath = filepath

	def get_column_headers(self):
		"""
		Extracts and returns the column headers of the shapefile.

		Returns:
			list: A list of column names (attribute table headers).
		"""
		try:
			with fiona.open(self.filepath, "r") as shapefile:
				headers = shapefile.schema["properties"].keys()
				return list(headers)
		except Exception as e:
			print(f"Error reading shapefile: {e}")
			return []


class FieldMapSelector(QWidget):
	def __init__(self):
		super().__init__()

		# Initialize the combo box
		self.combo_box = QComboBox()

		# Initialize the button
		self.select_button = QPushButton("Select Files")
		self.select_button.clicked.connect(self.create_file_dict)

		# Set up the layout
		layout = QVBoxLayout()
		layout.addWidget(self.combo_box)
		layout.addWidget(self.select_button)
		self.setLayout(layout)

		# Populate the combo box with layer file names
		self.populate_combo_box()

	def populate_combo_box(self):
		"""Populate the QComboBox with file names from the QGIS Layers Panel."""
		layers = QgsProject.instance().mapLayers().values()

		for layer in layers:
			layer_path = layer.dataProvider().dataSourceUri().split("|", 1)[0]
			file_name = os.path.basename(layer_path)

			if file_name.endswith((".shp", ".tiff")):
				self.combo_box.addItem(file_name, layer_path)

	def create_file_dict(self):
		"""Create a dictionary for the selected file."""
		selected_index = self.combo_box.currentIndex()
		if selected_index == -1:
			QMessageBox.warning(self, "Warning", "No file selected!")
			return

		file_name = self.combo_box.currentText()
		file_path = self.combo_box.itemData(selected_index)

		# Create a dictionary for the selected file
		selected_files = {file_name: file_path}
		QMessageBox.information(self, "Selected File", f"{selected_files}")
