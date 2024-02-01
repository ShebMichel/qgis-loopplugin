
# Welcome to qgis-loopplugin's plugin overview!
============================================

## Why loopplugin?

This plugin process various qgis layer such as a dtm raster, geology, fault and structure point layers.
These various layers can be loaded using 4 ways for the dtm, while the others in two options.

For example, we can load a dtm raster, using the following 4 Qcheckbox options:
  - **http**: if selected, the plugin generate a QLineeditor where the user will enter their own server address, then save it.
  - **File**: if selected, the plugin let you navigate to your local directory to select your file.
  - **Qgis**: if selected, the plugin generate a list of layer in which the user will have to select one.
  - **Aus** : if selected, the plugin will then select Geoscience Australia server address.

However, only **qgis** and **File** Qcheckbox options are active for the other type of layers.
Once a project directory and all layers with their Qcheckbox selected, a json and python files are created, and a processed data folder with only columns that are required for further calculations. 
All the outputs are then used as the input for map deconstruction (**run map2loop**) and/or for 3D modelling module(**LoopStructural**).

# 1. Environment Installation
## 1.1. Required
This plugin will requires the below dependencies: 
- QGIS version: 3.28.4-Firenze
- Qt version  : 5.15.3
- Python 3.9.5

Before you download this plugin, please execute the below code on your QGIS Python console.

```bash
  # Check if websocket module exist:
  try:
      import websockets
      print('websockets is available')
  except:
      subprocess.run('pip install websockets')
      print('websockets is not available')
```
If you have websocket installed, it is okay, otherwise, it will install it to your QGIS ENV PATH. 
Once done, you can follow on how to install loopplugin.

## 1.2. How to install **loopplugin**?
  You will need a python package manager, [see here](https://docs.anaconda.com/anaconda/install/index.html)), as well as Python ≥ 3.6.
  You can git clone this plugin from the Loop3D repository with the following link:
  [https://github.com/Loop3D/qgis-loopplugin](https://github.com/Loop3D/qgis-loopplugin)

  Click <a href="https://github.com/Loop3D/qgis-loopplugin/archive/refs/heads/master.zip">[Download]</a> the github repository. Then using zip install method, zip the folder and upload it to QGIS using the plugin manager.
  More details about installing qgis plugin can be found here: [https://plugins.qgis.org/](https://plugins.qgis.org/)  

# 2. How to run **loopplugin**?

If the plugin is availaible in QGIS plugin tabs launch it by clicking the Loop icon,
in case, it is not available, select then Loop Processor from the plugin menu/installed.


The hierarchy chart that show the functional plugin flow through a program-parts (modules) and how they are related is shown below:*
<p align="center">
<img src="https://github.com/ShebMichel/qgis-animated_gif/blob/main/plugin_structure_chart_v05.gif">
</p>


A usage example of the automated results after the geology layer is loaded:*
<p align="center">
<img src="https://github.com/ShebMichel/qgis-animated_gif/blob/main/plugin_launch_v05.gif"/>
</p>

# 3. Loading the layers and project directory

## 3.1. Setting the project path into qgis workspace

- Select the Project Directory:
   * Click the tool button (...) at the end of the QLineEdit widget.
   * Navigate between directories and select your project folder
   * Then, click Select Folder into the pop up window
   * Finally, the project directory is printed into the QLineEdit.

## 3.2. Loading a geology layer into qgis workspace

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

## 3.3. Repeat the process for Fault Polyline, Structure Point and DTM Layers

- Same process as the above.
- For dtm raster, only load the layer as described above.  
  click the Save Layer Params because the data is saved automatically. 

## 3.4. Loading Fold Polyline and Min Deposit Point Layer

- Hard coded for now..

# 4. Configuration File and processed data

- After the buttons **Geology**, **Fault**, **Structure** and **DTM** are all checked and also the **Project Directory** is defined, 
  click **Save Config File** to generate both "data.json" and "Run_test.py" in the newly created folder (process_source_data_timestamp) inside your Project Directory.
- Also inside the Project Directory, the output_data_timestamp folder, where the results of map2loop will locally be stored.
- The process_source_data contain the newly saved shapefile/geojson containing only the parameters selected during layer processing.
  These outputs are then used as input for map2loop or LoopStructural modelling engine. 

# 5. RUN map2loop (map deconstruction)
  In this feature, you have will have to select the environment in which your calculations will be running.
  
  Once you click **Run map2loop**, you will have to select one of the below options:
  
    * Yes : local server (i.e running docker locally)
    * No  : remote server(i.e running the calculation remotely)
    
    * Yes 
       * For local calculation, it is required to have Docker Desktop for window user. If not follow the link below to install and launch it
          Click <a href="https://www.docker.com/products/docker-desktop/">[Click and select to install]</a>
       * 1. For remote calculation, the output result are transferred to your local PC inside output_data.
  To do so, once Run map2loop is selected, a new pop-up window is poulated with the possibility of running locally or on a server your calculations.
  - Before using this feature, you need to clone/download map2loop-server repository and then run the server package (more details on the repository).
    To do so or to turn on the server, open the terminal in the root directory of this repository and run:  
   
  ```bash
   docker compose up --build
  ```
  
  Since your server is running, you can now process your data and build a map deconstruction, by sending the process data inside the container/server using websocket client. This is done by a single click of the module 'Run map2loop' once activated. 
   
  * Once you click Run Map2Loop, you will have to click the below options:
    Yes : remote calculation
    No  : locally running the calculation
  * For remote calculation, the output result are transferred to your local PC inside output_data.

# 5. Create your Region Of Interest (ROI)
 A clipping tool used to crop data and save it as a new layer. The new layer is saved as yourfilename_clip.shp
 Once ROI is pressed, if no layer is available on the Qgis layer panel, you will:
 * be prompted to load a layer from your local directory.
Once you have loaded your layers, by clicking ROI, the following happen:
 * A scratch template layer is generated and also the drwaing feature are toggle.
 * You need now to draw your ROI and continue by following the prompt from the plugin interface
 
 Once you click clipped_your_layer, all the loaded layer should be clipped and add to the panel.

### Future releases:

  * REQUIRED: This will be embedded during plugin installation into the next release.
  * LoopStructural.clicked.connect()
  * LoopUI.clicked.connect()
  * TomoFast.clicked.connect()
  * HelpU: A feature attached to the help function in which the user can upload their own library.
  * Verbose 1,2,3

