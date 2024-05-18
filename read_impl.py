import pandas as pd
import os
from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P


def read_file(file_path: str) -> pd.DataFrame:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.csv':
        return pd.read_csv(file_path)
    elif ext in ['.xls', '.xlsx']:
        return pd.read_excel(file_path)
    elif ext == '.ods':
        return read_ods(file_path)
    else:
        print(f"Unsupported file extension: {ext}")
        return None


def read_ods(file_path: str) -> pd.DataFrame:
    doc = load(file_path)
    table = doc.spreadsheet.getElementsByType(Table)[0]

    rows = []
    for row in table.getElementsByType(TableRow):
        cells = row.getElementsByType(TableCell)
        cell_values = []
        for cell in cells:
            paragraphs = cell.getElementsByType(P)
            cell_value = ' '.join(
                [paragraph.firstChild.data for paragraph in paragraphs if paragraph.firstChild is not None])
            cell_values.append(cell_value)
        rows.append(cell_values)

    df = pd.DataFrame(rows)
    df.columns = df.iloc[0]
    df = df[1:]
    return df
