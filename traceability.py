# Load both Excel files
database_file = r"C:\Users\Klaudia Gonciarz\Cocoasource SA\Cocoasource SA - Documents\Sustainability\EUDR\DATA COLLECTION\IVC\IVC_regster.xlsx"
received_file = r"C:\Users\Klaudia Gonciarz\OneDrive - Cocoasource SA\Traceability checks\FICHE D'ACCOMPAGNEMENTS FT 24-25.xlsx LOT 2352.xlsx"

# Read the Excel sheets into DataFrames
# Convert column names to lowercase for both files
database_df = pd.read_excel(database_file)
database_df.columns = database_df.columns.str.lower()

received_df = pd.read_excel(received_file)
received_df.columns = received_df.columns.str.lower()

# Extract only the 'farmer_id' column for comparison (case-insensitive check)
if 'farmer_id' in database_df.columns and 'farmer_id' in received_df.columns:
    # Convert farmer_id to lowercase to ignore case differences in the IDs
    database_farmers = database_df[['farmer_id']].drop_duplicates().apply(lambda x: x.str.lower())
    received_farmers = received_df[['farmer_id']].drop_duplicates().apply(lambda x: x.str.lower())

    # Find common farmer_ids (that exist in both files)
    common_data = pd.merge(received_farmers, database_farmers, on='farmer_id', how='inner')

    # Find farmer_ids that are in the received file but not in the database
    missing_data = pd.merge(received_farmers, database_farmers, on='farmer_id', how='outer', indicator=True)
    missing_data = missing_data[missing_data['_merge'] == 'left_only'].drop('_merge', axis=1)

    # Output the results
    print("Farmer IDs that exist in both files (common):")
    print(common_data)

    print("\nFarmer IDs that are in the received file but not in the database (missing):")
    print(missing_data)

    # Optionally, save the results to new Excel files
    common_data.to_excel('common_farmers.xlsx', index=False)
    missing_data.to_excel('missing_farmers.xlsx', index=False)
else:
    print("The 'farmer_id' column was not found in one or both files.")
