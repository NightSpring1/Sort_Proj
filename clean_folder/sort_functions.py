import os
import pathlib
import shutil
import re
from clean_folder.constants import EXTENSIONS, UNKNOWN


def find_filetype(list_of_file_paths: list, file_type: str) -> list:
    file_type_paths = []
    for file_path in list_of_file_paths:
        file_ext = re.search(r'(?:\.([^.]+))?$', file_path.name).group()
        selection_rule = file_ext.upper().endswith(EXTENSIONS[file_type])
        if selection_rule:
            file_type_paths.append(file_path)
    return file_type_paths


def check_destination_folders(path: pathlib.WindowsPath) -> None:
    if not path.joinpath(UNKNOWN).is_dir():
        os.mkdir(path.joinpath(UNKNOWN))
    for folder in EXTENSIONS:
        if not path.joinpath(folder).is_dir():
            os.mkdir(path.joinpath(folder))


def clean_empty_folders(path: pathlib.WindowsPath) -> None:
    for iter_folder in path.iterdir():
        if iter_folder.is_dir():
            clean_empty_folders(iter_folder)
            if not os.listdir(iter_folder):
                os.rmdir(iter_folder)


def move_files(list_of_files: list, destination_path: pathlib.WindowsPath, folder_name: str):
    destination_path = destination_path.joinpath(folder_name)
    for file_path in list_of_files:
        try:
            shutil.move(file_path, destination_path)
        except shutil.Error:
            resolve_same_name_error(file_path, destination_path)


def resolve_same_name_error(f_path: pathlib.WindowsPath, d_path: pathlib.WindowsPath) -> None:
    for j in range(1, 99):
        cut_name = file_name_separate(f_path.name)
        new_file_name = cut_name[0] + '_' + str(j) + cut_name[1]
        if not d_path.joinpath(new_file_name).is_file():
            f_path = f_path.rename(f_path.parent.joinpath(new_file_name))
            break
    shutil.move(f_path, d_path)


def file_name_separate(file_name: str):
    last_dot_index = file_name.rfind('.')
    if last_dot_index == -1:
        last_dot_index = len(file_name)
    return [file_name[:last_dot_index:], file_name[last_dot_index::]]
