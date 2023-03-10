from constants import EXTENSIONS
import re


def find_images(list_of_file_paths: list) -> list:
    file_images1 = []
    for file_path in list_of_file_paths:
        file_ext = re.search(r'(?:\.([^.]+))?$', file_path.name).group()
        selection_rule = file_ext.upper().endswith(EXTENSIONS["images"])
        if selection_rule:
            file_images1.append(file_path)
    return file_images1


def find_archives(list_of_file_paths: list) -> list:
    file_archives1 = []
    for file_path in list_of_file_paths:
        file_ext = re.search(r'(?:\.([^.]+))?$', file_path.name).group()
        selection_rule = file_ext.upper().endswith(EXTENSIONS["archives"])
        if selection_rule:
            file_archives1.append(file_path)
    return file_archives1


def find_videos(list_of_file_paths: list) -> list:
    file_videos1 = []
    for file_path in list_of_file_paths:
        file_ext = re.search(r'(?:\.([^.]+))?$', file_path.name).group()
        selection_rule = file_ext.upper().endswith(EXTENSIONS["videos"])
        if selection_rule:
            file_videos1.append(file_path)
    return file_videos1


def find_audio(list_of_file_paths: list) -> list:
    file_audio1 = []
    for file_path in list_of_file_paths:
        file_ext = re.search(r'(?:\.([^.]+))?$', file_path.name).group()
        selection_rule = file_ext.upper().endswith(EXTENSIONS["audio"])
        if selection_rule:
            file_audio1.append(file_path)
    return file_audio1


def find_documents(list_of_file_paths: list) -> list:
    file_documents1 = []
    for file_path in list_of_file_paths:
        file_ext = re.search(r'(?:\.([^.]+))?$', file_path.name).group()
        selection_rule = file_ext.upper().endswith(EXTENSIONS["documents"])
        if selection_rule:
            file_documents1.append(file_path)
    return file_documents1
