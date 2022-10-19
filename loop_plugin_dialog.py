# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Loop_pluginDialog
                                 A QGIS plugin
 This plugin preprocess shapefile inputs to generate python script and json file that are used as input for map2loop
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-10-13
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Michel M. Nzikou / CET - UWA
        email                : michel.nzikou@alumni.uleth.ca
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

#########
# Import the code for the DockWidget
import os
import sys
from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import QComboBox,QLabel,QAction, QFileDialog, QMessageBox, QTreeWidgetItem,QTextEdit,QVBoxLayout
from qgis.utils import iface
from qgis.core import QgsSettings
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont
#####
import os.path
from .Load_Vectors import shapeFileloader,xLayerReader,create_json_file
from .CreatePythonFile import create_a_python_file
from .Help_function import create_orientation_help
#

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'loop_plugin_dialog_base.ui'))


class Loop_pluginDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(Loop_pluginDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
### Toggle check box
        self.SearchFolder.setEnabled(False)
        ######
        self.Folder_checkBox.pressed.connect(self.select_folder)
        ################ add Geology and save its layer param into a list
        self.GeolButton.clicked.connect(self.create_geology_IdName)
        #self.Save_pushButton.clicked.connect(self.save_geol_IdName)

        #################   add Fault and save its layer param into a list 
        self.FaultButton.clicked.connect(self.create_fault_IdName)
        #self.Save_pushButton.clicked.connect(self.save_fault_IdName)
        ################# add struct and save its layer param into a list
        self.StructButton.clicked.connect(self.create_struct_IdName)
        #self.Save_pushButton.clicked.connect(self.save_struct_IdName)
        ################# Below we are pushing default data for Fold and Mineral Deposit Layer
        self.DTMButton.clicked.connect(self.saveDTM_path)
        ################# Create json file
        self.Json_pushButton.clicked.connect(self.createJson)    
        ################# Create py file
        self.CreatePyButton.clicked.connect(self.save_your_python_file) 
#**********************************************************************************************************
 ############################################################################################################       
    # ##### This function  select folder name/project name from it's folder
    def select_folder(self):
        foldername = QFileDialog.getExistingDirectory(self.Folder_checkBox, "Select folder ","",)
        self.SearchFolder.setText(foldername)
        self.Folder_checkBox.setChecked(True)
        return 
    ###### This function activate Layer into a qgis workspace and return the layer_name list (Col name of the table)
    def activate_layers(self):
        title = self.GeolButton.text()
        shape_file_list = []
        for shape_file in QFileDialog.getOpenFileNames(self, title):
            shape_file_list.append(shape_file)
        list_of_files     = shape_file_list[0]
        self.path_file    = list_of_files[0]
        colNames          = shapeFileloader(list_of_files)
        return colNames,self.path_file
#**********************************************************************************************************
############################################################################################################
    ### This function create Geology ID Name and for all combobox available
    ### X,Y .. defined the new position of the QLineEdit and Qlabel position when the Fault Layer is selected
    def create_geology_IdName(self): 
            p,self.GeolPath  = self.activate_layers()                                    ## This help select the shapefile
            if self.GeolButton.objectName()=='GeolButton':
                self.GeolPath= self.GeolPath
            geol_comboHeader = ['Formation*', 'Group*','Supergroup*', 'Description*', 'Fm code*', 'Rocktype 1*','Rocktype 2*','Polygon ID*','Min Age*','Max Age*']
            self.label_mover(geol_comboHeader)
            colNames         = xLayerReader()
            self.combo_column_appender(colNames,self.GeolButton.objectName())        # This code add element in combo items
            #self.label_replacer(geol_placeholder)      # This code changes 1st item of combo box
            ## The below section transform the label and QLineEditor and move it to X and Y
            self.QLine_and_Label_mover(320,210,320,230," Enter Sill Text:",self.Sill_Label,self.Sill_LineEditor)
            self.QLine_and_Label_mover(320,280,320,300," Enter Intrusion Text:",self.Intrusion_Label,self.Intrusion_LineEditor)
            ## The below write the 2 define string into two QLineEditor
            self.QLineEditor_default_string('sill','intrusive')
            self.Help_TextEdit.setText(self.list_of_infos[0])  ## This line is used to printout the help function
            self.Save_pushButton.clicked.connect(self.save_geol_IdName)
            return
############################################################################################################
    ### This function create fault ID Name and for the combobox 4=Dip Direction type* only ['num','alpha'] available
    ### X,Y .. defined the new position of the QLineEdit and Qlabel position when the Fault Layer is selected
    def create_fault_IdName(self):
            p,self.FaultPath       = self.activate_layers()                                    ## This help select the shapefile
            if self.FaultButton.objectName()=='FaultButton':
                self.FaultPath     = self.FaultPath
            fault_comboHeader      = ['Default Dip*', 'Dip Direction*','Feature*', 'Dip Direction type*', 'Fdipest*', 'Point ID*']
            colNames               = xLayerReader()
            self.label_mover(fault_comboHeader)
            self.combo_column_appender(colNames,self.FaultButton.objectName())                                        # This code add element in combo items
            ### Transform
            DipDirectionConv_colNames =['num','alpha']                                 # Empty label is set for the Header name
            self.cmbDescriptionLayerIDName.clear()                                     # Clear the Dip Direction Convention* box
            self.cmbDescriptionLayerIDName.addItems(DipDirectionConv_colNames)         # Clear the Dip Direction Convention* box
            #self.label_replacer(self.fault_comboHeader)                                     # This code changes 1st item of combo box
            ## The below section transform the label and QLineEditor and move it to X and Y
            self.QLine_and_Label_mover(320,180,320,200," Enter Fault Text:",self.Sill_Label,self.Sill_LineEditor)
            self.QLine_and_Label_mover(320,250,320,270," Enter fdipest Text:",self.Intrusion_Label,self.Intrusion_LineEditor)
            ## The below write the 2 define string into two QLineEditor
            self.QLineEditor_default_string('Fault','shallow,steep,vertical')
            self.clear_partially_combo_list(6)
            self.Help_TextEdit.setText(self.list_of_infos[0])           ## This line is used to printout the help function
            self.Save_pushButton.clicked.connect(self.save_fault_IdName)
            return
############################################################################################################
    ### This function create Structure Layer ID Name and for the combobox 4=Dip Direction convention* only ['Strike','Dip Direction'] available
    ### X,Y .. defined the new position of the QLineEdit and Qlabel position when the Fault Layer is selected
    def create_struct_IdName(self):
            p,self.StructPath      = self.activate_layers()                                   # This help select the shapefile
            if self.StructButton.objectName()=='StructButton':
                self.StructPath    =self.StructPath 
            struct_comboHeader     = ['Dip*', 'Dip Direction*','Feature*', 'Dip Dir Convention*', 'Overturned Field*', 'Point ID*']
            colNames               = xLayerReader()
            self.label_mover(struct_comboHeader)
            self.combo_column_appender(colNames,self.StructButton.objectName())
            ### Transform
            DipDirectionConv_colNames =['Strike','Dip Direction']                      # Empty label is set for the Header name
            self.cmbDescriptionLayerIDName.clear()                                     # Clear the Dip Direction Convention* box
            self.cmbDescriptionLayerIDName.addItems(DipDirectionConv_colNames)         # Clear the Dip Direction Convention* box
            #self.label_replacer(struct_comboHeader)                                     # This code changes 1st item of combo box
            ## The below section transform the label and QLineEditor and move it to X and Y
            self.QLine_and_Label_mover(320,180,320,200," Enter bedding Text:",self.Sill_Label,self.Sill_LineEditor)
            self.QLine_and_Label_mover(320,250,320,270," Enter Overturned Text:",self.Intrusion_Label,self.Intrusion_LineEditor)
            ## The below write the 2 define string into two QLineEditor
            self.QLineEditor_default_string('Bed','overturned')
            self.clear_partially_combo_list(6)
            self.Help_TextEdit.setText(self.list_of_infos[0])           ## This line is used to printout the help function
            self.Save_pushButton.clicked.connect(self.save_struct_IdName)
            return
#**********************************************************************************************************
############################################################################################################
    ###### This function save selected geology Layer ID name from the scrolldown and also entered value from the Qlineeditor
    def save_geol_IdName(self):
        self.my_combo_list       = self.combo_list() 
        if self.GeolButton.isEnabled(): 
            geol_data            = []           
            for i in range(10):
                geol_data.append(self.my_combo_list[i].currentText())
                self.my_combo_list[i].clear()
            self.Sill_input      = self.Sill_LineEditor.text()
            self.Intrusion_input = self.Intrusion_LineEditor.text()
            self.a_sill          = self.default_input(self.Sill_input,'sill')
            self.a_intrusion     = self.default_input(self.Intrusion_input,'intrusive')
            self.geol_data       = geol_data+[str(self.a_sill),str(self.a_intrusion)]
            self.Sill_LineEditor.clear()                                                 ## This line clear the QLineEditor text box
            self.Intrusion_LineEditor.clear()                                            ## This line clear the QLineEditor text box
            self.clear_all_label()
            self.Geology_checkBox.setChecked(True)
            self.GeolButton.setEnabled(False)                                            ### To deactivate the layer so that it can't be used in any other call
            self.Help_TextEdit.clear()
        return 
############################################################################################################
###### This function save fault Layer ID name into a scroll down search
    def save_fault_IdName(self):
        self.my_combo_list       = self.combo_list()
        if self.FaultButton.isEnabled():
            fault_data           = []
            for i in range(10):
                fault_data.append(self.my_combo_list[i].currentText())
                self.my_combo_list[i].clear()
            self.fault_input     = self.Sill_LineEditor.text()
            self.fdipest_input   = self.Intrusion_LineEditor.text()
            self.a_fault         = self.default_input(self.fault_input,'Fault')
            self.a_fdipest       = self.default_input(self.fdipest_input,'shallow,steep,vertical')
            self.fault_data      = fault_data[0:6]+[str(self.a_fault),str(self.a_fdipest)]  #
            self.Sill_LineEditor.clear()
            self.Intrusion_LineEditor.clear()
            self.clear_all_label()
            self.Fault_checkBox.setChecked(True)
            self.FaultButton.setEnabled(False)                                          ### To deactivate the layer so that it can't be used in any other call
            self.Help_TextEdit.clear()
        return
############################################################################################################
###### This function save Structure/Point Layer ID name into a scroll down search
    def save_struct_IdName(self):
        self.my_combo_list = self.combo_list()
        if self.StructButton.isEnabled():
            struct_data    = []
            for i in range(10):
                struct_data.append(self.my_combo_list[i].currentText())
                self.my_combo_list[i].clear()
            self.bedding_input     = self.Sill_LineEditor.text()
            self.overtune_input    = self.Intrusion_LineEditor.text()
            self.a_bedding         = self.default_input(self.bedding_input ,'Bed')
            self.a_overtune        = self.default_input(self.overtune_input,'overturned')
            self.struct_data       = struct_data[0:6]+[str(self.a_bedding),str(self.a_overtune)]
            self.Sill_LineEditor.clear()
            self.Intrusion_LineEditor.clear()
            self.Structure_checkBox.setChecked(True)
            self.clear_all_label()
            self.StructButton.setEnabled(False)          ### To deactivate the layer so that it can't be used in any other call
            self.Help_TextEdit.clear() 
        return 
############################################################################################################
    ##### This function save the DTM path and check the box once the file is selected.
    def saveDTM_path(self):
        p,self.DTMPath=self.activate_layers()                                   # This help select the shapefile
        if self.DTMButton.objectName()=='DTMButton':
                self.DTMPath=self.DTMPath 
        DTM_filename  = str(self.DTMPath)
        self.DTM_checkBox.setChecked(True)
############################################################################################################
    ###### This function is a purpose built to move both Qlabel and QLineEditor
    def QLine_and_Label_mover(self,X1,Y1,X2,Y2,msg1,label1,label2):
            self.dynamic_label(msg1,label1,X1,Y1)
            self.dynamic_QEditor(label2,X2,Y2)
#**********************************************************************************************************
############################################################################################################
    def createJson(self):
        try:
            ### Hard coded data for Min deposit and fold_data
            self.fold_data      = ['feature', 'Fold axial trace', 'type','syncline']
            self.mindeposit_data = ['site_code', 'short_name', 'site_type_','target_com','site_commo','commodity_','infrastructure']
            ###
            self.default_data     = [ 'volc', '0','No_col','500']  # Hard Coded default data
            self.Alldata          = self.geol_data+self.fault_data+self.struct_data+self.mindeposit_data+self.fold_data+self.default_data      
            geol_listKeys         = ['c','g','g2','ds','u','r1','r2','o-geol','min','max','sill','intrusive'] #o-geol is initially o
            fault_listKeys        = ['fdip','fdipdir','f','fdipdir_flag','fdipest','o','fault','fdipest_vals']    
            struct_listKeys       = ['d','dd','sf','otype','bo','gi','bedding','btype'] #o-struct is initially o 
            mindeposit_lisKeys    = ['msc','msn','mst','mtc','mscm','mcom','minf']
            fold_lisKeys          = ['ff','fold','t','syn']
            default_keys          = ['volcanic','fdipnull','n','deposit_dist']  # Hard Coded default data keys
            AllKeys               = geol_listKeys + fault_listKeys + struct_listKeys + mindeposit_lisKeys + fold_lisKeys + default_keys
            #print('self.Alldata:', self.Alldata)
            formation_data        = dict(zip(AllKeys, self.Alldata))
            json_path             = self.SearchFolder.text()
            ###
            try:
               create_json_file(json_path,formation_data)
               QMessageBox.about(self,"STATUS", "*****json file created*****")
            except:
                buttonReply = QMessageBox.question(self, 'OOPS Path Not Selected', "Do you want to continue?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        except:
            buttonReply = QMessageBox.question(self, 'OOPS Load all Layers', "Do you want to continue?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        return
############################################################################################################
     ###### This function change combo title based on the layer name
    def label_replacer(self,list_of_element):
        for id,replace_elt in enumerate(self.combo_list()):
            replace_elt.setItemText(0, list_of_element[id])
        return
############################################################################################################
     ###### This function append combo elt to all layer name
    def combo_column_appender(self,col_list,layerobject):
        for id,elt2 in enumerate(self.combo_list()):
            col_list, self.list_of_infos=create_orientation_help(col_list,id,layerobject)
            if not self.cmbFormationLayerIDName:
                elt2.addItems(col_list)
            else:
                elt2.addItems(col_list)  
        return
############################################################################################################
     ###### This function return a list combo elt 
    def combo_list(self):
        self.my_combo_list =[self.cmbFormationLayerIDName,self.cmbGroupLayerIDName,
                            self.cmbSupergroupLayerIDName,self.cmbDescriptionLayerIDName,
                            self.cmbFmLayerIDName, self.cmbRocktype1LayerIDName,
                            self.cmbRocktype2LayerIDName,self.cmbPointIDLayerIDName,
                            self.cmbMinAgeLayerIDName,self.cmbMaxAgeLayerIDName] 
        return self.my_combo_list
############################################################################################################
     ###### This function send default string into QLineEditor
    def QLineEditor_default_string(self,string1, string2):
        self.Sill_LineEditor.setText(str(string1))
        self.Intrusion_LineEditor.setText(str(string2))

############################################################################################################
    def default_input(self, value,input_tag):
        # This function return either empty QLineEdit string or the value typed in.
        value     =value
        input_tag =input_tag
        if not value:
            self.val =str(input_tag)
        else:
            self.val =value
        return self.val
############################################################################################################
    ## This function create dynamic label which is then move into X1,Y1 position
    def dynamic_label(self, Sill_Msg,label1,X1,Y1): #Sill_Msg is the message title on top op your QLineEditor
        label =label1                               #label1 is the name of the qt designer feature i.e self.Combobox, 
        label.setText(Sill_Msg)                     # X1,Y1 is the (x,y) coordinate of the feature into the MainWindow
        label.setFont(QFont("Sanserif",10))
        label1.move(X1,Y1)
############################################################################################################
    ## This function create dynamic QEditor which is then move into X1,Y1 position
    def dynamic_QEditor(self,label1,X1,Y1):
        label =label1
        label1.move(X1,Y1)
############################################################################################################
    ## This function clear the label associated with ComboBox 
    def clear_all_label(self):
        for i in range(len(self.label_list)):
            self.label_list[i].clear()
        self.Intrusion_Label.clear()
        self.Sill_Label.clear()
############################################################################################################
    ## This function create dynamic label which is then move into X1,Y1*idx position
    def label_mover(self,geol_comboHeader):
            self.label_list       = [self.moving_Label_1,self.moving_Label_2,self.moving_Label_3,self.moving_Label_4,self.moving_Label_5,self.moving_Label_6,self.moving_Label_7,self.moving_Label_8,self.moving_Label_9,self.moving_Label_10]
            for idx, combo_elt in enumerate(geol_comboHeader):
                      self.label_list[idx].setText(geol_comboHeader[idx])                     # X1,Y1 is the (x,y) coordinate of the feature into the MainWindow
                      self.label_list[idx].setFont(QFont("Sanserif",10))
                      if idx==len(geol_comboHeader)-1:
                        break
############################################################################################################
###### This function save Structure/Point Layer ID name into a scroll down search
    def clear_combo_list(self):
        self.my_combo_list =[self.cmbFormationLayerIDName,self.cmbGroupLayerIDName,
                    self.cmbSupergroupLayerIDName,self.cmbDescriptionLayerIDName,
                    self.cmbFmLayerIDName, self.cmbRocktype1LayerIDName,
                    self.cmbRocktype2LayerIDName,self.cmbPointIDLayerIDName,
                    self.cmbMinAgeLayerIDName,self.cmbMaxAgeLayerIDName]
        for i in range(10):
            self.my_combo_list[i].clear    
        return 

############################################################################################################
###### This function save clear partially combobox among the all 
    def clear_partially_combo_list(self,break_id):
            for i in reversed(range(10)):  
                self.my_combo_list[i].clear() 
                if i==break_id:
                   break
############################################################################################################
    def save_your_python_file(self):
        self.filepath     = self.SearchFolder.text()
        self.pyfilename   = 'Run_test'                     ##  This is the name of the python file created
        geology_filename  = str(self.GeolPath)
        fault_filename    = str(self.FaultPath)
        fold_filename     = str(self.FaultPath)
        structure_filename= str(self.StructPath)
        dtm_filename      = 'http://services.ga.gov.au/gis/services/DEM_SRTM_1Second_over_Bathymetry_Topography/MapServer/WCSServer?'
        metadata_filename = str(self.filepath)+'/'+'data.json'
        #mindep_filename   = 'http://13.211.217.129:8080/geoserver/loop/wms?service=WMS&version=1.1.0&request=GetMap&layers=loop%3Anull_mindeps'
        mindep_filename   = 'http://13.211.217.129:8080/geoserver/loop/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=loop:null_mindeps&bbox={BBOX_STR}&srs=EPSG:28350&outputFormat=shape-zip'
        overwrite         = 'true'
        verbose_level     = 'VerboseLevel.NONE'
        project_path      = str(self.filepath)
        working_projection= 'epsg:28350'
        # ### Here we define data2 paramas
        out_dir           =str(self.filepath)
        bbox_3d           ={'minx': 520000, 'miny': 7490000, 'maxx': 550000, 'maxy': 7510000, 'base': -3200, 'top': 1200}
        run_flags         ={'aus': True, 'close_dip': -999.0, 'contact_decimate': 5, 'contact_dip': -999.0, 'contact_orientation_decimate': 5, 'deposits': 'Fe,Cu,Au,NONE', 'dist_buffer': 10.0, 'dtb': '', 'fat_step': 750.0, 'fault_decimate': 5, 'fault_dip': 90.0, 'fold_decimate': 5, 'interpolation_scheme': 'scipy_rbf', 'interpolation_spacing': 500.0, 'intrusion_mode': 0, 'max_thickness_allowed': 10000.0, 'min_fault_length': 5000.0, 'misorientation': 30.0, 'null_scheme': 'null_scheme', 'orientation_decimate': 0, 'pluton_dip': 45.0, 'pluton_form': 'domes', 'thickness_buffer': 5000.0, 'use_fat': False, 'use_interpolations': False, 'fault_orientation_clusters': 2, 'fault_length_clusters': 2, 'use_roi_clip': False, 'roi_clip_path': ''}
        proj_crs          ='epsg:28350'
        clut_path         =''
        ### data4 is used to copy a specific file <map2loop.qgz> into a project path <proj.config.project_path+/>
        qgz_file          ='./source_data/map2loop.qgz'
        qgz_split_name    = qgz_file.split('/')[-1]
        #### Module_Import is the import module variable
        Module_Import     = 'from map2loop.project import Project \nfrom map2loop.m2l_enums import VerboseLevel \nimport shutil\n'
        #### project_config create a project with defined specific params
        project_config    = 'proj = Project(\n''                geology_filename='+"'"+str(geology_filename)+"'"+',''\n                fault_filename='+"'"+str(fault_filename)+"'"+',\n                fold_filename='+"'"+str(fold_filename)+"'"+',\n                structure_filename='+"'"+str(structure_filename)+"'"+',\n                mindep_filename='+"'"+str(mindep_filename)+"'"+',\n                dtm_filename='+"'"+str(dtm_filename)+"'"+',\n                metadata_filename='+"'"+str(metadata_filename)+"'"+',\n                overwrite='"'"+str(overwrite)+"'"+',\n                verbose_level=VerboseLevel.NONE'+',\n                project_path='+"'"+str(project_path)+"'"+',\n                working_projection='+"'"+str(working_projection)+"'"+',\n                )'
        #### project_update update the configuration files 
        project_update    = '\n \nproj.update_config(\n                    out_dir='+"'"+str(out_dir)+"'"+',\n                    bbox_3d='+str(bbox_3d)+',\n                    run_flags='+str(run_flags)+',\n                    proj_crs='+"'"+ str(proj_crs)+"'"+',\n                    clut_path='+"'"+str(clut_path)+"'"+',\n                )'
        #### project_run is used to run the proj
        project_run       = '\n \nproj.run()\n' 
        #### copy file qgz file into a different location
        proj_dest         = 'proj.config.project_path'
        qgz_move          = '/'+ str(qgz_split_name)
        copyqgzfile       = 'shutil.copyfile('+"'"+ str(qgz_file)+"'"+ ', '+str(proj_dest)+"+'"+ str(qgz_move)+"'"+ ')'
        #######################
        create_a_python_file(self.filepath,self.pyfilename,Module_Import,project_config,project_update,project_run,copyqgzfile)
        QMessageBox.about(self,"STATUS", "*****python file created*****")
###############################################################################################################################################################################