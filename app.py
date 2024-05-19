import streamlit as st
import os
from merge import execute_simple_merge
from file_management import read_file


def get_downloads_folder():
    if os.name == 'nt':
        return os.path.join(os.getenv('USERPROFILE'), 'Downloads')
    else:
        return os.path.join(os.path.expanduser('~'), 'Downloads')


def main():
    st.title("Multiple table sheet merge app")

    uploaded_files = st.file_uploader("Choose files", type=["csv", "xls", "xlsx", "ods"], accept_multiple_files=True)

    if uploaded_files:
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

        if dfs:
            st.write("Files uploaded successfully!")
            tabs = st.tabs(file_names)

            for i, tab in enumerate(tabs):
                with tab:
                    st.write(f"Preview of {file_names[i]}")
                    st.dataframe(dfs[i].head(5))

            selected_columns = st.multiselect("Select columns to merge on", list(all_columns))

            if selected_columns:
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


if __name__ == "__main__":
    main()
