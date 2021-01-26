import os


def get_relative_path_to_script():
    return os.path.dirname(os.path.abspath(__file__))
