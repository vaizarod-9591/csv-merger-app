import streamlit as st
import pandas as pd

st.title("📂 CSV Merger & UTF-8 Standardizer")
st.write("Upload your CSV files below to append them into a single, clean UTF-8 encoded file.")

# 1. Multi-file upload interface
uploaded_files = st.file_uploader("Choose CSV files", type="csv", accept_multiple_files=True)

if uploaded_files:
    dfs = []
    
    for file in uploaded_files:
        try:
            # Read CSV, letting pandas infer the original encoding
            df = pd.read_csv(file, encoding_type='utf-8', errors='replace')
            dfs.append(df)
            st.success(f"Successfully loaded: {file.name}")
        except Exception as e:
            st.error(f"Error reading {file.name}: {e}")

    if dfs:
        # 2. Append (concatenate) all dataframes together
        # ignore_index=True resets the row numbers to form a continuous index
        merged_df = pd.concat(dfs, ignore_index=True, sort=False)
        
        st.write("### Preview of Merged Data", merged_df.head())
        
        # 3. Convert dataframe to a UTF-8 CSV string
        # utf-8-sig is recommended as it includes a BOM (byte order mark) 
        # which prevents Excel from mangling non-ASCII characters on upload
        csv_data = merged_df.to_csv(index=False, encoding='utf-8-sig')
        
        # 4. Streamlit Download Button
        st.download_button(
            label="💾 Download Merged UTF-8 CSV",
            data=csv_data,
            file_name="merged_output_utf8.csv",
            mime="text/csv"
        )
