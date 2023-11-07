#
# editTCXFile.py 
# Reads in a .tcx file from strava and replaces altitude change with the elevation value in each event record 
# 
import os 
import xmltodict  
import xml.etree.ElementTree as ET
import pandas as pd 
from datetime import datetime 

# inputs 
filename = 'Tread_Hour_1_of_2 - UPDATE.tcx'
 

# Read in XML data and parse out fields of interest 
input_tcx_file =  str(os.getcwd()) + '\\' + filename


# Establish output filename 
outputfilename = input_tcx_file.replace('.tcx','_adj.tcx')
output_tcx_file = outputfilename

# Parse the input TCX file
tree = ET.parse(input_tcx_file)
root = tree.getroot()

# Define the TCX namespace
namespace = {'ns': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}

# Find all trackpoints in the TCX file
trackpoints = root.findall(".//ns:Trackpoint", namespaces=namespace)

# Iterate through each trackpoint and replace altitude with elevation
for trackpoint in trackpoints:
    altitude_element = trackpoint.find(".//ns:AltitudeMeters", namespaces=namespace)
    if altitude_element is not None:
        elevation_element = trackpoint.find(".//ns:AltitudeMeters", namespaces=namespace)
        elevation = elevation_element.text
        altitude_element.text = elevation


# Clean up the string of encoding issues
# updated_xml_data = updated_xml_data.replace('ns0:','').replace('ns1:','').replace('ns2:','')

# Save the modified TCX data to a new file
tree.write(output_tcx_file)

print(f"TCX file with altitude replaced by elevation saved to {output_tcx_file}")
