import pandas as pd
from typing import List
from pandas import DataFrame
from file_management import save_file, read_file


def soph_merge_mode1(data: DataFrame, by: str) -> DataFrame:
    if by == 'columns':
        return data.T
    elif by == 'lines':
        return data.T.reset_index().T.reset_index(drop=True)
    return data

def soph_merge_mode2():
    pass

def soph_merge_mode3():
    pass