from typing import Tuple, List, Any, Set
import streamlit as st
import os
from pandas import DataFrame
from streamlit.runtime.uploaded_file_manager import UploadedFile
from merge import execute_simple_merge
from file_management import read_file


def get_downloads_folder() -> str:
    if os.name == 'nt':
        return os.path.join(os.getenv('USERPROFILE'), 'Downloads')
    else:
        return os.path.join(os.path.expanduser('~'), 'Downloads')


def upload_files() -> List[UploadedFile]:
    uploaded_files = st.file_uploader("Choose files",
                                      type=["csv", "xls", "xlsx", "ods"],
                                      accept_multiple_files=True)
    return uploaded_files


def get_dataframes(uploaded_files: List[UploadedFile]) -> Tuple[List[DataFrame], List[str], Set[Any]]:
    dfs = []
    file_names = []
    all_columns = set()
    for uploaded_file in uploaded_files:
        try:
            df = read_file(uploaded_file.name)
            dfs.append(df)
            all_columns.update(df.columns.tolist())
            file_names.append(uploaded_file.name)
        except Exception as e:
            st.error(f"Error reading file {uploaded_file.name}: {e}")
            continue
    return dfs, file_names, all_columns


def preview_files(dataframes: List[DataFrame], file_names: List[str]) -> None:

    tabs = st.tabs(file_names)

    for i, tab in enumerate(tabs):
        with tab:
            st.write(f"Preview of {file_names[i]}")
            st.dataframe(dataframes[i].head(5))


def save_file(file_names: List[str], selected_columns: List[str]) -> None:
    file_format = st.selectbox("Select output file format", [".csv", ".ods", ".xls", ".xlsx"])
    downloads_folder = get_downloads_folder()
    output_file_name_with_format = f"merged{file_format}"
    output_file_name = os.path.join(downloads_folder, output_file_name_with_format)

    if st.button("Merge and save file"):
        try:
            output_file_name = execute_simple_merge(file_names, selected_columns, output_file_name)
            st.success(f"File saved successfully as {output_file_name}")
            st.write(f"Preview of merged file")
            st.dataframe(read_file(output_file_name).head(10))

        except Exception as e:
            st.error(f"Error merging and saving file: {e}")


def run_simple_merge(file_names: List[str], dfs: List[DataFrame], all_columns: Set[str]):
    selected_columns = []
    if dfs:
        sorted_columns = sorted(list(all_columns))
        selected_columns = st.multiselect("Select columns to merge on", list(sorted_columns))
    if selected_columns:
        save_file(file_names, selected_columns)
def main():
    dfs, file_names, all_columns = [], [], set()
    st.title("Multiple table sheet merge app")

    uploaded_files = upload_files()
    if uploaded_files:
        st.success("Files uploaded successfully!")
        dfs, file_names, all_columns = get_dataframes(uploaded_files)
        preview_files(dfs, file_names)
    run_simple_merge(file_names, dfs, all_columns)




if __name__ == "__main__":
    main()
