import os
import sys
from pathlib import Path
from absl import logging
from dotenv import find_dotenv, load_dotenv as _load_dotenv


def cd2path(path: Path, verbose: bool = True) -> Path:
    """
    Change working directory to path.

    :param path: the path to change working directory to
    :param verbose: whether to output verbose messages
    :return: path
    """
    if verbose:
        print(f"Change working directory to {path}")

    os.chdir(path)
    sys.path.insert(0, str(path))

    return path


def cd2root(dotfile_name: str = None, load_dotenv: bool = True) -> Path:
    """
    Change working directory to project root directory.

    The rules to find the project root directory:
    1. If dotfile_name is not None, find the directory containing dotfile_name
    2. If PROJECT_ROOT is set in .env, use it
    3. If any of the following files is found, use the directory containing it:
        .idea, .vscode, .editorconfig, .env, pyproject.toml, LICENSE

    :param dotfile_name: the name of the dotfile to find as the project root directory
    :param load_dotenv: whether to load .env file
    :return: project root directory
    """
    if load_dotenv:
        _load_dotenv()

    if dotfile_name is not None:
        try:
            return cd2path(Path(find_dotenv(dotfile_name)))
        except TypeError:
            logging.warning(f"{dotfile_name} is not found!")

    # If PROJECT_ROOT is set in .env, use it
    if os.getenv("PROJECT_ROOT") is not None:
        return cd2path(Path(os.getenv("PROJECT_ROOT")))

    for file_name in [
        ".idea",
        ".vscode",
        ".editorconfig",
        ".env",
        "pyproject.toml",
        "LICENSE",
    ]:
        project_root = find_dotenv(file_name)
        if project_root != "":
            return cd2path(Path(project_root))

    return Path.cwd()
