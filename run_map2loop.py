'''  
Michel Nzikou @UWA-MinEx CRC Perth, October 2022
This function load vector layers into the Qgis framework
'''

import pathlib
import subprocess,os
from qgis.utils import iface
from .client import client_main



def hide_map2loop_features(map2loop_qline_list,map2loop_label_list,flag):
    '''
    hide or unhide the map2loop qgis feature
    # map2loop_qline_list: list of qlineeditor
    # map2loop_label_list: list of the label ass
    # flag               : hide or unhide
    '''
    for label,qline in zip(map2loop_label_list,map2loop_qline_list):
        if flag==False:
            label.hide()
            qline.hide()
        elif flag==True:
            label.setVisible(True)
            qline.setVisible(True)
        else:
            pass
    return
            


def run_client(self,dir,hostname,username,port_number,config_param):
    '''
    This function run the client exchange process
    # dir         : local directory where the result data will be saved
    # hostname    : ip address of the remote server
    # username    : the user name or company/ department
    # port_number : the default port is 8000
    # config_param: the configuration parameters extracted from data processing
    '''
    client_main(self,username,hostname,port_number,config_param,dir)
    return 



def find_plugin_path(name, basepath=None):
    '''
    This function is used to find the file path and basename
    '''
    if not basepath:
      basepath = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(basepath, name)


