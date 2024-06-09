import streamlit as st
import os
from app_utils import save_file_simple, upload_files, get_dataframes, preview_files
from modes import MERGE_MODES, SOPHISTICATED_MERGE_MODES


def choose_mode() -> str:
    css_path = os.path.join("static/styles.css")
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.markdown("<h3>Select merge mode</h3>", unsafe_allow_html=True)
    columns = st.columns(len(MERGE_MODES))
    selected_mode = None

    for i, (mode_key, mode_info) in enumerate(MERGE_MODES.items()):
        with columns[i]:
            st.image(mode_info['image'], use_column_width=True)
            st.markdown(f"<div class='merge-description'>{mode_info['description']}</div>", unsafe_allow_html=True)
            if st.button(f"Select {mode_info['title'].lower()}", key=mode_key, type="primary"):
                selected_mode = mode_key
                st.session_state['selected_mode'] = selected_mode

    if 'selected_mode' in st.session_state:
        selected_mode = st.session_state['selected_mode']
        st.markdown(f"<h3>{MERGE_MODES[selected_mode]['title']}</h3>", unsafe_allow_html=True)
    return selected_mode


def run_simple_merge() -> None:
    dfs, file_names, all_columns = [], [], set()
    uploaded_files = upload_files()
    if uploaded_files:
        st.success("Files uploaded successfully!")
        dfs, file_names, all_columns = get_dataframes(uploaded_files)
        preview_files(dfs, file_names)

        selected_columns = []
        if dfs:
            sorted_columns = sorted(list(all_columns))
            selected_columns = st.multiselect(
                "Select columns to merge on", list(sorted_columns),
                key='simple_select_columns')
            all_options = st.checkbox("Select all options", key='simple_select_all_options')
            if all_options:
                selected_columns = sorted_columns
        if selected_columns:
            save_file_simple(uploaded_files, selected_columns)


def run_sophisticated_merge() -> None:
    st.markdown("<h4>Select Sophisticated Merge Mode</h4>", unsafe_allow_html=True)
    selected_sophisticated_mode = None
    if 'selected_sophisticated_mode' in st.session_state:
        selected_sophisticated_mode = st.session_state['selected_sophisticated_mode']

    for mode_key, mode_info in SOPHISTICATED_MERGE_MODES.items():
        cols = st.columns([1, 2])
        with cols[0]:
            st.image(mode_info['image'], use_column_width=True)
            if st.button(f"Select {mode_info['name']}", key=f"soph_{mode_key}"):
                selected_sophisticated_mode = mode_key
                st.session_state['selected_sophisticated_mode'] = selected_sophisticated_mode
        with cols[1]:
            st.markdown(f"#### {mode_info['title']}")
            st.markdown(f"{mode_info['description']}")

    if selected_sophisticated_mode:
        selected_mode_info = SOPHISTICATED_MERGE_MODES[selected_sophisticated_mode]
        st.markdown(f"<h4>{selected_mode_info['title']}</h4>", unsafe_allow_html=True)
        mode_function = selected_mode_info['function']
        mode_function()


def run_filter() -> None:
    pass


def main():
    st.title("Multiple table sheet merge app")

    mode = choose_mode()
    if mode == "simple":
        run_simple_merge()
    elif mode == "sophisticated":
        run_sophisticated_merge()
    elif mode == "filter":
        run_filter()


if __name__ == "__main__":
    main()
