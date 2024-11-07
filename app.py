import streamlit as st
import pandas as pd
from io import BytesIO

# Title for the Streamlit app
st.title('Farmer ID Comparison App')

# Sidebar for uploading the first Excel file (database)
database_file = st.file_uploader("Upload the database Excel file", type=["xlsx"])

# Sidebar for uploading the second Excel file (received)
received_file = st.file_uploader("Upload the received Excel file", type=["xlsx"])

# Check if both files are uploaded
if database_file is not None and received_file is not None:
    try:
        # Read both uploaded files into pandas DataFrames
        database_df = pd.read_excel(database_file)
        database_df.columns = database_df.columns.str.lower()

        received_df = pd.read_excel(received_file)
        received_df.columns = received_df.columns.str.lower()

# Convert farmer_id column to string and then to lowercase to avoid non-string issues
if 'farmer_id' in database_df.columns and 'farmer_id' in received_df.columns:
    # Ensure all values are strings, then apply .str.lower()
    database_farmers = database_df[['farmer_id']].drop_duplicates().astype(str).apply(lambda x: x.str.lower())
    received_farmers = received_df[['farmer_id']].drop_duplicates().astype(str).apply(lambda x: x.str.lower())

    # Continue with the rest of your code to find common and missing farmer IDs
    ...


            # Find common farmer_ids (that exist in both files)
            common_data = pd.merge(received_farmers, database_farmers, on='farmer_id', how='inner')

            # Find farmer_ids that are in the received file but not in the database
            missing_data = pd.merge(received_farmers, database_farmers, on='farmer_id', how='outer', indicator=True)
            missing_data = missing_data[missing_data['_merge'] == 'left_only'].drop('_merge', axis=1)

            # Display the results
            st.write("### Farmer IDs that exist in both files (common):")
            st.dataframe(common_data)

            st.write("### Farmer IDs that are in the received file but not in the database (missing):")
            st.dataframe(missing_data)

            # Provide download links for the results
            def to_excel(df):
                output = BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                df.to_excel(writer, index=False)
                writer.save()
                processed_data = output.getvalue()
                return processed_data

            # Download buttons for the results
            common_excel = to_excel(common_data)
            missing_excel = to_excel(missing_data)

            st.download_button(label="Download common farmer IDs", data=common_excel, file_name='common_farmers.xlsx')
            st.download_button(label="Download missing farmer IDs", data=missing_excel, file_name='missing_farmers.xlsx')

        else:
            st.error("The 'farmer_id' column was not found in one or both files.")
    except Exception as e:
        st.error(f"Error processing files: {str(e)}")
else:
    st.info("Please upload both Excel files.")
