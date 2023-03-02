import sys
from pathlib import Path
from constants import EXTENSIONS, UNKNOWN


def get_root_path_from_arg():
    arg_path = sys.argv[1::]
    if len(arg_path) != 1:
        print(f"sort.py received {len(arg_path)} parameters. Expected 1.")
        sys.exit()
    path = Path(arg_path[0])
    print(path.absolute())
    if not path.is_dir():
        print(f'{path} is not a folder.')
        sys.exit()
    return path


def get_all_files(path, path_dest) -> list:
    list_of_files = []
    if path.is_file():
        list_of_files.append(path)
    else:
        for iter_path in path.iterdir():
            if iter_path in [path_dest.joinpath(s) for s in [*EXTENSIONS.keys()] + [UNKNOWN]]:
                continue
            list_of_files += get_all_files(iter_path, path)
    return list_of_files
