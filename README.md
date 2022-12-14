
# Welcome to qgis-loopplugin's plugin overview!
============================================

## Why loopplugin?

This plugin process various qgis layer such as a dtm raster, geology, fault and structure point layers.
These various layers can be loaded using 4 ways for the dtm, while the others in two options.

For example, we can load a dtm raster, using the following 4 options:
  - qgis: if selected, the plugin generate a list of layer in which the user will have to select one.
  - file: if selected, the plugin let you navigate to your local directory to select your file.
  - Aus : if selected, the plugin will then select Geoscience Australia server address.
  - Http: if selected, the plugin generate a QLineeditor where the user will enter their own server address, then save it.
However, only qgis and file options are active for the other type of layers.
Once all layers are processed, json file and python script are created and then used to run Map2Loop as well as LoopStructural(Loop project).

## How to install **loopplugin**?

  You can git clone this plugin from the Loop3D repository with the following link:
  [https://github.com/Loop3D/qgis-loopplugin](https://github.com/Loop3D/qgis-loopplugin)

  Click <a href="https://github.com/Loop3D/qgis-loopplugin/archive/refs/heads/master.zip">[Download]</a> the github repository. Then using zip install method, zip the folder and upload it to QGIS using the plugin manager.
  More details about installing qgis plugin can be found here: [https://plugins.qgis.org/](https://plugins.qgis.org/)  

## How to run **loopplugin**?


If the plugin is availaible in QGIS plugin tabs launch it by clicking the Loop icon,
in case, it is not available, select then Loop Processor from the plugin menu/installed.


The hierarchy chart that show the functional plugin flow through a program-parts (modules) and how they are related is shown below:*
<p align="center">
<img src="https://github.com/ShebMichel/qgis-animated_gif/blob/main/plugin_structure_chart.gif">
</p>


A usage example of the automated results after the geology layer is loaded:*
<p align="center">
<img src="https://github.com/ShebMichel/qgis-animated_gif/blob/main/launch_simulation.gif"/>
</p>


### Set the project path

- Select the Project Directory:
   * Click the tool button (...) at the end of the QLineEdit widget.
   * Navigate between directories and select your project folder
   * Then, click Select Folder into the pop up window
   * Finally, the project directory is printed into the QLineEdit.

### Load geology Layer into qgis workspace

- Click into Geology to load the geology shapefile
- Once loaded, automatically the multiple combobox will be filled with multiple variable names (Layer columns names).
-  ``` Check that the filled values are correctly selected in the combobox.```
- Also a text label appear on top of QLineEditor for example for the top one, Enter sill text, 
  while the botton will show (Enter intrusion text). In these QLineEditor, default values filled i.e sill=sill. However, you can rewrite the text that correspond to your geology attribute.

- For example:
   * Rocktype 1* --------> rocktype1 
   * Min Age*    --------> min_age_ma

- After every combobox selected, the user click (Save Layer Params) to save their geology  
  parameters.
- Once (Save layer Params) is clicked, individual parameter in the combobox is saved and this is 
	confirmed by the (Tick) button being selected.


<!--
<p align="center">
<img src="filter_geol_data.gif">
</p>
-->

### Repeat the process for Fault Polyline, Structure Point and DTM Layers

- Same process as the above.
- For dtm raster, only load the layer as described in the above 4 options. Note that, we wont
  click the Save Layer Params because the data is saved automatically. 

### Loading Fold Polyline and Min Deposit Point Layer

- Hard coded for now..

### Create json and/or Py script

- After the above is completed, click Save Config File to generate both "data.json" and "Run_test.py" in your Project Directory.
  These output are then later used as input for Map2loop/LoopStructural.



### Future releases:

  * ROI = Region of interest.. A polygon cliping tool which will be used to crop data and save it as a new layer.
  * HelpU: A feature attached to the help function in which the user can upload their own library. 
  * Verbose 1,2,3 
  * Map2loop/LoopStructural clicked.connect()

