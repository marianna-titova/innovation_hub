import pandas as pd
from read_impl import (read_file as read_file_impl)
from save_impl import (save_file as save_file_impl)


def read_file(file_path: str) -> pd.DataFrame:
    """Reads a CSV/XLS/XLSX file and returns a DataFrame."""
    return read_file_impl(file_path)


def save_file(output_path: str, data: pd.DataFrame) -> str:
    """Saves a DataFrame to a CSV/XLS/XLSX file."""
    return save_file_impl(output_path, data)

