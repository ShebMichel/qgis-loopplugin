#Michel Nzikou @UWA-MinEx CRC Perth, October 2022
####This function  create a help library:
#############################################################################################################
def create_orientation_help(col_list,id,layerobjectName):#(elt1, elt2, elt3):
    #Orientations                                       
    d_params             = ['dip','DIP','Dip','diP','INCLINATIO','DIp','INCLINATN','DiP']
    d_help_msg           = 'field that contains dip information'
    dd_params            = ["azimuth2",'AZIMUTH',"azimuth",'dip direction',"azimuth",'AZIMUTH_TR','AZIMUTH','AZIMUTH','STRIKE']
    dd_help_msg          = 'field that contains dip direction information'
    sf_params            = ['feature','FEATURE','codedescpt','ObsType','codedescpt','STRUCTURE_','DESCRIPT','SUB_TYPE','SUBFEATURE']
    sf_help_msg          = 'field that contains information on type of structure'
    bedding_params       = ['Bed','Strata','bedding','Bed','beding','beD','bEd']
    bedding_help_msg     =  'text to search for in field defined by sf code to show that this is a bedding measurement'
    otype_params         = ['dip direction','FeatureCodeDesc', 'strike']
    otype_help_msg       = 'flag to determine measurement convention (currently <strike> or <dip direction>)'
    bo_params            = ['structypei', 'NEWBGSVS2', 'deform','Blah','YOUNGING','DESCRIPT','No_col','ATTITUDE']
    bo_help_msg          = 'field that contains type of foliation'
    btype_params         = ['BEOI','Blah','Group_Suit','-','overturned','over']
    btype_help_msg       = 'text to search for in field defined by bo code to show that this is an overturned bedding measurement'
   
   #ids 
    o_params             = ['objectid','OBJECTID','unique_id','ID','No_col','GEOGRAPHIC']
    o_help_msg           = 'object id'
    gi_params            = ['gi','geopnt_id','OBJECTID','objectid','ID','FIELD_STRU','No_col','STATION_ID']
    gi_help_msg          = 'object id for structures'
  
  ## faults and folds
    fdip_params          = ['dip','CaptureScale','No_col','fixed']
    fdip_help_msg        = 'field for numeric fault dip value'
    fdipdir_params       = ['dip_dir','faultdipdi','DipDirection','No_col','0']
    fdipdir_help_msg     = 'field for text fault dip direction value' 
    ff_params            = ['feature','CATEGORY','codedescpt','Type','DESCRIPTIO','TYPE','FEATURETYP','FEATURE']
    ff_help_msg          = 'field that contains information on type of structure'
    fdipest_params       = ['dip_est','HWALL_ROSE','faultdipan','Dip','faultdipan','No_col','0']
    fdipest_help_msg     = 'field for text fault dip estimate value'
 
  ## stratigraphy   
    c_params             = ['unitname','FM_EQ_D','unit_name','LithDescn1','STRATNAME','SYMBOL','FORMATTED_','LABEL']
    c_help_msg           = 'field that contains finer stratigraphic coding'                                  
    g_params             = ['group_','MAX_PERIOD','sub_provin','Super_Grou','PARENTNAME','SUPERGROUP','No_col','MAX_AGE']
    g_help_msg           =  'field that contains coarser stratigraphic coding'
    g2_params            = ['supergroup','supersuite','Super_Grou','MAX_EPOCH','Formation_','PROVINCE','GRP','INTERPRETA','MIN_AGE']
    g2_help_msg          = 'field that contains alternate coarser stratigraphic coding if <g> is blank'
    ds_params            = ['descriptn','RANK','deposition','Symbol','STRATDESC','DESCRIPT','TEXT_DESCR','LITH_LIST']
    ds_help_msg          = 'field that contains information about lithology'
    u_params             = ['code','RCS','nsw_code','RockCatego','MAINUNIT','SYMBOL','ABBREVIATE','MAP_THEME']
    u_help_msg           = 'field that contains alternate stratigraphic coding (not used??)'
    r1_params            = ['rocktype1','RCS_ORIGIN','class','LithOther','No_col','RANK','LITH_LIST']
    r1_help_msg          = 'field that contains  extra lithology information'
    r2_params            = ['rocktype2','No_col','igneous_ty','dolerite','No_col','TYPE','GENESIS']
    r2_help_msg          = 'field that contains even more lithology information'
    sill_params          = ['sill','intrusive']
    sill_help_msg        = 'text to search for in field defined by ds code to show that this is a sill'
    intrusive_params     = ['granite','IGNEOUS','intrusive','volc','granit','Intrusion']
    intrusive_help_msg   = 'text to search for in field defined by r1 code to show that this is an intrusion'
    volcanic_params      = ['volcanic','volc','ID']
    volcanic_help_msg    = 'text to search for in field defined by ds code to show that this is an volv=canic (not intrusion)'

    #timing                                     
    min_params           = ['min_age_ma','MIN_TIME_Y','top_end_ag','AgeMin','top_end_ag','RELAGE','MINAGE','No_col', 'RM_AGE']
    min_help_msg         = 'field that contains minimum age of unit defined by ccode'
    max_params           = ['max_age_ma','MAX_TIME_Y','base_start','AgeMax','RELAGE','MAXAGE','No_col','RM_AGE']
    max_help_msg         = 'field that contains maximum age of unit defined by ccode'


    ################################################ Here we are dealing with Structure layer selection
    structure_label   = ['Dip*','Dip Direction*','Feature*','Dip Direction Convention*','Overturned Field*','Point ID*']
    if layerobjectName=='StructButton':
       # for idx,elt in enumerate(structure_label):
        if id==0:
            for idx,col_elt in enumerate(col_list):
                    for col_dir_params in d_params:
                        if col_elt==col_dir_params:                 
                            col_list.insert(0,col_list.pop(idx))
        elif id==1:
            for idx,col_elt in enumerate(col_list):
                    for col_dir_params in dd_params:
                        if col_elt==col_dir_params:                          
                            col_list.insert(0,col_list.pop(idx))
        elif id==2:
            for idx,col_elt in enumerate(col_list):
                    for col_dir_params in sf_params:
                        if col_elt==col_dir_params:                          
                            col_list.insert(0,col_list.pop(idx))
        elif id==4:
            for idx,col_elt in enumerate(col_list):
                    for col_dir_params in bo_params:
                        if col_elt==col_dir_params:                          
                            col_list.insert(0,col_list.pop(idx))
        elif id==5:
            for idx,col_elt in enumerate(col_list):
                    for col_dir_params in o_params:
                        if col_elt==col_dir_params:                          
                            col_list.insert(0,col_list.pop(idx))
        else:
                col_list = col_list

    ################################################ Here we are dealing with Fault layer selection
    fault_label       = ['Default Dip*', 'Dip Direction*','Feature*', 'Dip Direction type*', 'fdipest*', 'Point ID*']
    if layerobjectName=='FaultButton':
       # for idx,elt in enumerate(structure_label):
        if id==0:
            for idx,col_elt in enumerate(col_list):
                    for col_dir_params in fdip_params:
                        if col_elt==col_dir_params:                 
                            col_list.insert(0,col_list.pop(idx))
        elif id==1:
            for idx,col_elt in enumerate(col_list):
                    for col_dir_params in fdipdir_params:
                        if col_elt==col_dir_params:                          
                            col_list.insert(0,col_list.pop(idx))
        elif id==2:
            for idx,col_elt in enumerate(col_list):
                    for col_dir_params in ff_params:
                        if col_elt==col_dir_params:                          
                            col_list.insert(0,col_list.pop(idx))
        elif id==4:
            for idx,col_elt in enumerate(col_list):
                    for col_dir_params in fdipest_params:
                        if col_elt==col_dir_params:                          
                            col_list.insert(0,col_list.pop(idx))
        elif id==5:
            for idx,col_elt in enumerate(col_list):
                    for col_dir_params in o_params:
                        if col_elt==col_dir_params:                          
                            col_list.insert(0,col_list.pop(idx))
        else:
                col_list = col_list

    ################################################ Here we are dealing with Geology layer selection
    geol_label       = ['Formation*', 'Group*','Supergroup*', 'Description*', 'Fm code*', 'Rocktype 1*','Rocktype 2*','Polygon ID*','Min Age*','Max Age*']
    
    if layerobjectName=='GeolButton':
        if id==0:
            for idx,col_elt in enumerate(col_list):
                    for col_dir_params in c_params:
                        if col_elt==col_dir_params:                 
                            col_list.insert(0,col_list.pop(idx))

        elif id==1:
            for idx,col_elt in enumerate(col_list):
                    for col_dir_params in g_params:
                        if col_elt==col_dir_params:                 
                            col_list.insert(0,col_list.pop(idx))

        elif id==2:
            for idx,col_elt in enumerate(col_list):
                    for col_dir_params in g2_params:
                        if col_elt==col_dir_params:                 
                            col_list.insert(0,col_list.pop(idx))
        elif id==3:
            for idx,col_elt in enumerate(col_list):
                    for col_dir_params in ds_params:
                        if col_elt==col_dir_params:                 
                            col_list.insert(0,col_list.pop(idx))
