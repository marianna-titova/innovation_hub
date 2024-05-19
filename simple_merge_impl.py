import pandas as pd
from file_management import save_file, read_file

def merge_files(file_paths: list, columns: list) -> pd.DataFrame:
    data_frames = []

    for file_path in file_paths:
        try:
            df = read_file(file_path)
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
        cleaned_df = pd.DataFrame({col: merged_df[col].dropna().reset_index(drop=True) for col in merged_df.columns})

        return cleaned_df
    else:
        print("No files to merge")
        return None


def execute_simple_merge(file_paths: list, columns: list, output_path: str) -> str:
    data = merge_files(file_paths, columns)
    if data is not None:
            return  save_file(output_path, data)
    else:
        print("Exiting: No data to save")
        return None
