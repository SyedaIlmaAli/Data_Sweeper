import pandas as pd
import os
import streamlit as st
from io import BytesIO

# Set Streamlit Page Config
st.set_page_config(page_title="🧹📊 Data Sweeper", layout="wide")

# Main Title
st.markdown("<h1 style='text-align: center; color: #007bff;'>🧹📊 Data Sweeper</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Transform CSV & Excel files with built-in cleaning & visualization!</h4>", unsafe_allow_html=True)

# File Upload Section
st.sidebar.header("📂 Upload Your Files")
uploaded_files = st.sidebar.file_uploader("Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

# Process Uploaded Files
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        # Read the file based on extension
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.sidebar.error(f"❌ Unsupported file type: {file.name}")
            continue
        
        # Display File Info
        with st.expander(f"📄 File Details: {file.name}", expanded=True):
            st.write(f"**📝 File Name:** {file.name}")
            st.write(f"**📏 File Size:** {file.size / 1024:.2f} KB")
            st.write("### 🔍 Data Preview")
            st.dataframe(df.head())

        # Data Cleaning Section
        st.subheader("🛠️ Data Cleaning Options")
        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"🗑 Remove Duplicates ({file.name})"):
                df.drop_duplicates(inplace=True)
                st.success("✅ Duplicates Removed!")

        with col2:
            if st.button(f"📌 Fill Missing Values ({file.name})"):
                numeric_cols = df.select_dtypes(include=["number"]).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.success("✅ Missing Values Filled!")

        # Column Selection
        st.subheader("🎯 Column Selection")
        selected_columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]

        # Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"📈 Show Visualization ({file.name})"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # Conversion Options
        st.subheader("🔄 File Conversion")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"🔄 Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                output_file = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine="openpyxl")
                output_file = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            buffer.seek(0)
            
            # Download Button
            st.download_button(
                label=f"⬇️ Download {output_file}",
                data=buffer,
                file_name=output_file,
                mime=mime_type
            )

    st.success("🎉 All files processed successfully!")

