import os
import io
import pickle
from typing import Union, Any
import dill
import zstandard
import cloudpickle
import joblib
import numpy as np
from enum import Enum, auto
from .data_blob import DataBlobTable


class GenericFormat(Enum):
    UNKNOWN = auto()
    PICKLE = auto()
    DILL = auto()
    CLOUDPICKLE = auto()
    JOBLIB = auto()


class GeneticData:
    class __GenericTo:
        def __init__(self, data):
            self.data = data
            self.extension_mapping = {
                GenericFormat.PICKLE: ".pkl",
                GenericFormat.DILL: ".dill",
                GenericFormat.CLOUDPICKLE: ".cpickle",
                GenericFormat.JOBLIB: ".joblib"
            }

        def _filename(self, file: str, fmt: GenericFormat):
            basename, _ = os.path.splitext(file)
            return basename + self.extension_mapping[fmt]

        def pickle(self, save_path: str) -> DataBlobTable:
            result = pickle.dumps(self.data, protocol=pickle.HIGHEST_PROTOCOL)
            cctx = zstandard.ZstdCompressor(level=19, threads=os.cpu_count() * 2)
            compressed_data = cctx.compress(result)
            output_path = self._filename(save_path, GenericFormat.PICKLE)
            with open(output_path, "wb") as f:
                f.write(compressed_data)
            return DataBlobTable(output_path)

        def dill(self, save_path: str) -> DataBlobTable:
            result = dill.dumps(self.data)
            output_path = self._filename(save_path, GenericFormat.DILL)
            with open(output_path, "wb") as f:
                f.write(result)
            return DataBlobTable(output_path)

        def cloudpickle(self, save_path: str) -> DataBlobTable:
            result = cloudpickle.dumps(self.data)
            output_path = self._filename(save_path, GenericFormat.CLOUDPICKLE)
            with open(output_path, "wb") as f:
                f.write(result)
            return DataBlobTable(output_path)

        def joblib(self, save_path: str) -> DataBlobTable:
            output_path = self._filename(save_path, GenericFormat.JOBLIB)
            joblib.dump(self.data, output_path, compress=("gzip", 9))
            return DataBlobTable(output_path)

    class __GenericFrom:
        def __init__(self, data, fmt: GenericFormat = GenericFormat.UNKNOWN):
            self.data = data
            self.fmt = fmt

        def pickle(self):
            dctx = zstandard.ZstdDecompressor()
            decompressed_data = dctx.decompress(self.data)
            return pickle.loads(decompressed_data)

        def dill(self):
            return dill.loads(self.data)

        def cloudpickle(self):
            return cloudpickle.loads(self.data)

        def joblib(self):
            buffer = io.BytesIO(self.data)
            return joblib.load(buffer)

    @staticmethod
    def __detect_format_from_extension(file_path: str) -> GenericFormat:
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        if ext in ['.pkl', '.pickle']:
            return GenericFormat.PICKLE
        elif ext == '.dill':
            return GenericFormat.DILL
        elif ext in ['.cpickle', '.cloudpickle']:
            return GenericFormat.CLOUDPICKLE
        elif ext == '.joblib':
            return GenericFormat.JOBLIB
        else:
            return GenericFormat.UNKNOWN

    def __init__(self, data: Any, fmt: GenericFormat = GenericFormat.UNKNOWN):
        if isinstance(data, str) and os.path.exists(data):
            detected = GeneticData.__detect_format_from_extension(data)
            fmt = detected if fmt == GenericFormat.UNKNOWN else fmt
            with open(data, "rb") as f:
                data = f.read()
            self.__data = self.__GenericFrom(data, fmt)
        elif isinstance(data, bytes):
            self.__data = self.__GenericFrom(data, fmt)
        else:
            self.__data = data

    @property
    def to(self):
        return GeneticData.__GenericTo(self.__data)
