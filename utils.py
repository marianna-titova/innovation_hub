import pandas as pd


def rename_duplicate_columns(dfs):
    all_columns = []
    for df in dfs:
        all_columns.extend(df.columns)

    cols = pd.Series(all_columns)
    for dup in cols[cols.duplicated()].unique():
        count = 0
        for i in range(len(dfs)):
            new_columns = []
            for col in dfs[i].columns:
                if col == dup:
                    if count != 0:
                        new_columns.append(f"{col} ({count})")
                    else:
                        new_columns.append(col)
                    count += 1
                else:
                    new_columns.append(col)
            dfs[i].columns = new_columns
    return dfs


def find_matches(dfs, keywords, match_type):
    matched_dfs = []
    for df in dfs:
        if match_type == 'columns':
            for col in df.columns:
                if any(keyword.lower() in str(df[col].values).lower() for keyword in keywords):
                    matched_dfs.append(df[[col]])
        elif match_type == 'lines':
            mask = df.apply(
                lambda row: any(keyword.lower() in str(cell).lower()
                                for cell in row for keyword in keywords), axis=1)
            matched_dfs.append(df[mask])
    return pd.concat(matched_dfs, axis=1 if match_type == 'columns' else 0)


def find_columns_by_name(dfs, keywords):
    matched_columns = []
    for df in dfs:
        for col in df.columns:
            if any(keyword.lower() in col.lower() for keyword in keywords):
                matched_columns.append(df[[col]])
    return pd.concat(matched_columns, axis=1)
