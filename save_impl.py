import pandas as pd
from pandas import DataFrame
import os
from odf.opendocument import OpenDocumentSpreadsheet
from odf.table import Table, TableRow, TableCell
from odf.text import P


def get_unique_file_name(output_path):
    base, ext = os.path.splitext(output_path)
    counter = 1
    new_output_path = output_path

    while os.path.exists(new_output_path):
        new_output_path = f"{base} ({counter}){ext}"
        counter += 1

    return new_output_path


def save_file(output_path: str, data: DataFrame) -> str | None:
    output_path = get_unique_file_name(output_path)
    ext = os.path.splitext(output_path)[1].lower()
    if ext == '.csv':
        data.to_csv(output_path, index=False)
    elif ext in ['.xls', '.xlsx']:
        data.to_excel(output_path, index=False, engine='openpyxl')
    elif ext == '.ods':
        save_ods(output_path, data)
    else:
        print(f"Unsupported output file extension: {ext}")
        return None
    print(f"Merged file saved as {output_path}")
    return output_path


def save_ods(output_path: str, data: DataFrame) -> None:
    doc = OpenDocumentSpreadsheet()
    table = Table(name="Sheet1")
    doc.spreadsheet.addElement(table)

    header_row = TableRow()
    table.addElement(header_row)
    for col in data.columns:
        cell = TableCell()
        header_row.addElement(cell)
        p = P(text=str(col))
        cell.addElement(p)

    for row in data.values.tolist():
        table_row = TableRow()
        table.addElement(table_row)
        for cell_value in row:
            cell = TableCell()
            table_row.addElement(cell)
            p = P(text=str(cell_value))
            cell.addElement(p)

    open(output_path, 'a').close()
    doc.save(output_path)
