import pandas as pd
from typing import List
from pandas import DataFrame
from file_management import save_file, read_file
from streamlit.runtime.uploaded_file_manager import UploadedFile


def merge_files(file_objects: List[UploadedFile], columns: List[str]) -> DataFrame | None:
    data_frames = []

    for file_object in file_objects:
        try:
            df = read_file(file_object)
            if df is not None:
                for col in columns:
                    if col not in df.columns:
                        df[col] = pd.NA

                df = df[columns]
                data_frames.append(df)
        except Exception as e:
            print(f"Error reading {file_object.name}: {e}")

    if data_frames:
        merged_df = pd.concat(data_frames, ignore_index=True)
        cleaned_df = pd.DataFrame({col: merged_df[col].dropna().reset_index(drop=True) for col in merged_df.columns})
        return cleaned_df
    else:
        print("No files to merge")
        return None

def execute_simple_merge(file_objects: List[UploadedFile], columns: List[str], output_path: str) -> str | None:
    data = merge_files(file_objects, columns)
    if data is not None:
        return save_file(output_path, data)
    else:
        print("Exiting: No data to save")
        return None