import pandas as pd
from typing import List
from pandas import DataFrame


def soph_merge_mode1(data: DataFrame, by: str) -> DataFrame:
    if by == 'columns':
        return data.T
    elif by == 'lines':
        return data.T.reset_index().T.reset_index(drop=True)
    return data


def soph_merge_mode2(
        dfs: List[DataFrame],
        selected_items: List[int or str],
        match_type: str,
        choose_entries_by: str,
        n: int = None,
        k: int = None
) -> DataFrame:
    merged_dfs = []
    selected_entries = []

    for df in dfs:
        if choose_entries_by == 'columns':
            for col in selected_items:
                if col in df.columns:
                    selected_entries.extend(df[col].tolist())
        else:
            if max(selected_items) < len(df):
                selected_entries.extend(df.iloc[selected_items].values.flatten())

    selected_entries = selected_entries[n:k] if n is not None and k is not None else selected_entries

    if match_type == 'columns named like any entry':
        for df in dfs:
            matched_columns = [col for col in df.columns if col in selected_entries]
            merged_dfs.append(df[matched_columns])

    elif match_type == 'lines named like any entry':
        for df in dfs:
            matched_rows = df[df.iloc[:, 0].isin(selected_entries)]
            merged_dfs.append(matched_rows)

    combined_df = pd.concat(merged_dfs, ignore_index=True) if merged_dfs else pd.DataFrame()
    cleaned_df = pd.DataFrame({col: combined_df[col].dropna().reset_index(drop=True) for col in combined_df.columns})
    return cleaned_df
