import os
import shutil
import uuid
from contextlib import contextmanager
from typing import ContextManager, Union
import tempfile


@contextmanager
def atomic_write(
    file: Union[str, os.PathLike],
    mode: str = "w", as_file: bool = True, **kwargs
) -> ContextManager:
    """Write a file atomically
    :param file: str or :class:`os.PathLike` target to write
    :param mode: the mode in which the file is opened,
                defaults to "w" (writing in text mode)
    :param bool as_file:  if True, the yielded object is a :class:File.
        (eg, what you get with `open(...)`).  Otherwise, it will be the
        temporary file path string
    :param kwargs: anything else needed to open the file
    :raises: FileExistsError if target exists
    Example::
        with atomic_write("hello.txt") as f:
            f.write("world!")
    This is the workflow of the atomic_write function:
    1. The function checks if the file exists in a the directory with an if
        statement. If the file exists, the function throws a
        FileExistsError with the name of the file.
    2. A named temporary file is created using NamedTemporaryFile()
        with mode, kwargs as parameters.
        The file is also givin unique prefix and suffix to ensure
        that the file name is
        unique every time it is created.
    3. The uuid.uuid1() is used to create a unique prefix for the
        file name and os.extsep is used to give the file a unique
        extension every time it is created.
    4. A try, except, finally block is created to handle the file
        and assert for errors.
    5: First, if as_file is true, the function yields the file.
        If as_file is false, the function yields the extension
        using an if/else block.
    6: Second, the function checks for general errors. If it
        encounters a particular error,
        the function closes the temporary file, removes the file
        from the directory with os.remove and raises the particular error.
    7. Third, if the directory and file extension already exist,
        the temporary file is closed. The extension and the file is
        moved from the directory.
    The benifits of using a temporary file is that there will be no
        duplicative files in the directory, there will be no broken,
        unfinished files in the directory and there will be a
        successful job every time.
    The tradeoff is that once the file is created and closed,
    it will never be recovered ever again.
    """

    if os.path.isfile(file):
        raise FileExistsError(f"{file} already exists")

    f = tempfile.NamedTemporaryFile(
        mode=mode,
        delete=False,
        prefix=str(uuid.uuid1()),
        suffix=file.split(os.extsep, 1)[-1],
        **kwargs,
    )
    try:
        if as_file:
            yield f
        else:
            yield f.name
    except Exception as e:
        f.close()
        os.remove(f.name)
        raise e

    finally:
        if os.path.isfile(f.name):
            f.close()
            shutil.move(f.name, file)
