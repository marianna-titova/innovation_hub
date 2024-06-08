from typing import List, Set
from pandas import DataFrame
from streamlit.runtime.uploaded_file_manager import UploadedFile
import streamlit as st
from merge import soph_merge_mode1
import os
from app_utils import get_downloads_folder
from file_management import save_file
import pandas as pd

def run_soph_merge_mode1(files: List[UploadedFile], dfs: List[DataFrame], all_columns: Set[str]) -> None:
    transpose_by = st.radio("Transpose by", ('columns', 'lines'))

    if transpose_by == 'columns':
        sorted_columns = sorted(list(all_columns))
        selected_columns = st.multiselect("Select columns to transpose", sorted_columns)
    else:
        max_rows = max(len(df) for df in dfs)
        selected_lines = st.multiselect("Select line numbers to transpose", list(range(max_rows)))

    save_to_separate_files = st.checkbox("Save to separate files")


    if st.button("Transpose and Save"):
        if transpose_by == 'columns' and selected_columns:
            transposed_dfs = [soph_merge_mode1(df[selected_columns], 'columns') for df in dfs]
        elif transpose_by == 'lines' and selected_lines:
            transposed_dfs = [soph_merge_mode1(df.iloc[selected_lines], 'lines') for df in dfs]
        else:
            st.error("Please select the columns/lines to transpose.")
            return

        if save_to_separate_files:
            for file, transposed_df in zip(files, transposed_dfs):
                output_file_name = os.path.join(get_downloads_folder(), f"transposed_{file.name}")
                save_file(output_file_name, transposed_df)
                st.success(f"File saved successfully as {output_file_name}")
        else:
            file_format = st.selectbox("Select output file format", [".csv", ".ods", ".xls", ".xlsx"])
            combined_df = pd.concat(transposed_dfs, ignore_index=True)
            output_file_name = os.path.join(get_downloads_folder(), f"transposed_combined{file_format}")
            save_file(output_file_name, combined_df)
            st.success(f"Combined file saved successfully as {output_file_name}")

        for transposed_df in transposed_dfs:
            st.write("Preview of transposed file")
            st.dataframe(transposed_df.head(10))

def run_soph_merge_mode2(files: List[UploadedFile], dfs: List[DataFrame], all_columns: Set[str]) -> None:
    pass

def run_soph_merge_mode3(files: List[UploadedFile], dfs: List[DataFrame], all_columns: Set[str]) -> None:
    pass