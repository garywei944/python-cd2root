=====================================================
cd2root: Change Working Directory to the Project Root
=====================================================

.. image:: https://img.shields.io/pypi/v/cd2root.svg
        :target: https://pypi.python.org/pypi/cd2root

..
    .. image:: https://img.shields.io/travis/garywei944/cd2root.svg
            :target: https://travis-ci.com/garywei944/cd2root

    .. image:: https://readthedocs.org/projects/cd2root/badge/?version=latest
            :target: https://cd2root.readthedocs.io/en/latest/?version=latest
            :alt: Documentation Status

``cd2root`` allows you to elegantly change the working directory of the current file to the project root directory with only 1 line of code.
It is useful when you have a project with a deep directory structure and you want to import modules relative to the project root directory.

===============
Getting Started
===============

Install cd2root
---------------
.. code-block:: bash

    pip install cd2root

Usage
-----
The easiest way to use ``cd2root`` is to add the following line to the top of your python file:

.. code-block:: python

    # normally import packages before custom modules
    import ...

    ############################################################################
    # cd2root: change working directory to project root
    from cd2root import cd2root
    cd2root()
    ############################################################################

    # Then import custom modules that are relative to the project root
    from src.utils import ...

If you just want to get the project root directory without changing the working directory

.. code-block:: python

    from cd2root import get_project_root

    project_root = get_project_root()  # type: pathlib.Path
    data_file = project_root / "data" / "data.csv"
    ...

=============
Documentation
=============
``cd2root.cd2root`` is the grab-and-go function for most use cases.
It has the following signature:

.. code-block:: python

    def cd2root(
        path_name: str = None,
        dotfile_name: str = None,
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
        ...

``cd2root.get_project_root`` shares the same signature as ``cd2root.cd2root`` except that it does not change the working directory.

.. code-block:: python

    def get_project_root(
        path_name: str = None,
        dotfile_name: str = None,
        load_dotenv: bool = True,
        use_cwd: bool = False,
        verbose: bool = False,
    ) -> Path:
        """
        Get the project root directory. Raise FileNotFoundError if the project root
        directory is not found.

        ...
        """
        ...

There are also other helper functions available with ``cd2root``.
``cd2root.cd2path`` change the working directory to given path.

.. code-block:: python

    def cd2path(path: Union[Path, str], verbose: bool = False) -> Path:
        """
        Change working directory to path.

        :param path: the path to change working directory to
        :param verbose: whether to output verbose messages
        :return: path
        """
        ...

    def find_path(path_name: str, use_cwd: bool = False) -> Path:
        """
        Find the path of the given path_name.

        raise FileNotFoundError if the path is not found.

        :param path_name: the name of the path to find
        :param use_cwd: whether to use current working directory as the starting point
        :return: the path of the given path_name
        """
        ...
