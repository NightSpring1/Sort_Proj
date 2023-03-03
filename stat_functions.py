from constants import EXTENSIONS, UNKNOWN
from sort_functions import file_name_separate
# import os


# def get_stat(path):
#     stats = [set(), set(), 0, 0]
#     for folder in EXTENSIONS:
#         for file in path.joinpath(folder).iterdir():
#             if file.is_file():
#                 stats[0].add(file_name_separate(str(file))[1])
#                 stats[2] += 1
#     for file in path.joinpath(UNKNOWN).iterdir():
#         stats[1].add(file_name_separate(str(file))[1])
#         stats[3] += 1
#     return stats
#
#
# def report(path):
#     sort_stats = get_stat(path)
#     print('* * * * * * * * * * * * * * * * Report * * * * * * * * * * * * * * * * * *')
#     for folder in EXTENSIONS:
#         file_path = path.joinpath(folder)
#         print(f'* Folder {folder} contains: {", ".join([*os.listdir(file_path)])}.')
#     print(f'* Folder {UNKNOWN} contains: {", ".join([*os.listdir(path.joinpath(UNKNOWN))])}')
#     print(f'* Unknown files:{sort_stats[3]}, Known files:{sort_stats[2]}.')
#     print(f'* Known extensions: {sort_stats[0]}')
#     print(f'* Unknown extensions: {sort_stats[1]}')
#     print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')


def get_extensions(stats: dict) -> list:
    k_extensions, uk_extensions = set(), set()
    for folder in EXTENSIONS:
        k_extensions.update(file_name_separate(k)[1] for k in stats[folder])
    uk_extensions.update(file_name_separate(k)[1] for k in stats[UNKNOWN])
    return [k_extensions, uk_extensions]


def report_dict(stats: dict) -> None:
    extensions = get_extensions(stats)
    for i in range(0, 2):
        if len(extensions[i]) == 0:
            extensions[i] = None
    for folder in EXTENSIONS:
        print(f'{folder} contains {len(stats[folder])} files: {", ".join(stats[folder])}')
    print(f'{UNKNOWN} contains {len(stats[UNKNOWN])} files: {", ".join(stats[UNKNOWN])}')
    print(f'Known Extensions: {extensions[0]}, Unknown Extensions: {extensions[1]}')
