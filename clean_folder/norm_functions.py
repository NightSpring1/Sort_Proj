from clean_folder import *
import os
import pathlib
import string

TRANS = {}
for cyr, lat in zip(CYRILLIC_SYMBOLS, TRANSLITERATION):
    TRANS[ord(cyr)] = lat
    TRANS[ord(cyr.upper())] = lat.upper()


def normalize(input_string: str) -> str:
    output_string = ''
    for i in input_string:
        if ord(i) in TRANS.keys():
            output_string += TRANS[ord(i)]
            continue
        elif i in string.ascii_letters + string.digits:
            output_string += i
            continue
        else:
            output_string += '_'
    return output_string


def normalize_files_in_folder(path: pathlib.WindowsPath) -> list:
    filenames = []
    for file in os.listdir(path):
        if path.joinpath(file).is_dir():
            continue
        cut_file = file_name_separate(file)
        normalized_file_name = normalize(cut_file[0]) + cut_file[1]
        try:
            path.joinpath(file).rename(path.joinpath(normalized_file_name))
            filenames.append(normalized_file_name)
        except FileExistsError:
            print(f'Error occurred during rename of {file}')
    return filenames
