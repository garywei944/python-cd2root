from pathlib import Path

from typing import Union, Optional

def _get_file_path(use_cwd: bool = False) -> Path: ...
def find_path(path_name: str, use_cwd: bool = False) -> Path: ...
def get_project_root(
    path_name: Optional[str] = None,
    dotfile_name: Optional[str] = None,
    load_dotenv: bool = True,
    use_cwd: bool = False,
    verbose: bool = False,
) -> Path: ...
def cd2path(path: Union[Path, str], verbose: bool = False) -> Path: ...
def cd2root(
    path_name: Optional[str] = None,
    dotfile_name: Optional[str] = None,
    load_dotenv: bool = True,
    use_cwd: bool = False,
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
    :param use_cwd: whether to use current working directory as the starting point
    :param verbose: whether to output verbose messages
    :return: project root directory
    """
