import pandas as pd
from read_impl import (read_file as read_file_impl,
                       read_ods as read_ods_impl)
from save_impl import (save_file as save_file_impl,
                       save_ods as save_ods_impl)


def read_file(file_path: str) -> pd.DataFrame:
    """Reads a CSV/XLS/XLSX file and returns a DataFrame."""
    return read_file_impl(file_path)


def read_ods(file_path: str) -> pd.DataFrame:
    """Reads an ODS file and returns a DataFrame."""
    return read_ods_impl(file_path)


def save_file(output_path: str, data: pd.DataFrame) -> None:
    """Saves a DataFrame to a CSV/XLS/XLSX file."""
    save_file_impl(output_path, data)


def save_ods(output_path: str, data: pd.DataFrame) -> None:
    """Saves a DataFrame to an ODS file."""
    save_ods_impl(output_path, data)
