import os
import sys
from pathlib import Path
from absl import logging
from dotenv import load_dotenv as _load_dotenv

from typing import Union, Optional


def _get_file_path(use_cwd: bool = True) -> Path:
    """
    Get the path of the file that calls this function.

    :param use_cwd: whether to use current working directory as the starting point
    :return: the path of the directory of the file that calls this function
    """

    # https://github.com/theskumar/python-dotenv/blob/main/src/dotenv/main.py#L281_L300
    def _is_interactive():
        """Decide whether this is running in a REPL or IPython notebook"""
        main = __import__("__main__", None, None, fromlist=["__file__"])
        return not hasattr(main, "__file__")

    if use_cwd or _is_interactive() or getattr(sys, "frozen", False):
        # Should work without __file__, e.g. in REPL or IPython notebook.
        path = Path.cwd().resolve().absolute()
    else:
        # will work for .py files
        frame = sys._getframe()
        current_file = __file__

        while frame.f_code.co_filename == current_file:
            assert frame.f_back is not None
            frame = frame.f_back
        frame_filename = frame.f_code.co_filename
        path = Path(frame_filename).absolute().parent

    return path


def find_path(path_name: str, use_cwd: bool = True) -> Path:
    """
    Find the path of the given path_name.

    raise FileNotFoundError if the path is not found.

    :param path_name: the name of the path to find
    :param use_cwd: whether to use current working directory as the starting point
    :return: the path of the given path_name
    """
    path = _get_file_path(use_cwd=use_cwd)
    while path.name != path_name and path != path.parent:
        path = path.parent
    if path.name != path_name:
        raise FileNotFoundError(f"{path_name} is not found!")
    return path


def find_dotfile(dotfile_name: str, use_cwd: bool = True) -> Path:
    """
    Find the path of the given dotfile_name.

    raise FileNotFoundError if the dotfile is not found.

    :param dotfile_name: the name of the dotfile to find
    :param use_cwd: whether to use current working directory as the starting point
    :return: the path of the folder of the given dotfile_name
    """
    path = _get_file_path(use_cwd=use_cwd)
    while not path.joinpath(dotfile_name).is_file() and path != path.parent:
        path = path.parent
    if not path.joinpath(dotfile_name).is_file():
        raise FileNotFoundError(f"{dotfile_name} is not found!")
    return path


def get_project_root(
    path_name: Optional[str] = None,
    dotfile_name: Optional[str] = None,
    load_dotenv: bool = True,
    use_cwd: bool = True,
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
    :param use_cwd: whether to use current working directory as the starting point
    :param verbose: whether to output verbose messages
    :return: project root directory
    """
    if load_dotenv:
        _load_dotenv()

    if path_name is not None:
        try:
            return find_path(path_name, use_cwd=use_cwd)
        except FileNotFoundError as err:
            logging.warning(err)

    if dotfile_name is not None:
        try:
            return find_dotfile(dotfile_name, use_cwd=use_cwd)
        except FileNotFoundError as err:
            logging.warning(err)

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
        try:
            project_root = find_dotfile(file_name, use_cwd=use_cwd)

            if verbose:
                print(f"Found {file_name} at {project_root}")

            return project_root
        except FileNotFoundError as err:
            logging.warning(err)

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


def cd2root(verbose: bool = False, *args, **kwargs) -> Path:
    """
    Change working directory to project root directory.

    :return: project root directory
    """
    try:
        return cd2path(
            get_project_root(verbose=verbose, *args, **kwargs),
            verbose=verbose,
        )
    except FileNotFoundError as err:
        if verbose:
            logging.warning(err)
        return Path.cwd()
