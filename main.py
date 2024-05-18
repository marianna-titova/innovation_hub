from merge import execute_simple_merge


def main():
    # file_names = input("Enter file names separated by commas: ").split(',')
    # file_names = [file.strip() for file in file_names]
    # columns = input("Enter column names separated by commas: ").split(',')
    # columns = [col.strip() for col in columns]
    # output_file = input("Enter output file name (available formats: csv, xls, xlsx): ").strip().lower()
    file_names = ["test1.ods", "test2.ods"]
    columns = ["test1", "test2"]
    output_file = "test_vert.ods"

    execute_simple_merge(file_names, columns, output_file)


if __name__ == "__main__":
    main()