#    ds_params
        elif id==4:
            for idx,col_elt in enumerate(col_list):
                    for col_dir_params in u_params:
                        if col_elt==col_dir_params:                 
                            col_list.insert(0,col_list.pop(idx))
        elif id==5:
            for idx,col_elt in enumerate(col_list):
                    for col_dir_params in r1_params:
                        if col_elt==col_dir_params:                 
                            col_list.insert(0,col_list.pop(idx))
        elif id==6:
            for idx,col_elt in enumerate(col_list):
                    for col_dir_params in r2_params:
                        if col_elt==col_dir_params:                 
                            col_list.insert(0,col_list.pop(idx))
        elif id==7:
            for idx,col_elt in enumerate(col_list):
                    for col_dir_params in o_params:
                        if col_elt==col_dir_params:                          
                            col_list.insert(0,col_list.pop(idx))
        elif id==8:
            for idx,col_elt in enumerate(col_list):
                    for col_dir_params in min_params:
                        if col_elt==col_dir_params:                          
                            col_list.insert(0,col_list.pop(idx))
        elif id==9:
            for idx,col_elt in enumerate(col_list):
                    for col_dir_params in max_params:
                        if col_elt==col_dir_params:                          
                            col_list.insert(0,col_list.pop(idx))
        else:
            col_list = col_list

    return col_list 
