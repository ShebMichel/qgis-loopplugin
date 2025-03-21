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

import os
import json
import glob
import shutil
import ast
import  datetime
from pathlib import Path
import platform

from qgis.PyQt import QtWidgets, uic
from qgis.utils import iface
from qgis.PyQt.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDir
# visualiz
from .scripts.run.viz.vizualize_vtk import VTKVisualizer
# run
from .scripts.run.qgis.L2S_wrapper_in_qgis import LoopStructural_Wrapper_Qgis
from .scripts.run.create_new_shapefile import ShapefileExtractorFromJSON
from .scripts.run.create_selection_box import ServerInfoPanel, Map2loopInQGIS
from .scripts.run.info_text import How_to_run_models
from .scripts.run.docker.run_docker import run_docker_compose
from .scripts.run.docker.loopstructural_client import LoopClientManager
#from .scripts.run.docker.data_transfert_to_local import DockerDataCopy
# config
from .scripts.config.loop_config import Loop3dConfig, CRSAppender
from .scripts.config.settings_dict import SettingsDictionary
from .scripts.config.roi_selector import RoishapefileSelector
from .scripts.config.json_data_saver import JSONDataHandler
from .scripts.config.widget_reset import QtWidgetResetter
from .scripts.config.load_qt_features import GeologyFaultStructureComboBoxes
from .scripts.config.json_file_handler import JSONDataPathHandler
from .scripts.config.checkbox_handler import LayerCheckboxHandler
from .scripts.config.bbox_extract import extract_bbox, get_shapefile_bounds
from .scripts.config.missing_parameters import fill_up_map2loop_parameters,fill_up_preprocessor_parameters
# geology
from .scripts.geology.geology_state_saver import StateSaver
# fault
from .scripts.fault.fault_state_saver import FStateSaver
# structure
from .scripts.structure.struct_state_saver import StructStateSaver
# dtm
from .scripts.dtm.dtm_path_selector import DTMPathSelector
# roi
from .scripts.roi.create_your_roi import create_scratch_layer_and_activate_clipping,save_roi_from_panel,DataClipper
# hover event
from .hover_event import assign_tooltips_to_ui_elements
FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "Loop3D_ModelGenerator_dockwidget_base.ui")
)


