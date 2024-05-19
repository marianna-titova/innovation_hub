import pandas as pd
from simple_merge_impl import (execute_simple_merge as impl_execute_simple_merge)


def execute_simple_merge(file_paths: list, columns: list, output_path: str) -> str:
    """Merges multiple files and saves the DataFrame to a file"""
    return impl_execute_simple_merge(file_paths, columns, output_path)
