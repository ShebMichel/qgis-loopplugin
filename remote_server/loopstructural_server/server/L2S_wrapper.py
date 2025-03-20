#!/usr/bin/env python
# coding: utf-8

## Loop Workflow Example 3
from map2loop.project import Project
from map2loop.m2l_enums import VerboseLevel
import LoopProjectFile as LPF
import LoopStructural
import numpy as np
from scipy.interpolate import RegularGridInterpolator
import time
import os, ast, shutil

####
from osgeo import gdal
from loopstructuralvisualisation import Loop3DView
from LoopStructural.modelling import (
    LoopProjectfileProcessor as LPFProcessor,
)



def move_vtk_files(source_directory, target_directory):
    # Ensure the target directory exists
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
        # print(f"Directory '{target_directory}' created.")
    output_data_list = []
    # Loop through all files in the source directory
    for filename in os.listdir(source_directory):
        # Check if the filename contains '.vtk'

        if filename.endswith(".vtk"):
            source_file_path = os.path.join(source_directory, filename)

            # Move the file to the target directory
            destination_file_path = os.path.join(target_directory, filename)
            output_data_list.append(destination_file_path)
            shutil.move(source_file_path, destination_file_path)
            # print(f"Moved {source_file_path} to {destination_file_path}")
    return output_data_list


class LoopStructural_Wrapper:
    """Wrapper class for loopStructural process"""

    def __init__(self, param_conf):
        self.param_conf = param_conf

    def run_all(self, **kwargs):

        t1 = time.time()

        LPFilename = str(self.param_conf["LPFilename"])                               #./source_data/server_local_source.loop3d" 
        fault_params = {
            "interpolatortype": str(self.param_conf["interpolatortype"]),             #"FDI",
            "nelements": float(self.param_conf["fault nelements"]),             #1e4,
        }
        foliation_params = {
            "interpolatortype": str(self.param_conf["interpolatortype"]),             #"FDI",  #'interpolatortype':'PLI',
            "nelements":float(self.param_conf["foliation nelements"]),      #1e5,  # how many tetras/voxels
            "regularisation": int(self.param_conf["regularisation"]),                 #5,
        }
        print(f" fault parameters {fault_params}")
        print(f" foliation parameters {foliation_params}")
        projFile = LPF.ProjectFile(LPFilename)
        processedData = LPFProcessor(projFile)
        processedData.foliation_properties["sg"] = foliation_params
        processedData.fault_properties["interpolatortype"] = fault_params[
            "interpolatortype"
        ]
        processedData.fault_properties["nelements"] = fault_params["nelements"]
        model = LoopStructural.GeologicalModel.from_processor(processedData)
        model.update()
        model_name = "output_data"

        # check whether directory 'output_data' already exists
        if not os.path.exists(str(model_name)):
            os.mkdir(str(model_name))
            print("Folder" + str(model_name) + " is created!")
        else:
            print("Folder " + str(model_name) + " already exists ")
        try:
            vtk_path = str(os.getcwd()) + "/" + str(model_name) + "/vtk/"
        except:
            print("./vtk test failed")
            pass
        if not os.path.exists(vtk_path):
            os.mkdir(vtk_path)
        # directories
        source_directory = "./"
        vtk_directory = "output_data/vtk"
        #
        model.save("model_surface.vtk")
        t2 = time.time()

        # ## Elapsed Time
        ls_time = t2 - t1
        total = ls_time
        ls_string = f"{ls_time} sec" if ls_time < 60 else f"{ls_time/60.0} min"
        total_string = f"{total} sec" if total < 60 else f"{total/60.0} min"
        print(f"LoopStructural {ls_string}, Total {total_string}")
        print("loopstructural run successfully!!! ")
        ####
        try:
            output_data_list = move_vtk_files(source_directory, vtk_directory)
            print(f"output data lists: {output_data_list}")
        except:
            pass
