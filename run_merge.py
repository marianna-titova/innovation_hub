import streamlit as st
from merge import soph_merge_mode1, soph_merge_mode2
import os
from file_management import save_file
import pandas as pd
from app_utils import upload_files, get_dataframes, preview_files, get_downloads_folder


def run_soph_merge_mode1() -> None:
    dfs, file_names, all_columns = [], [], set()
    uploaded_files = upload_files()
    if uploaded_files:
        st.success("Files uploaded successfully!")
        dfs, file_names, all_columns = get_dataframes(uploaded_files)
        preview_files(dfs, file_names)

        transpose_by = st.radio("Transpose by", ('columns', 'lines'))

        if transpose_by == 'columns':
            sorted_columns = sorted(list(all_columns))
            selected_columns = st.multiselect("Select columns to transpose", sorted_columns)
            all_options = st.checkbox("Select all options")
            if all_options:
                selected_columns = sorted_columns
        else:
            max_rows = max(len(df) for df in dfs)
            selected_lines = st.multiselect("Select line numbers to transpose", list(range(max_rows)))
            all_options = st.checkbox("Select all options")
            if all_options:
                selected_lines = list(range(max_rows))

        save_to_separate_files = st.checkbox("Save to separate files")

        if st.button("Transpose and save"):
            if transpose_by == 'columns' and selected_columns:
                transposed_dfs = [soph_merge_mode1(df[selected_columns], 'columns') for df in dfs]
            elif transpose_by == 'lines' and selected_lines:
                transposed_dfs = [soph_merge_mode1(df.iloc[selected_lines], 'lines') for df in dfs]
            else:
                st.error("Please select the columns/lines to transpose.")
                return

            if save_to_separate_files:
                for file, transposed_df in zip(uploaded_files, transposed_dfs):
                    output_file_name = os.path.join(get_downloads_folder(), f"transposed_{file.name}")
                    save_file(output_file_name, transposed_df)
                    st.success(f"File saved successfully as {output_file_name}")
            else:
                file_format = st.selectbox("Select output file format", [".csv", ".ods", ".xls", ".xlsx"], key='mode1')
                combined_df = pd.concat(transposed_dfs, ignore_index=True)
                output_file_name = os.path.join(get_downloads_folder(), f"transposed_combined{file_format}")
                save_file(output_file_name, combined_df)
                st.success(f"Combined file saved successfully as {output_file_name}")

            for transposed_df in transposed_dfs:
                st.write("Preview of transposed file")
                st.dataframe(transposed_df.head(10))


def run_soph_merge_mode2() -> None:
    dfs, file_names, all_columns = [], [], set()
    uploaded_files = upload_files()
    if uploaded_files:
        st.success("Files uploaded successfully!")
        dfs, file_names, all_columns = get_dataframes(uploaded_files)
        preview_files(dfs, file_names)

        choose_entries_by = st.radio("I'm choosing", ('columns', 'lines'))

        selected_items = []
        if choose_entries_by == 'columns':
            sorted_columns = sorted(list(all_columns))
            selected_items = st.multiselect("Select columns to get names from", sorted_columns)
        else:
            max_rows = max(len(df) for df in dfs)
            selected_items = st.multiselect("Select line numbers to get names from", list(range(max_rows)))

        if selected_items:
            n = st.number_input("Start", min_value=0, max_value=len(selected_items) - 1, value=0)
            k = st.number_input("End", min_value=n, max_value=len(selected_items), value=len(selected_items))
            all_options = st.checkbox("Select all options")
            if all_options:
                n = k = None

            match_type = st.radio("I want to merge", (
                'columns named like any entry',
                'lines named like any entry'))

            file_format = st.selectbox("Select output file format", [".csv", ".ods", ".xls", ".xlsx"], key='mode2')
            output_file_name = os.path.join(get_downloads_folder(), f"merged_combined{file_format}")
            if st.button("Merge and Save"):
                combined_df = soph_merge_mode2(dfs, selected_items, match_type, choose_entries_by, n, k)
                if not combined_df.empty:
                    save_file(output_file_name, combined_df)
                    st.success(f"Combined file saved successfully as {output_file_name}")
                    st.write("Preview of merged file")
                    st.dataframe(combined_df.head(10))
                else:
                    st.error("Please select the columns/lines to merge.")


def run_soph_merge_mode3() -> None:
    pass
