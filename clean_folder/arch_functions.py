from clean_folder import *
import pyunpack


def unpack_archives(archives_path) -> None:
    print('Unpacking archives.')
    for archive in archives_path.iterdir():
        archive_dir = archives_path.joinpath(file_name_separate(archive.name)[0])
        if not archive.is_file():
            continue
        try:
            os.mkdir(archive_dir)
            pyunpack.Archive(archive).extractall(archive_dir)
        except pyunpack.PatoolError:
            print(f"Error: Archive {archive.name} is not an archive.")
        except FileExistsError:
            print(f'Archive {archive.name} already unpacked.')
