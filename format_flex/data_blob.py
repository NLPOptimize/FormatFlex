import os
from typing import Union, Any


def format_file_size(size_bytes: int, precision: int = 2, fmt: Union[str, None] = None, padding: str = ''):
    if size_bytes == 0: return "0B"
    import math
    units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.log(size_bytes, 1024)) if fmt is None else units.index(fmt)
    return f'{round(size_bytes / 1024 ** i, precision)}{padding}{units[i]}'


class DataBlob:
    def __init__(self, raw: Union[str, bytes], ext: str):
        self._raw = raw
        self._size = len(raw)
        self._format = ext[1:]

    @property
    def size(self):
        return self._size

    def __str__(self):
        return str(self._raw)

    def show(self):
        print(f'{self._format}: {format_file_size(self.size)}')

    @property
    def summary(self):
        return f'{self._format}: {format_file_size(self.size)}'


class DataBlobText(DataBlob):
    def __init__(self, raw: Union[str, bytes], ext: str):
        super().__init__(raw, ext)

    @property
    def text(self):
        return self._raw


class DataBlobTable:
    def __init__(self, file_path):
        self._file_path = file_path
        self._size = os.path.getsize(self._file_path)
        _, ext = os.path.splitext(self._file_path)
        self._format = ext[1:]

    @property
    def size(self):
        return self._size

    @property
    def path(self):
        return self._file_path

    def show(self):
        print(f'{self._format}: {format_file_size(self.size)}')

    @property
    def summary(self):
        return f'{self._format}: {format_file_size(self.size)}'
