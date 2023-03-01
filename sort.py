import sys
import os
import shutil
import string
import pyunpack
from pathlib import Path
from pyunpack import Archive

FOLDERS_EXTENSIONS = {'archives': ('ZIP', 'GZ', 'TAR', 'RAR', '7Z'),  # archives folder should not be renamed
                      'video': ('AVI', 'MP4', 'MOV', 'MKV'),
                      'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
                      'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
                      'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
                      'origin': ('OPJ',)}  # Example how to add folder with only one extension.
# Any amount of folders could be added to the dict. Extensions should be added in UPPER case.
# No extension files could be added as ''.

FOLDER_UNKNOWN = 'unknown'  # Name of folder, where all unknown files will be moved
CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLITERATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t",
                   "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}
for cyr, lat in zip(CYRILLIC_SYMBOLS, TRANSLITERATION):
    TRANS[ord(cyr)] = lat
    TRANS[ord(cyr.upper())] = lat.upper()


def get_path_from_arg():
    """
    Function checks if the script received only one argument, then verifies if
    an argument is an existing folder and returns the path.
    """
    arg_path = sys.argv[1::]
    if len(arg_path) != 1:
        print(f"sort.py received {len(arg_path)} parameters. Expected 1.")
        exit()
    path = Path(arg_path[0])
    if not path.is_dir():
        print(f'{path} is not a folder.')
        exit()
    return path


def get_all_files(path, destination_folders=False) -> list:
    """
    Returns all file paths in the folder. Ignores folders from FOLDERS_EXTENSIONS keys dict.
    If destination_folders=True, returns file ONLY form FOLDERS_EXTENSIONS keys dict.
    """
    list_of_files = []
    if path.is_file():
        list_of_files.append(path)
    else:
        for iter_path in path.iterdir():
            if iter_path in [root_dir.joinpath(s) for s in [*FOLDERS_EXTENSIONS.keys()] + [FOLDER_UNKNOWN]]:
                if destination_folders:
                    list_of_files += get_all_files(iter_path)
                else:
                    continue
            else:
                if destination_folders:
                    continue
                else:
                    list_of_files += get_all_files(iter_path)
    return list_of_files


def check_destination_folders(path) -> None:
    """
    Checks if all destination folders exist, if they don't, create them.
    """
    if not path.joinpath(FOLDER_UNKNOWN).is_dir():
        os.mkdir(path.joinpath(FOLDER_UNKNOWN))
    for folder in FOLDERS_EXTENSIONS:
        if not path.joinpath(folder).is_dir():
            os.mkdir(path.joinpath(folder))


def sort_all_files(paths: list, path) -> list:
    """
    Believe me, it works!!
    """
    sort_stats = [set(()), set(()), 0, 0]
    for file_path in paths:
        last_dot_index = file_path.name.rfind('.')
        if last_dot_index == -1:
            last_dot_index = len(file_path.name)
        file_ext = file_path.name[last_dot_index + 1::].upper()
        for folder in FOLDERS_EXTENSIONS:
            if file_ext not in sum(FOLDERS_EXTENSIONS.values(), ()):  # all extensions that script knows
                sort_stats[0].add(file_ext)
                sort_stats[2] += 1
                new_file_name = file_path.name
                for j in range(1, 99):
                    if not path.joinpath(FOLDER_UNKNOWN + '\\' + new_file_name).is_file():
                        if new_file_name != file_path:
                            file_path = file_path.rename(file_path.parent.joinpath(new_file_name))
                        shutil.move(file_path, path.joinpath(FOLDER_UNKNOWN))
                        break
                    else:
                        new_file_name = insert(file_path.name, '_' + str(j), last_dot_index)
                break
            elif file_ext in FOLDERS_EXTENSIONS[folder]:
                sort_stats[1].add(file_ext)
                sort_stats[3] += 1
                new_file_name = file_path.name
                for j in range(1, 99):
                    if not path.joinpath(folder + '\\' + new_file_name).is_file():
                        if new_file_name != file_path:
                            file_path = file_path.rename(file_path.parent.joinpath(new_file_name))
                        shutil.move(file_path, path.joinpath(folder))
                        break
                    else:
                        new_file_name = insert(file_path.name, '_' + str(j), last_dot_index)
                break
    for i in range(0, 2):
        if len(sort_stats[i]) == 0:
            sort_stats[i] = None
    return sort_stats


def insert(source_str, insert_str, pos):
    return source_str[:pos] + insert_str + source_str[pos:]


def clean_empty_folders(path):
    for iter_folder in path.iterdir():
        if iter_folder.is_dir():
            clean_empty_folders(iter_folder)
            if not os.listdir(iter_folder):
                os.rmdir(iter_folder)


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


def normalize_files(paths_of_files) -> None:
    for file in paths_of_files:
        if file.parent == root_dir.joinpath(FOLDER_UNKNOWN):
            continue
        last_dot_index = file.name.rfind('.')
        if last_dot_index == -1:
            last_dot_index = len(file.name)
        file_ext = file.name[last_dot_index::]
        file_name = normalize(file.name[:last_dot_index:]) + file_ext
        try:
            file.rename(file.parent.joinpath(file_name))
        except FileExistsError:
            print(f'Error occurred during rename of {file}')
    print('Files have been normalized.')


def unpack_archives(path) -> None:
    archive_path = path.joinpath('archives')
    if not archive_path.is_dir():
        print('No archives found!')
        return None
    print("Archive unpacking started.")
    for archive in archive_path.iterdir():
        last_dot_index = archive.name.rfind('.')
        archive_name = archive.name[:last_dot_index:]
        archive_dir = archive.parent.joinpath(archive_name)
        if not archive.is_file():
            continue
        try:
            os.mkdir(archive_dir)
            Archive(archive).extractall(archive_dir)
        except pyunpack.PatoolError:
            print(f"Error: Archive {archive.name} is not an archive.")
        except FileExistsError:
            pass
    print('All archives have been unpacked.')


root_dir = get_path_from_arg()  # Get folder in which sorting should be done
check_destination_folders(root_dir)  # Create destination folders
stats = sort_all_files(get_all_files(root_dir), root_dir)  # Sort all files in folder
clean_empty_folders(root_dir)  # Delete all empty folders, even destination folders if there are no files
normalize_files(get_all_files(root_dir, True))  # Normalize names of files with known extensions

# Report
for rep_folder in os.listdir(root_dir):
    list_of_files_report = os.listdir(root_dir.joinpath(str(rep_folder)))
    print(f'\tFolder "{rep_folder}" contains: {", ".join(list_of_files_report)}.')
print(f'Total files sorted: {stats[3] + stats[2]}, Known Files: {stats[3]}, Unknown Files: {stats[2]}.')
print(f'Known Extensions: {stats[1]}')
print(f'Unknown Extensions: {stats[0]}')
# End of Report

unpack_archives(root_dir)  # Unpacks archives in archives folder. Original archives are not touched
clean_empty_folders(root_dir)
