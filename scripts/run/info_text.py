




# Function to transform JSON structure
def How_to_run_models(self, list_log_objects):
	# This function convert json dict to hjson one
	# Args: list_log_objects
	
	self.list_log_objects   = list_log_objects
    #

	self.config_instructions = {'instructions':["Configuration Tab",

	"The Configuration Tab comprises five key buttons for setting up input data and parameters:\n",

	"• Load Input Data",

	"Users can select either JSON or FILE.",

	"The default option is FILE, where users select the folder containing input data. This will load multiple shapefiles and DTM into QGIS.",

	"The JSON option should be used if a file has already been loaded before. This will preload data from a previously saved JSON file.\n",

	"• Select the CRS:",

	"Input CRS: Users select the reference coordinate system.",

	"CRS Selector: Click to append the selected input CRS to the Output CRS value.\n",

	"• Select the DTM:",

	"QGIS: Selects the DTM file path and appends it to the Path to DTM editor. If multiple DTMs are available in QGIS," 
	"a widget will populate buttons for selection, and once chosen, it appends the path accordingly.",

	"AUS: Connects to Geoscience Australia's server for DTM data.",

	"JSON: Uses preloaded DTM data from a JSON file.\n",

	"• Type of Data:",

	"Raw Data: Uses existing data from the QGIS panel and proceeds directly to step 5.",

	"Clip Data: Allows users to create or select a Region of Interest (ROI)." 
	"After selecting, a list of available data appears for users to choose which data to clip.\n",

	"• Save Configuration",

	"Saves all configuration parameters into a data.json file within the input folder.",
	" -------------------------------------INSTRUCTIONS END HERE-------------------------------------- \n"]
	}

	self.geol_instructions={'instructions':["Geology Layer Tab",

	"The Geology Tab comprises four key buttons for managing geological data: \n",

	"• Load Geology Data:",

	"Users can select either QGIS or JSON.",

	"The default option is QGIS, which fills the combobox with only geology file types. Users select one and click OK.",

	"The JSON option should be used if an existing data.json file is available from the Configuration Tab.",

	"This selection will fill: Geology file path in the editor,Data table and the combobox in section 2 and the Parameters in section 3.\n",

	"• Link Your Header with the Right Parameters:",

	"This section is pre-filled from the above selection.",

	"Users should verify whether the field mapping is correct. If not, they can manually adjust it, e.g., Formation <----> unitname.\n",

	"• Use Your Geological Field Knowledge:",

	"Users can change default values based on their own expertise and field observations.\n", 

	"• Save Configuration:",

	"Saves all configuration parameters into a data.json file within the input folder.",
	" -------------------------------------INSTRUCTIONS END HERE-------------------------------------- \n"]
	}

	self.fault_instructions={'instructions':["Fault Layer Tab",

	"The Fault Tab comprises four key buttons for managing fault data:\n",

	"• Load Fault Data:",

	"Users can select either QGIS or JSON.",

	"The default option is QGIS, which fills the combobox with only geology file types. Users select one and click OK.",

	"The JSON option should be used if an existing data.json file is available from the Configuration Tab.", 

	"This selection will fill: Fault file path in the editor, Data table and the combobox in section 2 and the Parameters in section 3.\n",

	"• Link Your Header with the Right Parameters:",

	"This section is pre-filled from the above selection.",

	"Users should verify whether the field mapping is correct. If not, they can manually adjust it, e.g., Dip <----> dip.\n",

	"• Use Your Geological Field Knowledge:",

	"Users can change default values based on their own expertise and field observations.\n", 

	"• Save Configuration:",

	"Saves all configuration parameters into a data.json file within the input folder.",
	" -------------------------------------INSTRUCTIONS END HERE-------------------------------------- \n"]
	}

	self.structure_instructions={'instructions':["Structure Layer Tab",

	"The Structure Tab comprises four key buttons for managing structure point data:\n",

	"• Load Structure Point Data:",

	"Users can select either QGIS or JSON.",

	"The default option is QGIS, which fills the combobox with only geology file types. Users select one and click OK.",

	"The JSON option should be used if an existing data.json file is available from the Configuration Tab.",

	"This selection will fill: Fault file path in the editor, Data table and the combobox in section 2 and the Parameters in section 3.\n",

	"• Link Your Header with the Right Parameters:",

	"This section is pre-filled from the above selection.",

	"Users should verify whether the field mapping is correct. If not, they can manually adjust it, e.g., Dip <----> dip.\n",

	"• Use Your Geological Field Knowledge:",

	"Users can change default values based on their own expertise and field observations.\n", 

	"• Save Configuration:",

	"Saves all configuration parameters into a data.json file within the input folder.",
	" -------------------------------------INSTRUCTIONS END HERE-------------------------------------- \n"]
	}

	self.run_instructions    = {'instructions':

	["Instruction Guide for Preprocessor, Map2loop, and LoopStructural:",
	"This module opens multiple server environments such as Docker, WSL, AWS, and Azure when activated.",
	"Once a server is selected, the Qt feature loads and displays specific configuration details for the chosen server environment.\n",
	
	"• Preprocessor:",

	"The Preprocessor module prepares and processes raw geological data before it is used in the Map2loop and LoopStructural modules.",

	"m2l Output: type the name of your map2loop output folder (The default is m2l_output)",

	"l2s Output: type the name of your LoopStructural output folder (The default is m2l_output). \n",

	"• Map2loop:",

	"Map2loop extracts and processes geological data from GIS sources to generate input parameters for LoopStructural.",

	"Enter Minimum Fault Length: Set the minimum length for faults to be considered. The default value is 5 km (5000.0 m).",

	"Choose Geology Sampler Spacing: Define the sampling resolution for geological formations. The default value is 200.0 m.",

	"Set Fault Sampler Spacing: Specify the sampling resolution for fault structures. The default value is 200.0 m.\n",

	"• LoopStructural:",

	"LoopStructural is used for 3D geological modeling, integrating structural and geological data.",

	" -------------------------------------INSTRUCTIONS END HERE-------------------------------------- \n"
	]

	}
	


	list_instructions=[self.config_instructions['instructions'],self.geol_instructions['instructions'],self.fault_instructions['instructions'],self.structure_instructions['instructions'],self.run_instructions['instructions'] ]

	for list_elt, obj_elt in zip(list_instructions,list_log_objects):
		for item in list_elt:
			obj_elt.addItem(str(item))
	return 
