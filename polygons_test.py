import pandas as pd
from fastkml import kml

k = kml.KML()

with open(r'C:\Users\Klaudia Gonciarz\OneDrive - Cocoasource SA\Polygons\Polygones Ahonto\Mapping Ahonto 2.kml', 'rb') as f:
    k.from_string(f.read())

placemark_data = []

# Function to extract geometries and `Superficie` value
def extract_geometries(features):
    for feature in features:
        if isinstance(feature, kml.Placemark):
            # Default values
            superficie = None

            # Extract `Superficie` from the placemark's ExtendedData
            if feature.extended_data:
                for schema_data in feature.extended_data.elements:
                    # Check if the element is `SchemaData` (ExtendedData can have various structures)
                    if schema_data.__class__.__name__ == 'SchemaData':
                        for simple_data in schema_data.data:
                            if simple_data['name'] == "Superficie":
                                superficie = simple_data['value']

            # Append the data with Name, Geometry, and Superficie
            placemark_data.append({
                'Name': feature.name,
                'Geometry': feature.geometry.to_wkt() if feature.geometry else None,
                'Superficie': superficie
            })
        elif isinstance(feature, kml.Folder):
            extract_geometries(feature.features())

# Extract data from the KML file
for feature in k.features():
    extract_geometries(feature.features())

# Output the data for verification
for placemark in placemark_data:
    print(placemark)

ahonto1 = pd.DataFrame(placemark_data)
ahonto1.drop_duplicates(inplace=True)
