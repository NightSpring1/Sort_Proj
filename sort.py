from constants import EXTENSIONS, UNKNOWN
from conf_functions import get_root_path_from_arg, get_all_files
from sort_functions import check_destination_folders, find_filetype, move_files, clean_empty_folders
from norm_functions import normalize_files_in_folder
from arch_functions import unpack_archives
from stat_functions import report_dict

if __name__ == '__main__':
    root_path = get_root_path_from_arg()
    if root_path is not None:
        check_destination_folders(root_path)
        all_files = get_all_files(root_path, root_path)
        unknown_files = all_files
        stat_dict = dict()
        # Move files section
        for destination_folder in EXTENSIONS:
            file_type_paths = find_filetype(all_files, destination_folder)
            move_files(file_type_paths, root_path, destination_folder)
            unknown_files = [path for path in unknown_files if path not in file_type_paths]
        stat_dict[UNKNOWN] = [fn.name for fn in unknown_files]
        move_files(unknown_files, root_path, UNKNOWN)
        # End of move files section

        # Normalization files section
        for n_destination_folder in EXTENSIONS:
            stat_dict[n_destination_folder] = normalize_files_in_folder(root_path.joinpath(n_destination_folder))
        # End of normalization section

        # Archives section
        unpack_archives(root_path.joinpath('archives'))
        # End of archives section

        # Report
        report_dict(stat_dict)
        # report(root_path)

        # Cleanup
        clean_empty_folders(root_path)
        print('Script Terminated Successfully')
    else:
        print('Script Terminated with Error!')
