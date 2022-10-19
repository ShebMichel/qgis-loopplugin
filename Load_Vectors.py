#Michel Nzikou @UWA-MinEx CRC Perth, October 2022
## This function is needed to load vector layers
import os # This is is needed in the pyqgis console also
from qgis.core import QgsVectorLayer
from qgis.core import QgsProject
import glob
from qgis.utils import iface
import json
import io
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QComboBox,QLabel,QAction, QFileDialog, QMessageBox, QTreeWidgetItem

##########################################################
###### This function load Layers into a scroll down search
def shapeFileloader(file_list):
    for path_to_vector_layer in file_list:
        fn_path    = str(path_to_vector_layer)
        layer_name =str(fn_path.split('/')[-1].split('.')[0])
        ext=str(fn_path.split('.')[-1])
        if ext=='tif':
            vlayer = iface.addRasterLayer(fn_path,layer_name)
        else:
            vlayer = iface.addVectorLayer(fn_path,layer_name, "ogr")
    return 
###### This function generate Layer ID or it's column name 
def xLayerReader():
	mc = iface.mapCanvas()
	lyr= mc.currentLayer()
	#print('', lyr.name())
	#print('The active layer name is {}'.format(lyr.name()))
	layer_colnames = [ ]
	for field in lyr.fields():
	  layer_colnames.append(field.name())
	#print('The active col name is {}'.format(layer_colnames))
	return layer_colnames
###### This function create json file     
def create_json_file(data_path,data):
	try:
		to_unicode = unicode
	except NameError:
		to_unicode = str
	with io.open(str(data_path)+'/'+'data.json', 'w', encoding='utf8') as outfile:
		str_ = json.dumps(data,indent=4,sort_keys=True, separators=(',',':'),ensure_ascii=False)
		outfile.write(to_unicode(str_))
		return
