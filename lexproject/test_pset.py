#!/usr/bin/env python
# -*- coding: utf-8 -*-

from approject.hash_str import hash_str
from approject.io import atomic_write

import os
from tempfile import TemporaryDirectory
from unittest import TestCase
import tempfile


class FakeFileFailure(IOError):
    pass


class HashTests(TestCase):
    def test_basic(self):
        self.assertEqual(
            hash_str("world!", salt="hello, ").hex()[:6], "68e656")


class AtomicWriteTests(TestCase):
    def test_atomic_write(self):
        """Ensure file exists after being written successfully"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            with atomic_write(fp, "w") as f:
                assert not os.path.exists(fp)
                tmpfile = f.name
                f.write("asdf")

            assert not os.path.exists(tmpfile)
            assert os.path.exists(fp)

            with open(fp) as f:
                self.assertEqual(f.read(), "asdf")

    def test_atomic_failure(self):
        """Ensure that file does not exist after failure during write"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            with self.assertRaises(FakeFileFailure):
                with atomic_write(fp, "w") as f:
                    tmpfile = f.name
                    assert os.path.exists(tmpfile)
                    raise FakeFileFailure()

            assert not os.path.exists(tmpfile)
            assert not os.path.exists(fp)

    def test_file_exists(self):
        """Ensure an error is raised when a file exists"""

        def test_raise():
            f = tempfile.NamedTemporaryFile()
            with atomic_write(f.name, "w") as f:
                pass
        self.assertRaises(FileExistsError, test_raise)
        """
        This test raises a FileExistsError if a temporary file already exists
        in the directory. It evokes the NamedTemporyFile function and uses the
        atomic_write function in a writing mode.
        """
