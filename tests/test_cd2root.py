#!/usr/bin/env python

"""Tests for `cd2root` package."""


import unittest

import os
import sys
from pathlib import Path

from src.cd2root import main


class TestProjroot(unittest.TestCase):
    """Tests for `cd2root` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.file_path = Path(__file__).parent
        self.project_root = Path(__file__).parent.parent

        os.chdir(self.file_path)
        sys.path.insert(0, str(self.file_path))

        assert self.file_path != self.project_root

    def tearDown(self):
        """Tear down test fixtures, if any."""

        os.chdir(self.file_path)
        sys.path.insert(0, str(self.file_path))

    def test_get_project_file(self):
        assert Path.cwd() == self.file_path
        assert sys.path[0] == str(self.file_path)
        path = Path(__file__).parent
        assert main.get_project_root(use_cwd=False) == self.project_root
        assert main.get_project_root(use_cwd=True) == self.project_root
        assert main.get_project_root(path=path) == self.project_root
        assert main.get_project_root(path=path) == self.project_root
        assert Path.cwd() == self.file_path
        assert sys.path[0] == str(self.file_path)

    def test_cd2path(self):
        assert Path.cwd() == self.file_path
        assert sys.path[0] == str(self.file_path)
        assert main.cd2path(self.project_root) == self.project_root
        assert Path.cwd() == self.project_root
        assert sys.path[0] == str(self.project_root)

    def test_cd2root(self):
        assert Path.cwd() == self.file_path
        assert sys.path[0] == str(self.file_path)
        assert main.cd2root(use_cwd=False) == self.project_root
        assert Path.cwd() == self.project_root
        assert sys.path[0] == str(self.project_root)

    def test_cd2root_cwd(self):
        assert Path.cwd() == self.file_path
        assert sys.path[0] == str(self.file_path)
        assert main.cd2root(use_cwd=True) == self.project_root
        assert Path.cwd() == self.project_root
        assert sys.path[0] == str(self.project_root)
