#  Process different shapefiles
## Set the project path
- Tick off the box in front of ProjectPath to navigate between directories and select your project folder
- Then, the 

## Load geology (button 1) Layer into qgis workspace

- Click into (Load Geology Polygon Layer) to load the shapefile corresponding to your geology layer
- Once loaded, a msg will popup into the console label: Geology Layer is Loaded
- In the multiple combobox, indivual one will be filled with Layer columns names &
- Also a text label appear on top of QLineEditor for example for the top one, Enter sill text, while the botton will show (Enter intrusion text).
- Then, the user need to assign individual combo type to their valid input from the scroll down value
- for example Rocktype 1* --to -- rocktype1, Min Age* --to -- min_age_ma.
- If the Qlineeditor is left empty the default value such sill and intrusive is assigned.
- After every combobox selected, the user need to click (Save Layer Params) to save their geology parameters.
- A confirmation msg is then printed next to the Console label.

## Repeat the process for Fault Polyline (button 2) and Structure Point (button 4) Layers

- In this process, here the QLineEditor text will be different and also their positions as well once the layer is loaded.
- Save the params as described above

## Loading Fold Polyline(button 4) and Min Deposit Point(button 5) Layer

- In contrary to the 3 button described above, here the data are hard coded.
- The user should click the Load Default Fold Polyline/Min Dep Point Layer.
- Once clicked, the default params are saved into their associated variable.
- Then, a confirmation msg is then printed next to the Console label.

## Create json and/or Py script

- Once all the 5 QPush button have been used and all parameters saved.
- A single click to Create Json File will generate a json file with name data.json in your above ProjectPath
- Once Create Py Script is clicked, a python filename Run_test.py will be created and saved in the same directory.