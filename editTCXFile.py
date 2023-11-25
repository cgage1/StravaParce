#
# editTCXFile.py 
# Reads in a .tcx file from strava and replaces altitude change with the elevation value in each event record 
# 
import os 
import xmltodict  
import xml.etree.ElementTree as ET  # ET GUIDE: https://stackoverflow.com/questions/16419673/how-to-find-specific-elements-in-xml-using-elementtree 
import pandas as pd 
from datetime import datetime 

#--- input params ---# 
filename = 'Tread_Hour_1_of_2 - UPDATE.tcx'  # name of tcx file (do not include path)

#--------------------# 

# Read in XML data from current working directory 
input_tcx_file =  str(os.getcwd()) + '\\' + filename
tree = ET.parse(input_tcx_file)
root = tree.getroot()

# Establish output filename 
outputfilename = input_tcx_file.replace('.tcx','_adj.tcx')
output_tcx_file = outputfilename

# Define the TCX namespace (one default, one for extension data)
namespace = {'ns': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'} # this is the default namespace 
namespace_ext = {'ns': 'http://www.garmin.com/xmlschemas/ActivityExtension/v2'} # this is a namespace unique to the extension branches 

# Find all trackpoints in the TCX file
trackpoints = root.findall(".//ns:Trackpoint", namespaces=namespace)

# Iterate through each trackpoint and replace altitude with elevation
for trackpoint in trackpoints:
    altitude_element = trackpoint.find(".//ns:AltitudeMeters", namespaces=namespace)
    if altitude_element is not None:
        elevation_element = trackpoint.find(".//ns:Elevation", namespaces=namespace_ext)
        elevation = elevation_element.text
        altitude_element.text = elevation

# NEED TO Clean up the string of encoding issues
# updated_xml_data = updated_xml_data.replace('ns0:','').replace('ns1:','').replace('ns2:','') # issue with this approach is the namespaces get removed in some branches

# Save the modified TCX data to a new file
tree.write(output_tcx_file)
print(f"TCX file with altitude replaced by elevation saved to {output_tcx_file}")
