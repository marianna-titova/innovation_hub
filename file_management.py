from pandas import DataFrame
from read_impl import (read_file as read_file_impl)
from save_impl import (save_file as save_file_impl)


def read_file(file_path: str) -> DataFrame | None:
    """Reads a CSV/XLS/XLSX file and returns a DataFrame."""
    return read_file_impl(file_path)


def save_file(output_path: str, data: DataFrame) -> str:
    """Saves a DataFrame to a CSV/XLS/XLSX file."""
    return save_file_impl(output_path, data)

