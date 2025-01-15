import pandas as pd

# Load both Excel files
database_file = r"C:\Users\Klaudia Gonciarz\Cocoasource SA\Cocoasource SA - Documents\Sustainability\EUDR\DATA COLLECTION\IVC\IVC_regster.xlsx"
received_file = r"C:\Users\Klaudia Gonciarz\OneDrive - Cocoasource SA\Traceability checks\FICHE D'ACCOMPAGNEMENTS FT 24-25.xlsx LOT 2352.xlsx"

# Read the Excel sheets into DataFrames
database_df = pd.read_excel(database_file)
database_df.columns = database_df.columns.str.lower()

received_df = pd.read_excel(received_file)
received_df.columns = received_df.columns.str.lower()

# Check for 'farmer_id' in both files
if 'farmer_id' in database_df.columns and 'farmer_id' in received_df.columns:
    # Normalize farmer_id: lowercase, strip spaces, drop duplicates
    database_farmers = database_df[['farmer_id']].drop_duplicates().apply(lambda x: x.str.lower().str.strip())
    received_farmers = received_df[['farmer_id']].drop_duplicates().apply(lambda x: x.str.lower().str.strip())

    # Compare IDs
    comparison = pd.merge(received_farmers, database_farmers, on='farmer_id', how='outer', indicator=True)
    common_data = comparison[comparison['_merge'] == 'both']
    missing_data = comparison[comparison['_merge'] == 'left_only']

    # Output the results
    print("\nComparison of IDs across files:")
    print(comparison)

    print("\nFarmer IDs that exist in both files (common):")
    print(common_data)

    print("\nFarmer IDs that are in the received file but not in the database (missing):")
    print(missing_data)

    # Optionally, save the results
    common_data.to_excel('common_farmers.xlsx', index=False)
    missing_data.to_excel('missing_farmers.xlsx', index=False)
else:
    print("The 'farmer_id' column was not found in one or both files.")
