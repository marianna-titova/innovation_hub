from simple_merge_impl import (execute_simple_merge as impl_execute_simple_merge)
from typing import List


def execute_simple_merge(file_paths: List[str], columns: List[str], output_path: str) -> str | None:
    """Merges multiple files and saves the DataFrame to a file"""
    return impl_execute_simple_merge(file_paths, columns, output_path)
