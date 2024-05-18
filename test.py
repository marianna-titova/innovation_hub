import unittest
import pandas as pd
from merge import execute_simple_merge
from file_management import save_ods, read_ods, read_file


class TestMergeFilesVertically(unittest.TestCase):
    def setUp(self):
        self.csv_file = 'test1.csv'
        df_csv = pd.DataFrame({
            'a': [1, 2, 3],
            'b': [4, 5, 6]
        })
        df_csv.to_csv(self.csv_file, index=False)

        self.excel_file = 'test2.xlsx'
        df_excel = pd.DataFrame({
            'a': [7, 8, 9],
            'c': [10, 11, 12]
        })
        df_excel.to_excel(self.excel_file, index=False, engine='openpyxl')

        self.ods_file = 'test3.ods'
        df_ods = pd.DataFrame({
            'b': [13, 14, 15],
            'c': [16, 17, 18]
        })
        save_ods(self.ods_file, df_ods)

        self.file_paths = [self.csv_file, self.excel_file, self.ods_file]

    def test_merge_ods(self):
        columns = ['a', 'b']
        output_path = 'merged_output.ods'

        execute_simple_merge(self.file_paths, columns, output_path)

        expected_df = pd.DataFrame({
            'a': [1, 2, 3, 7, 8, 9],
            'b': [4, 5, 6, 13, 14, 15]
        })

        actual_df = read_ods(output_path)
        actual_df = actual_df.apply(pd.to_numeric, errors='coerce')
        pd.testing.assert_frame_equal(expected_df, actual_df)

    def test_merge_csv(self):
        columns = ['a', 'c']
        output_path = 'merged_output.csv'

        execute_simple_merge(self.file_paths, columns, output_path)

        expected_df = pd.DataFrame({
            'a': [1, 2, 3, 7, 8, 9],
            'c': [10, 11, 12, 16, 17, 18]
        })

        actual_df = read_file(output_path)
        actual_df = actual_df.apply(pd.to_numeric, errors='coerce')
        pd.testing.assert_frame_equal(expected_df, actual_df)

    def test_merge_excel(self):
        columns = ['a', 'b', 'c']
        output_path = 'merged_output.xls'

        execute_simple_merge(self.file_paths, columns, output_path)

        expected_df = pd.DataFrame({
            'a': [1, 2, 3, 7, 8, 9],
            'b': [4, 5, 6, 13, 14, 15],
            'c': [10, 11, 12, 16, 17, 18]
        })

        actual_df = read_file(output_path)
        actual_df = actual_df.apply(pd.to_numeric, errors='coerce')
        pd.testing.assert_frame_equal(expected_df, actual_df)


if __name__ == '__main__':
    unittest.main()