from simple_merge_impl import (execute_simple_merge as impl_execute_simple_merge)
from typing import List
from sophisticated_merge_impl import (soph_merge_mode1 as soph_merge_mode1_impl,
                                      soph_merge_mode2 as soph_merge_mode2_impl)

from streamlit.runtime.uploaded_file_manager import UploadedFile
from pandas import DataFrame


def execute_simple_merge(files: List[UploadedFile], columns: List[str], output_path: str) -> str | None:
    """Merges multiple files and saves the DataFrame to a file"""
    return impl_execute_simple_merge(files, columns, output_path)


def soph_merge_mode1(data: DataFrame, by: str) -> DataFrame:
    return soph_merge_mode1_impl(data, by)


def soph_merge_mode2(
        dfs: List[DataFrame],
        selected_items: List[int or str],
        match_type: str,
        choose_entries_by: str,
        n: int = None,
        k: int = None
) -> DataFrame:
    return soph_merge_mode2_impl(dfs, selected_items, match_type, choose_entries_by, n, k)
