import streamlit as st
import os
from app_utils import upload_files, get_dataframes, preview_files, get_downloads_folder
from file_management import save_file
from utils import rename_duplicate_columns, find_matches


def run_filter_mode1() -> None:
    dfs, file_names, all_columns = [], [], set()
    uploaded_files = upload_files()
    if uploaded_files:
        st.success("Files uploaded successfully!")
        dfs, file_names, all_columns = get_dataframes(uploaded_files)
        dfs = rename_duplicate_columns(dfs)
        preview_files(dfs, file_names)

        match_type = st.radio("Choose type", ('columns', 'lines'))
        keywords_input = st.text_input("Enter words/collocations separated by commas")
        if keywords_input:
            keywords = [kw.strip() for kw in keywords_input.split(',')]
            if st.button("Find and merge"):
                combined_df = find_matches(dfs, keywords, match_type)
                if not combined_df.empty:
                    file_format = st.selectbox("Select output file format", [".csv", ".ods", ".xls", ".xlsx"],
                                               key='mode')
                    output_file_name = os.path.join(get_downloads_folder(), f"filtered{file_format}")
                    save_file(output_file_name, combined_df)
                    st.success(f"Combined file saved successfully as {output_file_name}")
                    st.write("Preview of merged file")
                    st.dataframe(combined_df.head(10))
                else:
                    st.error("No matches found with the given words/collocations.")
