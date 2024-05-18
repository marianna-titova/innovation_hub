import pandas as pd
from simple_merge_impl import (merge_files as impl_merge_files,
                               execute_simple_merge as impl_execute_simple_merge)


def merge_files(file_paths: list, columns: list) -> pd.DataFrame:
    """Merges multiple files and returns merged dataframe"""
    return impl_merge_files(file_paths, columns)


def execute_simple_merge(file_paths: list, columns: list, output_path: str) -> None:
    """Merges multiple files and saves the DataFrame to a file"""
    impl_execute_simple_merge(file_paths, columns, output_path)
