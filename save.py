import pandas as pd
import os
from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P


def save_ods(output_path, data):
    from odf.opendocument import OpenDocumentSpreadsheet
    from odf.table import Table, TableRow, TableCell
    from odf.text import P

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

    # Add the data rows
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


def save_file(output_path, data):
    ext = os.path.splitext(output_path)[1].lower()
    if ext == '.csv':
        data.to_csv(output_path, index=False)
    elif ext in ['.xls', '.xlsx']:
        data.to_excel(output_path, index=False)
    elif ext == '.ods':
        save_ods(output_path, data)
    else:
        raise ValueError(f"Unsupported output file extension: {ext}")
    print(f"Merged file saved as {output_path}")