import os
import sys
from pathlib import Path
from absl import logging
from dotenv import find_dotenv, load_dotenv as _load_dotenv

from typing import Union


def find_path(path_name: str) -> Path:
    """
    Find the path of the given path_name.

    raise FileNotFoundError if the path is not found.

    :param path_name: the name of the path to find
    :return: the path of the given path_name
    """
    path = Path.cwd().resolve()
    while path.name != path_name and path != path.parent:
        path = path.parent
    if path.name != path_name:
        raise FileNotFoundError(f"{path_name} is not found!")
    return path


def get_project_root(
    path_name: str = None,
    dotfile_name: str = None,
    load_dotenv: bool = True,
    verbose: bool = False,
) -> Path:
    """
    Get the project root directory. Raise FileNotFoundError if the project root
    directory is not found.

    The rules to find the project root directory:
    1. If path_name is not None, find the directory containing path_name
    2. If dotfile_name is not None, find the directory containing dotfile_name
    3. If PROJECT_ROOT is set in .env, use it
    4. If any of the following files is found, use the directory containing it:
        .idea, .vscode, .editorconfig, .env, pyproject.toml, LICENSE

    :param path_name: the name of the path to find as the project root directory
    :param dotfile_name: the name of the dotfile to find as the project root directory
    :param load_dotenv: whether to load .env file
    :param verbose: whether to output verbose messages
    :return: project root directory
    """
    if load_dotenv:
        _load_dotenv()

    if path_name is not None:
        try:
            return find_path(path_name)
        except FileNotFoundError as err:
            logging.warning(err)

    if dotfile_name is not None:
        project_root = find_dotenv(dotfile_name)
        if project_root != "":
            return Path(project_root).parent
        else:
            logging.warning(f"{dotfile_name} is not found!")

    # If PROJECT_ROOT is set in .env, use it
    if os.getenv("PROJECT_ROOT") is not None:
        return Path(os.getenv("PROJECT_ROOT"))

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
            if verbose:
                print(f"Found {file_name} at {project_root}")
            return Path(project_root).parent

    raise FileNotFoundError("Project root directory is not found!")


def cd2path(path: Union[Path, str], verbose: bool = False) -> Path:
    """
    Change working directory to path.

    :param path: the path to change working directory to
    :param verbose: whether to output verbose messages
    :return: path
    """
    if verbose:
        print(f"Changed working directory to {path}")

    os.chdir(path)
    sys.path.insert(0, str(path))

    return path


def cd2root(
    path_name: str = None,
    dotfile_name: str = None,
    load_dotenv: bool = True,
    verbose: bool = False,
) -> Path:
    """
    Change working directory to project root directory.

    The rules to find the project root directory:
    1. If path_name is not None, find the directory containing path_name
    2. If dotfile_name is not None, find the directory containing dotfile_name
    3. If PROJECT_ROOT is set in .env, use it
    4. If any of the following files is found, use the directory containing it:
        .idea, .vscode, .editorconfig, .env, pyproject.toml, LICENSE

    :param path_name: the name of the path to find as the project root directory
    :param dotfile_name: the name of the dotfile to find as the project root directory
    :param load_dotenv: whether to load .env file
    :param verbose: whether to output verbose messages
    :return: project root directory
    """
    try:
        return cd2path(
            get_project_root(path_name, dotfile_name, load_dotenv, verbose),
            verbose=verbose,
        )
    except FileNotFoundError as err:
        if verbose:
            logging.warning(err)
        return Path.cwd()
