#!/usr/bin/env python
# coding: utf-8

# # Loop Workflow Example 3

# * High level approach to making a 3D model from just a bounding box and source files as input. (In Australia only for now. Documentation to come)
# This is the wrapper module to pass data and execute calculation in your container
from map2loop.project import Project
from map2loop.m2l_enums import Datatype, VerboseLevel
from map2loop.sampler import SamplerSpacing, SamplerDecimator
from map2loop.sorter import SorterAlpha
import time
import os, ast
import json
from pathlib import Path
##

from datetime import datetime


class M2l_Wrapper:
	"""Wrapper class for map2loop process"""

	def __init__(self,conf_param,log_object,m2l_par_dict,bbox):
		try: 
			self.conf_param    = conf_param
			self.log_object    = log_object
			self.m2l_par_dict  = m2l_par_dict
			self.bbox          =bbox

			print(f" input parameters : {self.m2l_par_dict}")
			print(f"Config param is {self.conf_param}")

		except:
			print(f"Error ")
		self.proc_data_folder  = str(Path(self.conf_param['geology_filename']).parent)
		path                   = Path(str(self.conf_param['geology_filename']))
		parent_path            = path.parent
		self.m2l_output_folder = os.path.join(str(parent_path) , str(self.conf_param['M2L Output']) )
		self.l2s_output_folder = os.path.join(str(parent_path) , str(self.conf_param['L2S Output']) )
		# check if folder exist, if not create it
		for folder in [self.m2l_output_folder,self.proc_data_folder,self.l2s_output_folder]:
			os.makedirs(str(folder), exist_ok=True)



	def check_hjson_file(self,folder_path, filename="mapping.hjson"):
		"""
		Check if a HJSON file exists in the specified folder.
		
		Args:
			folder_path (str): Path to the folder to check
			filename (str): Name of the HJSON file to look for
		
		Returns:
			tuple: (bool, str) - (Whether file exists, Status message)
		"""
		try:
			# Convert to Path object for better path handling
			folder = Path(folder_path)
			
			# Check if folder exists
			if not folder.exists():
				return False, f"Folder does not exist: {folder_path}"
			
			if not folder.is_dir():
				return False, f"Path is not a directory: {folder_path}"
			
			# Check for the file
			file_path = folder / filename
			print(f"file is {file_path}")
			if file_path.exists():
				return True, f"File found: {file_path}"
			else:
				return False, f"File not found: {file_path}"
				
		except Exception as e:
			return False, f"Error checking file: {str(e)}"



	def run_all_wrapper(self, **kwargs):
		# return processed map2loop data and .loop3d output
		t0 = time.time()
		try:
			# Check if hjson file exist
			exists, message = self.check_hjson_file(self.proc_data_folder, filename="output.hjson")
		except:
			print(f" Error no HJSON config prameter found!.")

		
		loop_project_filename = os.path.join(self.m2l_output_folder, "local_source.loop3d")
		bbox_3d=self.bbox
		self.log_object.addItem(f"Running proj")
		# output locations and projection to work in
		proj = Project(
			geology_filename          = str( self.conf_param['geology_filename']),
			fault_filename            = str(self.conf_param['fault_filename'] ),
			structure_filename        = str(self.conf_param['structure_filename'] ),
			mindep_filename           = 'http://13.211.217.129:8080/geoserver/loop/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=loop:null_mindeps&bbox={BBOX_STR}&srs=EPSG:28350&outputFormat=shape-zip',
			dtm_filename              = str(self.conf_param['dtm_filename']),
			metadata_filename         = str(self.conf_param['metadata_filename']),
			clut_filename             = str(self.conf_param['clut_filename']),
			clut_file_legacy          = True,
			verbose_level             = VerboseLevel.NONE,
			tmp_path                  = str(self.m2l_output_folder),
			working_projection        = str(self.conf_param['working_projection']),
			bounding_box              = bbox_3d,
			loop_project_filename     = str(loop_project_filename),
			overwrite_loopprojectfile = True
		)

		# Remove faults less than 5km
		self.log_object.addItem(f"Removing faults less than {self.m2l_par_dict['Minimun fault length']} km")
		proj.set_minimum_fault_length(self.m2l_par_dict['Minimun fault length'])#5000.0)
		self.log_object.addItem(f"Sampling for geology and fault maps to {self.m2l_par_dict['Geology Sampler Spacing']} m")
		# Set sampling distance for geology and fault maps to 200m
		proj.set_sampler(Datatype.GEOLOGY, SamplerSpacing(self.m2l_par_dict['Geology Sampler Spacing'])) #(200.0))
		proj.set_sampler(Datatype.FAULT, SamplerSpacing(self.m2l_par_dict['Fault Sampler Spacing']))    #((200.0))
		self.log_object.addItem(f"Taking every second orientation observation (0 or 1 means take all observations)")
		# Set to only take every second orientation observation (0 or 1 means take all observations)
		proj.set_sampler(Datatype.STRUCTURE, SamplerDecimator(self.m2l_par_dict['Sampler Decimator']))#(2))

		self.log_object.addItem(f"Sorting with set_sorter...SorterAlpha or (SorterAlpha, SorterAgeBased, SorterUseHint, SorterUseNetworkX, SorterMaximiseContacts, SorterObservationProjections)")
		# Specify which stratigraphic columns sorter to use, other options are
		# (SorterAlpha, SorterAgeBased, SorterUseHint, SorterUseNetworkX, SorterMaximiseContacts, SorterObservationProjections)
		proj.set_sorter(SorterAlpha())
		self.log_object.addItem(f"Running proj.run_all(user_defined_stratigraphic_column=None, take_best=True)")
		proj.run_all(user_defined_stratigraphic_column=None, take_best=True)
		self.log_object.addItem(f"Map2loop Succesfully completed")
		self.log_object.addItem(f"===============================================================================")
		self.log_object.addItem(f"NOW RUN LOOPSTRUCTURAL")
	
