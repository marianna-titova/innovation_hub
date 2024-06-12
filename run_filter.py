import streamlit as st
import pandas as pd
import os
from app_utils import upload_files, get_dataframes, preview_files, get_downloads_folder
from file_management import save_file


def rename_duplicate_columns(dfs):
    all_columns = []
    for df in dfs:
        all_columns.extend(df.columns)

    cols = pd.Series(all_columns)
    for dup in cols[cols.duplicated()].unique():
        count = 0
        for i in range(len(dfs)):
            new_columns = []
            for col in dfs[i].columns:
                if col == dup:
                    if count != 0:
                        new_columns.append(f"{col}_{count}")
                    else:
                        new_columns.append(col)
                    count += 1
                else:
                    new_columns.append(col)
            dfs[i].columns = new_columns
    return dfs


def find_matches(dfs, keywords, match_type):
    matched_dfs = []
    for df in dfs:
        if match_type == 'columns':
            for col in df.columns:
                if any(keyword.lower() in str(df[col].values).lower() for keyword in keywords):
                    matched_dfs.append(df[[col]])
        elif match_type == 'lines':
            mask = df.apply(
                lambda row: any(keyword.lower() in str(cell).lower()
                                for cell in row for keyword in keywords), axis=1)
            matched_dfs.append(df[mask])
    return pd.concat(matched_dfs, axis=1 if match_type == 'columns' else 0)


def run_filter_mode1() -> None:
    dfs, file_names, all_columns = [], [], set()
    uploaded_files = upload_files()
    if uploaded_files:
        st.success("Files uploaded successfully!")
        dfs, file_names, all_columns = get_dataframes(uploaded_files)
        print(dfs)
        dfs = rename_duplicate_columns(dfs)
        print(dfs)
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
