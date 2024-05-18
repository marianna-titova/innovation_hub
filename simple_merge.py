import pandas as pd
from save import save_file
from read import read_file


def merge_files(file_paths, columns):
    data_frames = []

    for file_path in file_paths:
        try:
            df = read_file(file_path, columns)
            if df is not None:
                for col in columns:
                    if col not in df.columns:
                        df[col] = pd.NA
                df = df[columns]
                data_frames.append(df)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    if data_frames:
        merged_df = pd.concat(data_frames, ignore_index=True)
        return merged_df
    else:
        print("No files to merge")
        return None


def execute_simple_merge(file_paths, columns, output_path):
    data = merge_files(file_paths, columns)
    if data is not None:
        save_file(output_path, data)
    else:
        print("Exiting: No data to save")
