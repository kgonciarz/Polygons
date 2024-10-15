import pandas as pd
from fastkml import kml

# Create a KML object
k = kml.KML()

# Open and read the KML file
with open(r'C:\Users\Klaudia Gonciarz\OneDrive - Cocoasource SA\Polygons\Polygons Ecakoog\bogoboua.kml', 'rb') as f:
    k.from_string(f.read())

# List to hold placemark data
placemark_data = []

# Function to recursively extract geometries and other data
def extract_geometries(features):
    for feature in features:
        if isinstance(feature, kml.Placemark):
            # Initialize a dictionary to hold the placemark information
            placemark_info = {
                'Farmer Name': None,
                'Geometry': None,
                'Size': None
            }

            # Extract ExtendedData (Farmer Name and Size)
            if feature.extended_data:
                for data in feature.extended_data.elements:
                    if data.name == 'Farmer Name':
                        placemark_info['Farmer Name'] = data.value
                    elif data.name == 'Size':
                        placemark_info['Size'] = data.value

            # Extract the geometry as WKT
            if feature.geometry:
                placemark_info['Geometry'] = feature.geometry.to_wkt()

            # Append the data to the list
            placemark_data.append(placemark_info)

        elif isinstance(feature, kml.Folder):
            # Recursively extract geometries from the folder
            extract_geometries(feature.features())


# Start extracting geometries from the top-level features
for feature in k.features():
    extract_geometries(feature.features())

# Create a DataFrame from the collected data
bogoboua = pd.DataFrame(placemark_data)