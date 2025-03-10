# QGIS Geological Data Processing Plugin

## Overview
This plugin provides a comprehensive workflow for managing and processing geological data within QGIS. It facilitates the preparation, configuration, and integration of geological, fault, and structural data for 3D geological modeling.

## Features
- Multiple data loading options (shapefile, DTM, JSON)
- Coordinate reference system management
- Digital Terrain Model (DTM) integration
- Geological formation mapping
- Fault data processing
- Structural point data handling
- Integration with Map2loop and LoopStructural for 3D modeling

## Tab Descriptions

### Configuration Tab
| Feature | Description |
|---------|-------------|
| Load Input Data | Select FILE (default) to load multiple shapefiles and DTM into QGIS or JSON to preload data from a saved file. |
| Select the CRS | Choose the reference coordinate system. Use CRS Selector to append the selected CRS to Output CRS. |
| Select the DTM | QGIS: Select a DTM file path. AUS: Fetch DTM from Geoscience Australia. JSON: Use preloaded DTM data. |
| Type of Data | Raw Data: Uses existing data from QGIS. Clip Data: Select/define a Region of Interest (ROI) and clip available data. |


### Geology Layer Tab
| Feature | Description |
|---------|-------------|
| Load Geology Data | Select QGIS (default) to fill the combobox with only geology file types, then select one and click OK. Use JSON to load from an existing data.json file from the Configuration Tab. |
| Link Your Header with the Right Parameters | Verify field mapping (e.g., Formation <----> unitname) and adjust if needed. |
| Use Your Geological Field Knowledge | Modify default values based on expertise and field observations. |


### Fault Layer Tab
| Feature | Description |
|---------|-------------|
| Load Fault Data | Select QGIS (default) to fill the combobox with only geology file types, then select one and click OK. Use JSON to load from an existing data.json file. |
| Link Your Header with the Right Parameters | Verify field mapping (e.g., Dip <----> dip) and adjust if needed. |
| Use Your Geological Field Knowledge | Modify default values based on expertise and field observations. |


### Structure Layer Tab
| Feature | Description |
|---------|-------------|
| Load Structure Point Data | Select QGIS (default) to fill the combobox with only geology file types, then select one and click OK. Use JSON to load from an existing data.json file. |
| Link Your Header with the Right Parameters | Verify field mapping (e.g., Dip <----> dip) and adjust if needed. |
| Use Your Geological Field Knowledge | Modify default values based on expertise and field observations. |


### Run Tab
| Feature | Description |
|---------|-------------|
| Save Configuration | - **m2l Output**: Type the name of your Map2loop output folder (default: `m2l_output`) <br>- **l2s Output**: Type the name of your LoopStructural output folder (default: `m2l_output`).<br>- Click <Save Configuration> to save all configuration parameters into data.json. |
| Preprocessor | Prepares and processes raw geological data and and create new shapefile data for modelling. Only the new field selected above will be saved in the new shape files.|
| Map2loop | Extracts and processes geological data from GIS sources. <br>- **Run MAP2LOOP parameters**:<br>- - Minimum Fault Length: Set the minimum length for faults (default: 5 km / 5000.0 m),
<br>- Geology Sampler Spacing: Define the sampling resolution for geological formations (default: 200.0 m),
<br>- Fault Sampler Spacing: Specify the sampling resolution for fault structures (default: 200.0 m), 
<br>- Base: map base value (default=-3200), 
<br>- Top: The elevation value (default=1200), 
<br>- MinX and MaxX: minimun and maximun X-value, 
<br>- MinY and MaxY: minimun and maximun Y-value. 
<br> These values are automatically populated, check and edit using your expertise. |
| LoopStructural | Used for 3D geological modeling, integrating structural and geological data. Select the following server <br>- DOCKER: Docker server, GCP: Google Cloud Server, AWS: Amazon Web Server, and AZURE: Microsoft Cloud Server. Choose the server availaible for your own case.|
| 3D PLOT | Used to visualize the result of loopStructural 3D modelling.|

## Server Environments
The Run tab supports multiple server environments:
- Docker 
 * For windows machine, you need to have Docker Desktop Launch
 * If using remote machine without Docker Desktop, clone the following (LINK goe here: ) and cd to the folder and run <docker compose up --build>
- GCP (Google Cloud Platform)
- AWS (Amazon Web Services)
- Azure (Microsoft Azure)

## Workflow
1. Configure input data and parameters in the Configuration Tab
2. Set up geological data in the Geology Layer Tab
3. Configure fault data in the Fault Layer Tab
4. Set up structural point data in the Structure Layer Tab
5. Run the processing workflow in the Run Tab

## Support
For issues or questions, please refer to the documentation or open an issue in this repository.

## Requirements
### Environment
- QGIS>=3.38.1 (Grenoble)
- Access to server environments (Docker, WSL, AWS, or Azure) for the Run module
- Install map2loop via OSGeo4W shell (pip install map2loop)
### Data
In order to run map2loop you will need the following input files:

1. Polygon shapefile containing your lithologies
2. LineString shapefile containing your linear features (e.g. faults)
3. Point data shapefile containing orientation data
4. Digital Terain Model (DTM)
