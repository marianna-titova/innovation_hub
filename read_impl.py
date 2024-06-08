import pandas as pd
from pandas import DataFrame
from typing import Tuple, List, Any, Set
import os
from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P
from streamlit.runtime.uploaded_file_manager import UploadedFile
import io
import streamlit as st


def read_file(file: UploadedFile | str) -> DataFrame | None:
    if isinstance(file, UploadedFile):
        ext = os.path.splitext(file.name)[1].lower()
        file_content = file.getvalue()
    else:
        ext = os.path.splitext(file)[1].lower()
        file_content = file

    if ext == '.csv':
        if isinstance(file, UploadedFile):
            return pd.read_csv(io.BytesIO(file_content))
        else:
            return pd.read_csv(file_content)
    elif ext in ['.xls', '.xlsx']:
        if isinstance(file, UploadedFile):
            return pd.read_excel(io.BytesIO(file_content))
        else:
            return pd.read_excel(file_content)
    elif ext == '.ods':
        return read_ods(file)
    else:
        st.error(f"Unsupported file extension: {ext}")
        return None

def read_ods(file: UploadedFile | str) -> DataFrame | None:
    from odf.opendocument import load
    from odf.table import Table, TableRow, TableCell
    from odf.text import P

    if isinstance(file, UploadedFile):
        file_bytes = io.BytesIO(file.getvalue())
    else:
        file_bytes = file

    doc = load(file_bytes)
    table = doc.spreadsheet.getElementsByType(Table)[0]
    if table is None:
        return None

    rows = []
    for row in table.getElementsByType(TableRow):
        cells = row.getElementsByType(TableCell)
        cell_values = []
        for cell in cells:
            paragraphs = cell.getElementsByType(P)
            cell_value = ' '.join([paragraph.firstChild.data for paragraph in paragraphs if paragraph.firstChild is not None])
            cell_values.append(cell_value)
        rows.append(cell_values)

    df = pd.DataFrame(rows[1:], columns=rows[0])
    return df

