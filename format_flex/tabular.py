import pandas as pd
import os
import io
from typing import Union
from enum import Enum, auto
from tabulate import tabulate
from .data_blob import DataBlob, DataBlobText, DataBlobTable


class TabularFormat(Enum):
    UNKNOWN = auto()
    CSV = auto()
    EXCEL = auto()
    PARQUET = auto()
    ORC = auto()
    FEATHER = auto()
    # HDF5 = auto()


class TabularData:
    class __TabularTo:
        def __init__(self, data, sheet_name: str = "Sheet1"):
            self.data: pd.DataFrame = data
            self.sheet_name = sheet_name
            self.extension_mapping = {
                TabularFormat.CSV: ".csv",
                TabularFormat.EXCEL: ".xlsx",
                TabularFormat.PARQUET: ".parquet",
                TabularFormat.ORC: ".orc",
                TabularFormat.FEATHER: ".feather",
                # TabularFormat.HDF5: ".h5"
            }

        def _filename(self, file: str, fmt: TabularFormat):
            basename, _ = os.path.splitext(file)
            return basename + self.extension_mapping[fmt]

        def csv(self, save_path: str) -> DataBlobTable:
            buffer = io.StringIO()
            self.data.to_csv(buffer, index=False)
            result = buffer.getvalue()
            output_path = self._filename(save_path, TabularFormat.CSV)
            with open(output_path, 'w', encoding="utf-8") as f:
                f.write(result)
            return DataBlobTable(os.path.abspath(output_path))

        def excel(self, save_path: str) -> DataBlobTable:
            buffer = io.BytesIO()
            self.data.to_excel(buffer, sheet_name=self.sheet_name, engine="openpyxl", index=False)
            buffer.seek(0)
            result = buffer.getvalue()
            output_path = self._filename(save_path, TabularFormat.EXCEL)
            with open(output_path, 'wb') as f:
                f.write(result)
            return DataBlobTable(os.path.abspath(output_path))

        def parquet(self, save_path: str) -> DataBlobTable:
            buffer = io.BytesIO()
            self.data.to_parquet(buffer, engine="pyarrow", compression="zstd", index=False)
            buffer.seek(0)
            result = buffer.getvalue()
            output_path = self._filename(save_path, TabularFormat.PARQUET)
            with open(output_path, 'wb') as f:
                f.write(result)
            return DataBlobTable(os.path.abspath(output_path))

        def orc(self, save_path: str) -> DataBlobTable:
            buffer = io.BytesIO()
            self.data.to_orc(buffer, index=False, engine="pyarrow")
            buffer.seek(0)
            result = buffer.getvalue()
            output_path = self._filename(save_path, TabularFormat.ORC)
            with open(output_path, 'wb') as f:
                f.write(result)
            return DataBlobTable(os.path.abspath(output_path))

        def feather(self, save_path: str) -> DataBlobTable:
            output_path = self._filename(save_path, TabularFormat.FEATHER)
            self.data.to_feather(output_path)
            return DataBlobTable(os.path.abspath(output_path))

        # def hdf5(self, save_path: str) -> DataBlobTable:
        #     output_path = self._filename(save_path, TabularFormat.HDF5)
        #     self.data.to_hdf(output_path, key="data", mode="w"
        #                      , complib="blosc", complevel=9)
        #     return DataBlobTable(os.path.abspath(output_path))

    class __TabularFrom:
        def __init__(self, data, **kwargs):
            self.data = data
            self.kwargs = kwargs

        def csv(self) -> pd.DataFrame:
            if isinstance(self.data, bytes):
                self.data = self.data.decode('utf-8')
            return pd.read_csv(io.StringIO(self.data), **self.kwargs)

        def excel(self) -> pd.DataFrame:
            return pd.read_excel(io.BytesIO(self.data), **self.kwargs)

        def parquet(self) -> pd.DataFrame:
            return pd.read_parquet(io.BytesIO(self.data), engine="pyarrow", **self.kwargs)

        def orc(self) -> pd.DataFrame:
            return pd.read_orc(io.BytesIO(self.data), **self.kwargs)

        def feather(self) -> pd.DataFrame:
            if isinstance(self.data, bytes):
                return pd.read_feather(io.BytesIO(self.data))
            return pd.read_feather(self.data)

        def hdf5(self) -> pd.DataFrame:
            if isinstance(self.data, bytes):
                return pd.read_hdf(io.BytesIO(self.data), key="data", **self.kwargs)
            return pd.read_hdf(self.data, key="data", **self.kwargs)

    def __init__(self, data, format: TabularFormat = TabularFormat.UNKNOWN, **kwargs):
        if isinstance(data, str) and os.path.exists(data):
            detected_format = self.__detect_format_from_extension(data)
            if detected_format == TabularFormat.CSV:
                self.__df = pd.read_csv(data, **kwargs)
            elif detected_format == TabularFormat.EXCEL:
                self.__df = pd.read_excel(data, **kwargs)
            elif detected_format == TabularFormat.PARQUET:
                self.__df = pd.read_parquet(data, **kwargs)
            elif detected_format == TabularFormat.ORC:
                self.__df = pd.read_orc(data, **kwargs)
            elif detected_format == TabularFormat.FEATHER:
                self.__df = pd.read_feather(data)
            elif detected_format == TabularFormat.HDF5:
                self.__df = pd.read_hdf(data, key="data", **kwargs)
            else:
                raise ValueError(f"Unsupported file format: {data}")
        elif isinstance(data, (str, bytes)):
            fmt = format
            if fmt == TabularFormat.UNKNOWN:
                fmt = self.detect_format(data)
            if fmt == TabularFormat.CSV:
                self.__df = self.__TabularFrom(data, **kwargs).csv()
            elif fmt == TabularFormat.EXCEL:
                self.__df = self.__TabularFrom(data, **kwargs).excel()
            elif fmt == TabularFormat.PARQUET:
                self.__df = self.__TabularFrom(data, **kwargs).parquet()
            elif fmt == TabularFormat.ORC:
                self.__df = self.__TabularFrom(data, **kwargs).orc()
            elif fmt == TabularFormat.FEATHER:
                self.__df = self.__TabularFrom(data, **kwargs).feather()
            elif fmt == TabularFormat.HDF5:
                self.__df = self.__TabularFrom(data, **kwargs).hdf5()
            else:
                raise ValueError("Unable to detect file_data format")
        elif isinstance(data, pd.DataFrame):
            self.__df = data.copy()
        else:
            self.__df = pd.DataFrame(data, **kwargs)

    @staticmethod
    def __detect_format_from_extension(file_path):
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        if ext in ['.csv', '.txt']:
            return TabularFormat.CSV
        elif ext in ['.xls', '.xlsx', '.xlsm']:
            return TabularFormat.EXCEL
        elif ext == '.parquet':
            return TabularFormat.PARQUET
        elif ext == '.orc':
            return TabularFormat.ORC
        elif ext == '.feather':
            return TabularFormat.FEATHER
        elif ext in ['.h5', '.hdf5']:
            return TabularFormat.HDF5
        else:
            return TabularFormat.UNKNOWN

    @staticmethod
    def detect_format(file_data):
        if isinstance(file_data, str):
            if ',' in file_data and '\n' in file_data:
                lines = file_data.split('\n')
                if len(lines) > 1:
                    first_line_commas = lines[0].count(',')
                    if any(line and line.count(',') == first_line_commas for line in lines[1:3]):
                        return TabularFormat.CSV
            return TabularFormat.UNKNOWN
        elif isinstance(file_data, bytes):
            if file_data[:8] == b'\x89HDF\r\n\x1a\n':
                return TabularFormat.HDF5
            if file_data[:4] in (b'FEA1', b'FEA2'):
                return TabularFormat.FEATHER
            if file_data[:2] == b'PK':
                return TabularFormat.EXCEL
            if file_data[:8] == b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1':
                return TabularFormat.EXCEL
            if file_data[:4] == b'PAR1':
                return TabularFormat.PARQUET
            if file_data[:3] == b'ORC':
                return TabularFormat.ORC
            try:
                sample = file_data[:1024].decode('utf-8', errors='ignore')
                if ',' in sample and '\n' in sample:
                    lines = sample.split('\n')
                    if len(lines) > 1:
                        first_line_commas = lines[0].count(',')
                        if any(line and line.count(',') == first_line_commas for line in lines[1:3]):
                            return TabularFormat.CSV
            except:
                pass
        return TabularFormat.UNKNOWN

    @property
    def to(self):
        return TabularData.__TabularTo(self.__df)

    @property
    def dataframe(self):
        return self.__df

    def keys(self):
        return set(self.__df.columns)

    def __getitem__(self, key):
        return self.__df[key].tolist()

    def __setitem__(self, key, value):
        self.__df[key] = value

    def __len__(self):
        return len(self.__df)

    def __str__(self):
        try:
            return tabulate(self.__df, headers=self.__df.columns, tablefmt="simple_grid", showindex=False)
        except ImportError:
            return str(self.__df)

    def json(self):
        return {column: self.__df[column].tolist() for column in self.__df.columns}
