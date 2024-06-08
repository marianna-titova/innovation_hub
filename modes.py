
from run_merge import run_soph_merge_mode1, run_soph_merge_mode2, run_soph_merge_mode3

MERGE_MODES = {
    "simple": {
        "title": "Simple merge",
        "name": "simple merge",
        "description": "Merges multiple files combining selected columns together vertically.",
        "image": "static/simple_merge.png"
    },
    "sophisticated": {
        "title": "Sophisticated merge",
        "name": "sophisticated merge",
        "description": "A sophisticated merge which allows you to use advanced options for merging files.",
        "image": "static/sophisticated_merge.png"
    },
    "filter": {
        "title": "Filtering & sorting",
        "name": "filtering & sorting",
        "description": "Apply simple or sophisticated filtering and sorting algorithms to a single or multiple files.",
        "image": "static/filter.png"
    }
}


SOPHISTICATED_MERGE_MODES = {
    "mode1": {
        "title": "Transpose",
        "name": "transpose",
        "description": "This mode provides functionality to choose columns/lines and transpose them. If there are multiple files you can choose if you want to save all in one file or different.",
        "image": "static/sophisticated_merge.png",
        "function": run_soph_merge_mode1
    },
    "mode2": {
        "title": "Find by column entries",
        "name": "find by column entries",
        "description": "This mode provides functionality to choose one or multiple columns and to find all columns which names are in entries of chosen column(s).",
        "image": "static/sophisticated_merge.png",
        "function": run_soph_merge_mode2
    },
    "mode3": {
        "title": "Find columns by word",
        "name": "find columns by word",
        "description": "This mode provides functionality to choose all columns which name contains a word/number of the list.",
        "image": "static/sophisticated_merge.png",
        "function": run_soph_merge_mode3
    },
}
