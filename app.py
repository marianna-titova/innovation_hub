from typing import List, Set
import streamlit as st
import os
from pandas import DataFrame
from app_utils import save_file, upload_files, get_dataframes
from modes import MERGE_MODES


def preview_files(dataframes: List[DataFrame], file_names: List[str]) -> None:

    tabs = st.tabs(file_names)

    for i, tab in enumerate(tabs):
        with tab:
            st.write(f"Preview of {file_names[i]}")
            st.dataframe(dataframes[i].head(5))


def choose_merge_mode() -> str:
    css_path = os.path.join("static/styles.css")
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.markdown("<h3>Select merge mode</h3>", unsafe_allow_html=True)
    columns = st.columns(len(MERGE_MODES))
    selected_mode = None

    if 'toggle' not in st.session_state:
        st.session_state['toggle'] = {key: False for key in MERGE_MODES.keys()}

    for i, (mode_key, mode_info) in enumerate(MERGE_MODES.items()):
        with columns[i]:
            st.image(mode_info['image'], use_column_width=True)

            if st.button(f"Show description for {mode_info['name']}", key=f"toggle-{mode_key}"):
                st.session_state['toggle'][mode_key] = not st.session_state['toggle'][mode_key]

            if st.session_state['toggle'][mode_key]:
                st.markdown(f"<div class='merge-description'>{mode_info['description']}</div>", unsafe_allow_html=True)

            if st.button(f"Select {mode_info['name']}", key=mode_key, type="primary"):
                selected_mode = mode_key
                st.session_state['selected_mode'] = selected_mode

    if 'selected_mode' in st.session_state:
        selected_mode = st.session_state['selected_mode']
        st.markdown(f"<h4>{MERGE_MODES[selected_mode]['title']}</h4>",
                    unsafe_allow_html=True)
    return selected_mode


def run_simple_merge(file_names: List[str], dfs: List[DataFrame], all_columns: Set[str]):
    selected_columns = []
    if dfs:
        sorted_columns = sorted(list(all_columns))
        selected_columns = st.multiselect("Select columns to merge on", list(sorted_columns))
        all_options = st.checkbox("Select all options")

        if all_options:
            selected_columns = sorted_columns
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
        merge_mode = choose_merge_mode()
        if merge_mode == "simple":
            run_simple_merge(file_names, dfs, all_columns)
        elif merge_mode == "sophisticated":
            st.warning("Sophisticated merge is not yet implemented.")


if __name__ == "__main__":
    main()
