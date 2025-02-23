import pandas as pd
import os
import streamlit as st
from io import BytesIO

st.set_page_config(page_title="🧹📊 Data Sweeper", layout="wide")
st.title("🧹📊 Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualisation!")

uploaded_files = st.file_uploader("Upload your files (CSV or Excel): ", type=["csv", "xlsx"], accept_multiple_files= True)

if(uploaded_files):
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)

        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file.name}")
        continue

    st.write(f"**📄 File Name: ** {file.name}")
    st.write(f"**📏 File Size: ** {file.size/1024}")

    st.write("Preview the Head of the Dataframe")
    st.dataframe(df.head())

    st.subheader("🛠️ Data Cleaning Options")
    if st.checkbox(f"Clean Data for {file.name}"):
        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"Remove Duplicates from {file.name}"):
                df.drop_duplicates(inplace = True)
                st.write("Duplicates Removed")

        with col2:
            if st.button(f"Fill Missing Values for {file.name}"):
                numeric_cols = df.select_dtypes(include=["number"]).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.write("Missing Values have been Filled!")

        st.subheader("🎯 Select Columns To Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        st.subheader("📊 Data Visualisation")
        if st.checkbox(f"Show Visualisation for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])

        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()  # Creates in-memory buffer for file output
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)  # Save DataFrame as CSV in buffer
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine='openpyxl')  # Save as Excel using openpyxl
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)
            
            # Download button for the converted file
            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

        st.success("🎉 All files processed successfully!")