class Loop3DModelGenDockWidget(QtWidgets.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(Loop3DModelGenDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://doc.qt.io/qt-5/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        # Initialize geo_sorted_data as global parameter
        # QGIS version
        version = "v.0.1"

        # Append model instructions
        self.logs_list = [
            self.conf_log_listWidget,
            self.geology_log_listWidget,
            self.fault_log_listWidget,
            self.struct_log_listWidget,
            self.run_log_listWidget,
        ]
        How_to_run_models(self, list_log_objects=self.logs_list)
        # Show qt features infos
        assign_tooltips_to_ui_elements(self)
        # Plugin version
        self.version_label.setText(f"version: {version}")
        # Get the QGIS plugin path
        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))
        ## Hide Data table groupbox
        self.geology_groupBox_5.hide()
        self.fault_groupBox_5.hide()
        self.struct_groupBox_5.hide()
        # self.pushButton_param_load_source_path.clicked.connect(self.load_folder_path)
        self.load_configdata_from_file_radioButton.toggled.connect(
            self.load_folder_path
        )
        self.load_configdata_from_json_radioButton.toggled.connect(
            self.fill_config_from_json
        )
        # CRS
        self.CRS_pushButton_load_value.clicked.connect(self.select_crs_value)
        # Clear Selection
        # Use TabWidgetCleaner to clear all tabs after a delay
        self.ResetConfiguration_pushButton.clicked.connect(self.reset_widgets)
        # Run
        self.Run_Preprocessor_pushButton.clicked.connect(self.save_preprocessed_data)
        self.Run_Map2loop_pushButton.clicked.connect(self.run_map2loop)
        self.loop_docker_pushButton.clicked.connect(self.show_input_dialog)
        self.loop_qgis_pushButton.clicked.connect(self.show_input_dialog)
        self.Run_LoopStructural_pushButton.clicked.connect(self.run_loopstructural)

        # ROI Section
        self.Rawdata_radioButton.toggled.connect(self.roi_clipping_processor)
        self.clippeddata_radioButton.toggled.connect(self.roi_clipping_processor)
        self.CreateROI_radioButton.toggled.connect(self.on_roi_toggled)
        self.ExistingROI_radioButton.toggled.connect(self.on_roi_toggled)
        self.Ok_ClipLayer.clicked.connect(self.select_data_to_be_clipped)

        ### ## Geology & Toggle checkbox
        self.geology_Qgis_checkBox.stateChanged.connect(self.checkbox_toggled)
        self.geology_json_checkBox.stateChanged.connect(self.checkbox_toggled)

        ### fault & Toggle checkbox
        self.fault_Qgis_checkBox.stateChanged.connect(self.checkbox_toggled)
        self.fault_json_checkBox.stateChanged.connect(self.checkbox_toggled)

        ### struct & Toggle checkbox
        self.struct_Qgis_checkBox.stateChanged.connect(self.checkbox_toggled)
        self.struct_json_checkBox.stateChanged.connect(self.checkbox_toggled)

        ###  DTM
        self.conf_AUS_radioButton.toggled.connect(self.select_dtm_path)
        self.conf_JSON_radioButton.toggled.connect(self.select_dtm_path)
        self.conf_QGIS_radioButton.toggled.connect(self.select_dtm_path)

        # Save Config parameters
        # self.SaveAllConfig_pushButton.clicked.connect(self.save_all_config_parameters)
        # self.SaveAllConfig_pushButton.clicked.connect(self.save_geol_parameters)
        # self.SaveAllConfig_pushButton.clicked.connect(self.save_fault_parameters)
        # self.SaveAllConfig_pushButton.clicked.connect(self.save_struct_parameters)
        # 3D Visualization
        self.Run_viz_pushButton.clicked.connect(self.plot_surfaces)
        # Initialize the GeologyFaultStructureComboBoxes class with this window as the parent
        boxes = GeologyFaultStructureComboBoxes.get_combo_boxes_and_param_boxes(self)
        # # Access the geology combo boxes and parameters
        self.geology_combo_boxes = boxes["geology_combo_boxes"]
        self.geology_param_boxes = boxes["geology_param_boxes"]

        # # Access the fault combo boxes and parameters
        self.fault_combo_boxes = boxes["fault_combo_boxes"]
        self.fault_param_boxes = boxes["fault_param_boxes"]

        # # Access the structure combo boxes and parameters
        self.struct_combo_boxes = boxes["struct_combo_boxes"]
        self.struct_param_boxes = boxes["struct_param_boxes"]

        # Set Enable False the ROI features
        self.CreateROI_radioButton.setEnabled(False)
        self.ExistingROI_radioButton.setEnabled(False)
        self.Ok_ClipLayer.setEnabled(False)
        self.save_roi.setEnabled(False)
 
        ## set server off
        self.loop_gcp_pushButton.setEnabled(False)
        self.loop_aws_pushButton.setEnabled(False)
        self.loop_qgis_pushButton.setEnabled(False)
        self.loop_docker_pushButton.setEnabled(False)

       ## set qpushbutton off
        self.Run_LoopStructural_pushButton.setEnabled(False)
        self.loop_docker_pushButton.setEnabled(False)
        self.Run_viz_pushButton.setEnabled(False)
        #self.Run_Preprocessor_pushButton.setEnabled(False)
        self.Run_Preprocessor_pushButton.setEnabled(True)
        self.Run_LoopStructural_pushButton.setEnabled(False)
        self.Run_Map2loop_pushButton.setEnabled(False)     ## To be deleted soon
        ###############################################################
    def plot_surfaces(self):
        # This return a 3D plot of the model
        visualizer = VTKVisualizer(self.local_output_dir)
        visualizer.visualize()
        self.run_log_listWidget.addItem(f" 3D Show ---> Success !!!!!")

    def show_input_dialog(self):
    
        # show dynamic input for server
        self.server_flag = self.sender().text()
        self.Run_LoopStructural_pushButton.setEnabled(True)
       
        if self.server_flag == "DOCKER":
            self.loop_docker_pushButton.setEnabled(False)
            # self.loop_gcp_pushButton.setEnabled(False)
            # self.loop_aws_pushButton.setEnabled(False)
            self.loop_qgis_pushButton.setEnabled(False)
            loop_obj = ServerInfoPanel(
                run_log_listWidget=self.run_log_listWidget,
                loop_docker_pushButton=self.loop_docker_pushButton,
            )
            loop_obj.load_docker_credentials()
            
            yaml_dir = os.path.join(self.plugin_dir, "scripts","run","docker","loopstructural_server")
            if platform.system() == "Windows":
                self.container_name = run_docker_compose(
                    self, yaml_dir, run_log_listWidget=self.run_log_listWidget
                )
                self.server_info = loop_obj.get_data()
                self.run_log_listWidget.addItem(f"{self.container_name} ready to be used")
            else:
                print(f" Using a different platform, eitheir linux or mac")
            return self.server_info
        
        elif self.server_flag=="QGIS":
            self.loop_qgis_pushButton.setEnabled(False)
            self.loop_docker_pushButton.setEnabled(False)
            self.run_log_listWidget.addItem(f"LoopStructural running in QGIS Locally!")
            return 
        
    def run_loopstructural(self):
        # Run loopstructural
        self.loop_flag = self.sender().text()
        self.Run_LoopStructural_pushButton.setEnabled(False)
        self.Run_viz_pushButton.setEnabled(True)
        self.loop_flag = self.sender().text()
        server_output_folder     = './output_data/vtk'  # server output directory
        m2l_output = self.m2l_output_lineedit.text()
        l2s_output = self.l2s_output_lineedit.text()
        # move .loop3d
        loop3d_file = str(self.process_path / m2l_output / "local_source.loop3d")
        destination = str(self.process_data_path + "/")
        shutil.copy(loop3d_file, destination)
        self.run_log_listWidget.addItem(f".loop3d file moved in process_data")
       # running_container_name ="loopstructural_server-loopstructural-1"
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.local_output_dir = str(self.process_path / l2s_output / f"{timestamp}/vtk")
        # Check if the folder exists, if not, create it
        os.makedirs(self.local_output_dir, exist_ok=True)
        self.run_log_listWidget.addItem(f"Folder '{self.local_output_dir}' is ready!")
        if self.server_flag =="QGIS":
            self.run_log_listWidget.addItem(f"LoopStructural running in QGIS Locally!")
            param_conf = {"LPFilename": str(loop3d_file),"fault nelements": self.fault_nelts_lineedit.text(), "regularisation": self.regularisation_lineedit.text(),"interpolatortype": self.interpolator_comboBox.currentText(),"foliation nelements": self.foliation_nelts_lineedit.text()}
            l2s_obj=LoopStructural_Wrapper_Qgis(param_conf,self.run_log_listWidget,self.local_output_dir)
            result_output_path=l2s_obj.run_all()
            try:
                output_data_list= l2s_obj.move_vtk_files(result_output_path,self.local_output_dir)
            except Exception as e:
                
                print(f"Error: {e}")

            self.loop_qgis_pushButton.setEnabled(False)
        else:
            # Initialize LoopClientManager
            l2s_manager = LoopClientManager(self.server_info['hostname'],int(self.server_info['portname']))
            try: 
                # Ping the server
                if l2s_manager.ping_server():
                    self.run_log_listWidget.addItem("Server is online. Proceeding with file transfer...")
                    data_list = glob.glob(self.process_data_path + "/*")
                    N = len(data_list)
                    for idx, filepath in enumerate(data_list):
                        filename = Path(filepath).name
                        upload_response = l2s_manager.data_uploader(filename, filepath, idx, N)
                        self.run_log_listWidget.addItem(f"Upload Response: {upload_response}")
                        if upload_response  == "All data from client 1 received" and idx + 1 == N:
                            # Execute loop process
                            conf_param = {"LPFilename": "./server/source_data/server_local_source.loop3d","fault nelements": self.fault_nelts_lineedit.text(), "regularisation": self.regularisation_lineedit.text(),"interpolatortype": self.interpolator_comboBox.currentText(),"foliation nelements": self.foliation_nelts_lineedit.text()}
                            loop_output, loop_exec_msg = l2s_manager.loop_executor(str(conf_param))
                            # # Convert string to dictionary
                            vtk_files = ast.literal_eval(loop_output)
                            Nbre_server_data = len(vtk_files)
                            self.run_log_listWidget.addItem(f"{Nbre_server_data} Files to download from the server")
                            if loop_exec_msg == "LoopStructural execution completed successfully":
                                self.run_log_listWidget.addItem("LoopStructural execution completed successfully")
                                try:
                                    idx=0
                                    for server_filename, server_path in vtk_files.items():
                                        l2s_manager.data_downloader(str(server_filename),str(self.local_output_dir),int(Nbre_server_data), int(idx))
                                        if idx+1 == Nbre_server_data:
                                            self.run_log_listWidget.addItem(f"ALL {Nbre_server_data} FILES ARE SUCCESSFULLY DOWNLOADED!")
                                            self.run_log_listWidget.addItem(f"====================================== 3D PLOT ==================================")
                                            self.run_log_listWidget.addItem(f" Click <3D Plot> to visualize the model!")
                                        else:
                                            self.run_log_listWidget.addItem(f" Server filename: {server_filename} Successfully Saved! ")
                                        idx+=1
                                except:
                                    self.run_log_listWidget.addItem(f" Error server is not responding!")

                            else:
                                self.run_log_listWidget.addItem(f"LoopStructural did not execute successfull")
                        else:
                            pass
                
                else:
                    self.run_log_listWidget.addItem(f" The data is not running")                

            except:
                self.run_log_listWidget.addItem("Can't connection !!!!!")


    def run_map2loop(self):
        # run map2loop
        self.Run_Map2loop_pushButton.setEnabled(False)
        self.loop_docker_pushButton.setEnabled(True)
        self.loop_qgis_pushButton.setEnabled(True)

        # Extract map2loop value:
        map_base = int(self.base_lineedit.text())
        map_top = int(self.top_lineedit.text())
        map_minx = float(self.minx_lineedit.text())
        map_miny = float(self.miny_lineedit.text())
        map_maxx = float(self.maxx_lineedit.text())
        map_maxy = float(self.maxy_lineedit.text())

        self.bbox_3d = {
            "minx": map_minx,
            "miny": map_miny,
            "maxx": map_maxx,
            "maxy": map_maxy,
            "base": map_base,
            "top": map_top,
        }
        # Read the arg from text editors
        self.m2l_list_of_label = [
            self.min_fault_label,
            self.geol_sampler_label,
            self.f_sampler_label,
            self.sampler_decimator_label,
        ]
        # Set the value to the lineeditor
        self.m2l_list_of_input = [
            self.f_min_length_lineedit.text(),
            self.g_sampler_lineedit.text(),
            self.f_sampler_lineedit.text(),
            self.sampler_decimator_lineedit.text(),
        ]
        self.m2l_par_dict = fill_up_map2loop_parameters(
            self,
            m2l_list_of_label=self.m2l_list_of_label,
            m2l_list_of_input=self.m2l_list_of_input,
        )
       
        thicknes_calculator_selection = {"Interpolator function": self.thickness_calculator_comboBox.currentText()}
        self.m2l_par_dict ={**self.m2l_par_dict, **thicknes_calculator_selection }
        print(f" The selected m2l_par is {self.m2l_par_dict}")
        # Create an instance of Map2loopInQGIS
        self.run_log_listWidget.addItem(f"Running Map2loop in QGIS Backend.")
        run_m2l = Map2loopInQGIS(
            object_button=self.sender().text(),
            log_object=self.run_log_listWidget,
            m2l_par_dict=self.m2l_par_dict,
            config_param=self.config_param,
            bbox=self.bbox_3d,
        )
        run_m2l.map2loop_in_qgis()
        # Fill in the loop parameters
        self.regularisation_lineedit.setText("5")
        self.fault_nelts_lineedit.setText("1e4")
        self.foliation_nelts_lineedit.setText("1e5")

        return

    def save_preprocessed_data(self):
        # This function is used to save the preprocessed data with only selected table headers
        self.Run_Map2loop_pushButton.setEnabled(True)
        self.Run_Preprocessor_pushButton.setEnabled(False)
        self.save_all_config_parameters()
        self.save_geol_parameters()
        self.save_fault_parameters()
        self.save_struct_parameters()
        self.data_source_path = self.lineEdit_param_load_source_path.text().strip()
        self.data_source_dir = QDir(self.data_source_path)

        self.run_log_listWidget.addItem(
            f" Running now {self.sender().text()} QPushbutton"
        )
        self.preprocessor_label_list = [self.m2l_output_label, self.l2s_output_label]
        self.preprocessor_value_list = [
            self.m2l_output_lineedit,
            self.l2s_output_lineedit,
        ]
        self.processor_par_dict = fill_up_preprocessor_parameters(
            self,
            preproc_list_of_label=self.preprocessor_label_list,
            preproc_list_of_input=self.preprocessor_value_list,
            proc_Widgelist=self.run_log_listWidget,
        )

        extractor = ShapefileExtractorFromJSON(
            run_log_listWidget=self.run_log_listWidget,
            map2loop_button=self.Run_Map2loop_pushButton,
            output_folder_dict=self.processor_par_dict,
            json_path=self.data_source_dir,
            dtm_toggle=self.dtm_toggle,
        )

        # Get the data from json_file
        self.config_param = extractor.select_json_file()
        # load all process data:
        self.process_data_folder = Path(self.json_data_path).parent
        extractor.add_all_layers_from_directory(self.process_data_folder)
        # Add bbox_dict here
        if self.dtm_toggle == "QGIS":
            path_to_extract_top_base = self.lineEdit_dtm_path.text()
            # Consider when data is clipped
            minx, miny, maxx, maxy = extract_bbox(self, str(path_to_extract_top_base))
            # round the value
            minx, miny, maxx, maxy = (
                round(minx, 1),
                round(miny, 1),
                round(maxx, 1),
                round(maxy, 1),
            )

        elif self.dtm_toggle == "AUS":
            path_to_extract_top_base = self.geology_QLineEdit.text()
            bbox = get_shapefile_bounds(self, str(path_to_extract_top_base))
            minx, miny, maxx, maxy = (
                round(bbox["minx"], 1),
                round(bbox["miny"], 1),
                round(bbox["maxx"], 1),
                round(bbox["maxy"], 1),
            )
        else:
            pass
        # Base, Top, minX, minY, maxX and maxY append into map2loop feature
        self.base_lineedit.setText("-3200")
        self.top_lineedit.setText("1200")
        self.minx_lineedit.setText(str(minx))
        self.miny_lineedit.setText(str(miny))
        self.maxx_lineedit.setText(str(maxx))
        self.maxy_lineedit.setText(str(maxy))
        # Set the default value for sampling and decimation
        self.f_min_length_lineedit.setText("5000.0")
        self.g_sampler_lineedit.setText("200.0")
        self.f_sampler_lineedit.setText("200.0")
        self.sampler_decimator_lineedit.setText("2")
        # Consider also when data is clipped:
        return

    def fill_config_from_json(self):
        # return config parameters from the saved json file
        self.load_configdata_from_file_radioButton.setEnabled(False)
        self.lineEdit_dtm_path.setEnabled(True)
        json_handler = JSONDataPathHandler()
        self.json_data_path = json_handler.ensure_json_data_path()
        try:
            with open(self.json_data_path, "r") as file:
                data = json.load(file)
                self.lineEdit_param_load_source_path.setText(str(data["Input Folder"]))
                self.CRS_lineEdit_value.setText(str(data["CRS Output"]))
                self.lineEdit_dtm_path.setText(str(data["DTM path"]))

        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_geol_parameters(self):
        # this function return all the layers data as a dict
        self.saver_object = StateSaver(
            geology_combo_boxes=self.geology_combo_boxes,
            geology_param_boxes=self.geology_param_boxes,
            sill_QLineEdit=self.geology_sill_QLineEdit,
            intrusion_QLineEdit=self.geology_intrusion_QLineEdit,
            geology_QLineEdit=self.geology_QLineEdit,
        )
        try:
            # Save state current_state,
            self.json_data = self.saver_object.save_parameters()
            self.json_handler.add_data(self.json_data)
            self.geology_log_listWidget.addItem(
                "Geology config data successfully added into json."
            )
        except:
            self.show_message_box()
            self.SaveGeology_pushButton.setEnabled(True)

        return

    def save_struct_parameters(self):
        # this function return all the layers data as a dict
        self.saver_object = StructStateSaver(
            struct_combo_boxes=self.struct_combo_boxes,
            struct_param_boxes=self.struct_param_boxes,
            struct_bedding_QLineEdit=self.struct_bedding_QLineEdit,
            struct_overturned_QLineEdit=self.struct_overturned_QLineEdit,
            struct_line_edit=self.struct_QLineEdit,
        )
        try:
            # Save state current_state,
            self.json_data = self.saver_object.save_parameters()
            self.json_handler.add_data(self.json_data)
            self.struct_log_listWidget.addItem(
                "Structure config data successfully added into json."
            )

        except:
            self.show_message_box()
            self.SaveFault_pushButton.setEnabled(True)
        return

    def save_fault_parameters(self):
        # this function return all the layers data as a dict
        self.saver_object = FStateSaver(
            fault_combo_boxes=self.fault_combo_boxes,
            fault_param_boxes=self.fault_param_boxes,
            fault_ftext_QLineEdit=self.fault_ftext_QLineEdit,
            fault_fdipest_QLineEdit=self.fault_fdipest_QLineEdit,
            fault_line_edit=self.fault_QLineEdit,
        )
        try:
            # Save state current_state,
            self.json_data = self.saver_object.save_parameters()
            self.json_handler.add_data(self.json_data)

            self.fault_log_listWidget.addItem(
                "Fault config data successfully added into json."
            )
            self.run_log_listWidget.addItem("Config data successfully saved.")
            self.run_log_listWidget.addItem(
                "Now preprocess the data --> Click Preprocessor Button."
            )
        except:
            self.show_message_box()
            self.SaveFault_pushButton.setEnabled(True)
        return

    def show_message_box(self):
        # Create the message box
        QMessageBox.about(
            self,
            "Configuration Status",
            "Fill in the Configuration Tab",
        )

    def reset_widgets(self):
        """
        Function to reset widgets in a QGIS dialog.
        Args:
            dialog: The dialog containing the tab widget to reset
        """

        try:

            if self.tabWidget:
                print(f"Found tab widget in dialog")
                resetter = QtWidgetResetter(self.tabWidget)
                resetter.reset_all()
            else:
                print("No tab widget found in dialog")
        except Exception as e:
            print(f"Error resetting widgets: {str(e)}")

    def save_all_config_parameters(self):
        # This function is used to save the configuration files
        #self.Run_Preprocessor_pushButton.setEnabled(True)
        config_settings = SettingsDictionary()
        config_settings.add_multiple_mappings(
            {
                "Input Folder": self.lineEdit_param_load_source_path,
                "CRS Output": self.CRS_lineEdit_value,
                "DTM path": self.lineEdit_dtm_path,
            }
        )

        try:
            self.config_param = config_settings.create_dictionary()
            self.process_path = Path(self.config_param["Input Folder"])
            self.process_data_path = os.path.join(self.process_path, "process_data")
            self.json_data_path = str(self.process_data_path) + "/data.json"
            # # Create an instance of the class with the file path
            self.json_handler = JSONDataHandler(self.json_data_path)
            if self.roi_flag == "Rawdata_radioButton":
                self.config_param = self.config_param
                # Save initial data
                self.json_handler.save_data(self.config_param)
            else:
                # Merge the dictionaries
                self.config_param = {**self.config_param, **self.output_paths}
                # Save initial data
                self.json_handler.save_data(self.config_param)

        except ValueError as e:
            print(f"Error: {e}")
        return

    def select_dtm_path(self):
        # Select the dtm path and append it to the lineeditor
        self.conf_log_listWidget.addItem(
            f"DTM Layer Options:-->{self.sender().text()} RadioButton selected"
        )
        self.dtm_toggle = self.sender().text()
        dtm_selector = DTMPathSelector(
            config_log=self.conf_log_listWidget, line_edit=self.lineEdit_dtm_path
        )

        self.conf_AUS_radioButton.setEnabled(False)
        self.conf_JSON_radioButton.setEnabled(False)
        self.conf_QGIS_radioButton.setEnabled(False)
        self.lineEdit_dtm_path.setEnabled(True)
        if self.dtm_toggle == "QGIS":
            self.dtm_path = dtm_selector.update_line_edit()
        elif self.dtm_toggle == "AUS":
            self.dtm_path = "https://services.ga.gov.au/gis/services/Bathymetry_Topography/MapServer/WCSServer?request=GetCapabilities&service=WCS"
            self.lineEdit_dtm_path.setText(self.dtm_path)
            self.conf_log_listWidget.addItem(
                f"DTM file path extract from <Geoscience Australia> server"
            )
        else:

            self.dtm_path = "JSON path Upcoming soon"
            self.conf_log_listWidget.addItem(
                f"DTM file path extract from saved JSON configuration file"
            )

        return

    def load_folder_path(self):
        """
        This function selects and loads a folder path for input data configuration in a QGIS-based application.
        It performs the following tasks:

        1. **Disables a Radio Button**: Temporarily disables `load_configdata_from_json_radioButton`
           to prevent interference during folder selection.
        2. **Initializes Configuration Object**: Creates an instance of `Loop3dConfig`, which manages
           configuration settings and input data.
        3. **Selects Input Folder**: Calls `select_folder` to prompt the user to choose a folder, linking it
           to `lineEdit_param_load_source_path`.
        4. **Loads Data into QGIS**: Uses `load_data_in_qgis` to integrate the selected data into the QGIS environment.
        5. **Stores the Folder Path**: Saves the input folder path in a dictionary (`global_input_path`).
        6. **Handles CRS (Coordinate Reference System) Setup**: Initializes a `CRSAppender` instance and populates
           the QGIS CRS selection widget to ensure proper geospatial referencing.
        """

        self.conf_log_listWidget.addItem(
            f"Data Loading Options:--> {self.sender().text()} RadioButton selected"
        )
        self.load_configdata_from_json_radioButton.setEnabled(False)
        # Assign elements to Loop3d_Config attributes and create global input data folder
        self.config_folder_object = Loop3dConfig(config_log=self.conf_log_listWidget)
        self.input_folder_path = self.config_folder_object.select_folder(
            self.load_configdata_from_file_radioButton,
            self.lineEdit_param_load_source_path,
        )
        self.config_folder_object.load_data_in_qgis(self.input_folder_path)
        self.global_input_path = {"data_source_path:", self.input_folder_path}
        # Automated crs_object
        self.crs_object = CRSAppender()
        self.crs_object.populate_crs(self.CRS_QgsProjectionSelectionWidget)

        return

    def select_crs_value(self):
        # Slect the crs value in the combobox and set it to the its label
        self.crs_value = self.CRS_QgsProjectionSelectionWidget.crs().authid()
        self.global_crs_value = {"CRS:", self.crs_value}
        self.CRS_lineEdit_value.setText(str(self.crs_value))
        self.conf_log_listWidget.addItem(f"Selected CRS value: {self.crs_value}")
        return

    def checkbox_toggled(self):
        # Deal with all checkbox in populating data
        # ... other initialization code ...
        self.checkbox_handler = LayerCheckboxHandler(
            self,
            geology_log=self.geology_log_listWidget,
            fault_log=self.fault_log_listWidget,
            structure_log=self.struct_log_listWidget,
        )
        if (
            self.sender().objectName() == "geology_Qgis_checkBox"
            or self.sender().objectName() == "geology_json_checkBox"
        ):
            self.geology_log_listWidget.addItem(
                f"Geology Data Loading Options:--> {self.sender().text()} RadioButton selected"
            )
            self.geology_groupBox_5.setVisible(True)
            self.checkbox_handler.geology_on_checkbox_toggled()
        elif (
            self.sender().objectName() == "fault_Qgis_checkBox"
            or self.sender().objectName() == "fault_json_checkBox"
        ):
            self.fault_log_listWidget.addItem(
                f"Fault Data Loading Options:--> {self.sender().text()} RadioButton selected"
            )
            self.fault_groupBox_5.setVisible(True)
            self.checkbox_handler.fault_on_checkbox_toggled()
        elif (
            self.sender().objectName() == "struct_Qgis_checkBox"
            or self.sender().objectName() == "struct_json_checkBox"
        ):
            self.struct_log_listWidget.addItem(
                f"Structure Data Loading Options:--> {self.sender().text()} RadioButton selected"
            )
            self.struct_groupBox_5.setVisible(True)
            self.checkbox_handler.struct_on_checkbox_toggled()
        else:
            pass
        return

    def roi_clipping_processor(self):
        """
        Triggered the data processing to clip data
        """

        self.conf_log_listWidget.addItem(
            f"Data Clipping Options:--> {self.sender().text()} RadioButton selected"
        )
        self.roi_flag = self.sender().objectName()

        if self.roi_flag == "Rawdata_radioButton":

            self.clippeddata_radioButton.setEnabled(False)
            self.Rawdata_radioButton.setEnabled(False)
            msg_to_display = [
                "You're almost there! 🎉\n ",
                "Review all selection, make any necessary adjustments.",
                "To continue, go to the next Tabs to define further properties.",
            ]
            self.conf_log_listWidget.addItem(
                f"Data Clipping Status: NO --> Raw Data to be used for modelling"
            )
            self.conf_log_listWidget.addItem(
                "DTM selected and json config file created."
            )
            for display_string in msg_to_display:
                self.conf_shp_tif_listWidget.addItem(str(display_string))

        else:
            self.conf_log_listWidget.addItem(
                f"Data Clipping Status: YES --> Clipped Data to be used for modelling"
            )
            self.conf_log_listWidget.addItem(
                "DTM selected and json config file created."
            )
            self.Rawdata_radioButton.setEnabled(False)
            self.CreateROI_radioButton.setEnabled(True)
            self.ExistingROI_radioButton.setEnabled(True)
            self.clippeddata_radioButton.setEnabled(False)
            self.Ok_ClipLayer.setEnabled(False)

        return

    def on_roi_toggled(self):
        sender = self.sender()
        self.clippeddata_radioButton.setEnabled(False)
        self.CreateROI_radioButton.setEnabled(False)
        self.ExistingROI_radioButton.setEnabled(False)
        self.create_roi_flag = sender.text()
        if sender.text() == "Create ROI":  # Correct method
            self.save_roi.setEnabled(True)

            create_scratch_layer_and_activate_clipping(self, 0)
            self.save_roi.clicked.connect(self.create_save_roi_button)
        else:
            self.save_roi.setEnabled(False)
            self.Ok_ClipLayer.setEnabled(True)
            print(f"{sender.text()} is selected.")
            existing_roi_msg = self.config_folder_object.show_message_box(
                "Choose an Option: ", "QGIS Panel", "Local File"
            )
            if existing_roi_msg == QMessageBox.No:
                print(f"Load a local ROI file")
                self.selected_ROI_file_path = self.config_folder_object.select_file()
                self.config_folder_object.populate_list_widget(
                    self.conf_shp_tif_listWidget
                )

            else:
                print(f"QGIS Panel is selected")
                # Create the selector with your list widget
                roi_selector = RoishapefileSelector(self.conf_shp_tif_listWidget)
                # Add shapefile to list
                self.selected_ROI_file_path = roi_selector.append_to_list_widget()
                print(f" the path selected for ROI is {self.selected_ROI_file_path}")
                self.config_folder_object.populate_list_widget(
                    self.conf_shp_tif_listWidget
                )

    def create_save_roi_button(self):
        """
        Connects the save_roi function to an existing button
        """
        self.save_roi.setEnabled(False)
        roi_button = self.sender().text()
        if roi_button:
            self.config_folder_object.populate_list_widget(self.conf_shp_tif_listWidget)
            self.path_roi = save_roi_from_panel(self, self.input_folder_path)
        else:
            iface.messageBar().pushWarning(
                "Warning", f"Button '{roi_button}' not found"
            )

    def select_data_to_be_clipped(self):
        """
        return the dictionary of selected layer with key and value
        """
        # Disable clip function
        self.Ok_ClipLayer.setEnabled(False)
        # To get selected files as a dictionary
        self.selected_files_to_clip_dict = self.config_folder_object.create_file_dict(
            self.conf_shp_tif_listWidget
        )
        # Define input and output file paths
        self.input_paths = self.selected_files_to_clip_dict
        self.output_paths = self.config_folder_object.generate_clipped_paths(
            self.input_paths
        )
        if self.create_roi_flag == "Create ROI":
            print(f"Clipping using Created ROI")
            clipper = DataClipper(self.path_roi)
        else:
            print(f"Clipping using Existing ROI")
            clipper = DataClipper(self.selected_ROI_file_path)
        # Clip the data
        clipping_msg = clipper.clip_data(self.input_paths, self.output_paths)
        if str(clipping_msg) == "Done Clipping":
            self.clipped_path = os.path.join(self.input_folder_path, "clipped")
            self.config_folder_object.load_data_in_qgis(self.clipped_path)
            print(f"Clipped data successfully loaded into QGIS panel ")

        return

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
