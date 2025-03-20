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

#import vtk
import subprocess,os
import pyvista as pv
from pyvistaqt import BackgroundPlotter
#import panel as pn
from pathlib import Path


class VTKVisualizer:
    def __init__(self, vtk_folder_path):
        """Initialize with a list of VTK file paths."""
        
        self.vtk_folder_path =vtk_folder_path
    
    def visualize(self):
        """
        This function call the show_3d_plot
        """
        self.output_name_list = os.listdir(str(self.vtk_folder_path))
        output_list=[ os.path.join(self.vtk_folder_path, key) for key in self.output_name_list]
        self.plot_block_model_with_surfaces_and_stratigraphy(output_list)
        return
     
    def plot_block_model_with_surfaces_and_stratigraphy(self,list_of_files):

        ## Read individual dataset
        surfaces = [a for a in list_of_files if "Fault" in a]
        stratigraphy = [a for a in list_of_files if "sg" in a]
        block_model_path = [a for a in list_of_files if "block_model" in a][0]
        # Read the block model
        block_model_mesh = pv.read(block_model_path)

        # Initialize the plotter
        plotter = BackgroundPlotter()

        # Add the block model to the plotter
        plotter.add_mesh(
            block_model_mesh, color="lightblue", opacity=0.7, label="Block Model"
        )

        # Add all surfaces to the plotter
        for surface_path in surfaces:
            surface_mesh = pv.read(surface_path)
            plotter.add_mesh(
                surface_mesh,
                color="green",
                opacity=0.6,
                label=f"Surface: {Path(surface_path).name}",
            )

        # Add all stratigraphy layers to the plotter
        for stratigraphy_path in stratigraphy:
            stratigraphy_mesh = pv.read(stratigraphy_path)
            plotter.add_mesh(
                stratigraphy_mesh,
                color="brown",
                opacity=0.8,
                label=f"Stratigraphy: {Path(stratigraphy_path).name}",
            )

        # Set the plotter title and background
        plotter.set_background("white")
        plotter.add_text(
            f"3D Model",
            position=(0.25, 0.95),
            font_size=12,
            color="black",
            shadow=True,
            viewport=True,
        )
        # f"Model: {Path(block_model_path).name}",
        # Display the legend
        plotter.add_legend()

        # Show the plot
        plotter.show()
        return


