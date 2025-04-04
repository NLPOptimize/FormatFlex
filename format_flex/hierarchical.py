from lxml import etree
import json
import yaml
import toml
import os
from typing import Dict, Union, List
from enum import Enum, auto
import cbor2
import msgpack as messagepack
import bson
import ubjson

from .data_blob import DataBlob, DataBlobText, DataBlobTable


class HierarchicalFormat(Enum):
    UNKNOWN = auto()
    XML = auto()
    JSON = auto()
    YAML = auto()
    TOML = auto()
    CBOR2 = auto()
    MSGPACK = auto()
    BSON = auto()
    UBJSON = auto()


class HierarchicalData:
    class __HierarchicalTo:
        def __init__(self, data, root_name: str = "root", indent=4):
            self.data = data
            self.root_name = root_name
            self.indent = indent
            self.extension_mapping = {
                HierarchicalFormat.XML: ".xml",
                HierarchicalFormat.JSON: ".json",
                HierarchicalFormat.YAML: ".yaml",
                HierarchicalFormat.TOML: ".toml",
                HierarchicalFormat.CBOR2: ".cbor",
                HierarchicalFormat.MSGPACK: ".msgpack",
                HierarchicalFormat.BSON: ".bson",
                HierarchicalFormat.UBJSON: ".ubjson"
            }

        def _filename(self, file: str, fmt: HierarchicalFormat):
            basename, _ = os.path.splitext(file)
            return basename + self.extension_mapping[fmt]

        def xml(self, save_path: Union[str, None] = None) -> DataBlobText:
            def _convert(parent, data):
                if isinstance(data, dict):
                    for key, value in data.items():
                        child = etree.SubElement(parent, str(key))
                        _convert(child, value)
                elif isinstance(data, list):
                    for item in data:
                        child = etree.SubElement(parent, "item")
                        _convert(child, item)
                else:
                    parent.text = str(data)

            if len(self.data) == 1:
                root_key = list(self.data.keys())[0]
                root = etree.Element(root_key)
                dictionary = self.data[root_key]
            else:
                root = etree.Element(self.root_name)
                dictionary = self.data
            _convert(root, dictionary)
            result = etree.tostring(root, encoding='utf-8', xml_declaration=True, pretty_print=True).decode('utf-8')
            if save_path is not None:
                output_path = self._filename(save_path, HierarchicalFormat.XML)
                with open(output_path, "wt", encoding="utf-8") as f:
                    f.write(result)
            return DataBlobText(result,
                                self.extension_mapping[HierarchicalFormat.XML])

        def json(self, save_path: Union[str, None] = None) -> DataBlobText:
            result = json.dumps(self.data, indent=self.indent, ensure_ascii=False)
            if save_path is not None:
                output_path = self._filename(save_path, HierarchicalFormat.JSON)
                with open(output_path, "wt", encoding="utf-8") as f:
                    f.write(result)
            return DataBlobText(result, self.extension_mapping[HierarchicalFormat.JSON])

        def yaml(self, save_path: Union[str, None] = None) -> DataBlobText:
            result = yaml.dump(self.data, default_flow_style=False, indent=self.indent)
            if save_path is not None:
                output_path = self._filename(save_path, HierarchicalFormat.YAML)
                with open(output_path, "wt", encoding="utf-8") as f:
                    f.write(result)
            return DataBlobText(result, self.extension_mapping[HierarchicalFormat.YAML])

        def toml(self, save_path: Union[str, None] = None) -> DataBlobText:
            result = toml.dumps(self.data)
            if save_path is not None:
                output_path = self._filename(save_path, HierarchicalFormat.TOML)
                with open(output_path, "wt", encoding="utf-8") as f:
                    f.write(result)
            return DataBlobText(result, self.extension_mapping[HierarchicalFormat.TOML])

        def cbor2(self, save_path: Union[str, None] = None) -> DataBlob:
            result = cbor2.dumps(self.data)
            if save_path is not None:
                output_path = self._filename(save_path, HierarchicalFormat.CBOR2)
                with open(output_path, "wb") as f:
                    f.write(result)
            return DataBlob(result, self.extension_mapping[HierarchicalFormat.CBOR2])

        def msgpack(self, save_path: Union[str, None] = None) -> DataBlob:
            result = messagepack.packb(self.data, use_bin_type=True)
            if save_path is not None:
                output_path = self._filename(save_path, HierarchicalFormat.MSGPACK)
                with open(output_path, "wb") as f:
                    f.write(result)
            return DataBlob(result, self.extension_mapping[HierarchicalFormat.MSGPACK])

        def bson(self, save_path: Union[str, None] = None) -> DataBlob:
            result = bson.BSON.encode(self.data)
            if save_path is not None:
                output_path = self._filename(save_path, HierarchicalFormat.BSON)
                with open(output_path, "wb") as f:
                    f.write(result)
            return DataBlob(result, self.extension_mapping[HierarchicalFormat.BSON])

        def ubjson(self, save_path: Union[str, None] = None) -> DataBlob:
            result = ubjson.dumpb(self.data)
            if save_path is not None:
                output_path = self._filename(save_path, HierarchicalFormat.UBJSON)
                with open(output_path, "wb") as f:
                    f.write(result)
            return DataBlob(result, self.extension_mapping[HierarchicalFormat.UBJSON])

    class __HierarchicalFrom:
        def __init__(self, data, root_name: str = "root", indent=4):
            self.data = data
            self.root_name = root_name
            self.indent = indent
            parser = etree.XMLParser(remove_blank_text=True)
            self.xml_version = None
            try:
                tree = etree.fromstring(data.encode('utf-8'), parser)
                self.xml_version = tree.getroottree().docinfo.xml_version
            except Exception:
                pass

        def xml(self) -> dict:
            def _convert_element(element):
                if len(element) == 0:
                    if element.text and element.text.strip():
                        text = element.text.strip()
                        try:
                            return float(text) if '.' in text else int(text)
                        except ValueError:
                            return text
                    return None
                result = {}
                for child in element:
                    child_result = _convert_element(child)
                    if child.tag in result:
                        if isinstance(result[child.tag], list):
                            result[child.tag].append(child_result)
                        else:
                            result[child.tag] = [result[child.tag], child_result]
                    else:
                        result[child.tag] = child_result
                return DataBlob(result)

            parser = etree.XMLParser(remove_blank_text=True)
            root = etree.fromstring(self.data.encode('utf-8'), parser)
            if root.tag == self.root_name:
                return _convert_element(root)
            return {root.tag: _convert_element(root)}

        def json(self) -> dict:
            return json.loads(self.data)

        def yaml(self) -> dict:
            return yaml.safe_load(self.data)

        def toml(self) -> dict:
            return toml.loads(self.data)

        def cbor2(self) -> dict:
            bdata = self.data if isinstance(self.data, bytes) else self.data.encode('utf-8')
            return cbor2.loads(bdata)

        def messagepack(self) -> dict:
            bdata = self.data if isinstance(self.data, bytes) else self.data.encode('utf-8')
            return messagepack.unpackb(bdata, raw=False)

        def bson(self) -> dict:
            bdata = self.data if isinstance(self.data, bytes) else self.data.encode('utf-8')
            return bson.BSON(bdata).decode()

        def ubjson(self) -> dict:
            bdata = self.data if isinstance(self.data, bytes) else self.data.encode('utf-8')
            return ubjson.loadb(bdata)

    def __init__(self, data: Union[Dict, str, bytes]):
        if isinstance(data, str) and os.path.exists(data):
            with open(data, "rt", encoding="utf-8") as f:
                data = f.read()
        elif isinstance(data, bytes) and os.path.exists(data):
            with open(data, "rb") as f:
                data = f.read()
        if isinstance(data, (str, bytes)):
            fmt = HierarchicalData.detect_format(data)
            if fmt == HierarchicalFormat.XML:
                self.__data = self.__HierarchicalFrom(data).xml()
            elif fmt == HierarchicalFormat.JSON:
                self.__data = self.__HierarchicalFrom(data).json()
            elif fmt == HierarchicalFormat.YAML:
                self.__data = self.__HierarchicalFrom(data).yaml()
            elif fmt == HierarchicalFormat.TOML:
                self.__data = self.__HierarchicalFrom(data).toml()
            elif fmt == HierarchicalFormat.CBOR2:
                self.__data = self.__HierarchicalFrom(data).cbor2()
            elif fmt == HierarchicalFormat.MSGPACK:
                self.__data = self.__HierarchicalFrom(data).messagepack()
            elif fmt == HierarchicalFormat.BSON:
                self.__data = self.__HierarchicalFrom(data).bson()
            elif fmt == HierarchicalFormat.UBJSON:
                self.__data = self.__HierarchicalFrom(data).ubjson()
            else:
                raise ValueError("Unable to detect file_data format")
        elif isinstance(data, dict):
            self.__data = data
        else:
            raise ValueError("Invalid file_data format")

    @staticmethod
    def detect_format(data: Union[str, bytes]) -> HierarchicalFormat:
        if not data or (isinstance(data, str) and not data.strip()):
            return HierarchicalFormat.UNKNOWN
        if isinstance(data, bytes):
            try:
                cbor2.loads(data)
                return HierarchicalFormat.CBOR2
            except Exception:
                pass
            try:
                messagepack.unpackb(data, raw=False)
                return HierarchicalFormat.MSGPACK
            except Exception:
                pass
            try:
                bson.BSON(data).decode()
                return HierarchicalFormat.BSON
            except Exception:
                pass
            try:
                ubjson.loadb(data)
                return HierarchicalFormat.UBJSON
            except Exception:
                pass
        else:
            try:
                parser = etree.XMLParser(remove_blank_text=True)
                etree.fromstring(data.encode('utf-8'), parser)
                return HierarchicalFormat.XML
            except etree.XMLSyntaxError:
                pass
            try:
                json.loads(data)
                return HierarchicalFormat.JSON
            except json.JSONDecodeError:
                pass
            try:
                yaml_result = yaml.safe_load(data)
                if isinstance(yaml_result, (dict, list)) and data.strip():
                    if yaml_result or data.strip() in ('{}', '[]'):
                        return HierarchicalFormat.YAML
            except yaml.YAMLError:
                pass
            try:
                toml.loads(data)
                return HierarchicalFormat.TOML
            except toml.TomlDecodeError:
                pass
            try:
                bdata = data.encode('utf-8')
                try:
                    cbor2.loads(bdata)
                    return HierarchicalFormat.CBOR2
                except Exception:
                    pass
                try:
                    messagepack.unpackb(bdata, raw=False)
                    return HierarchicalFormat.MSGPACK
                except Exception:
                    pass
                try:
                    bson.BSON(bdata).decode()
                    return HierarchicalFormat.BSON
                except Exception:
                    pass
                try:
                    ubjson.loadb(bdata)
                    return HierarchicalFormat.UBJSON
                except Exception:
                    pass
            except Exception:
                pass
        return HierarchicalFormat.UNKNOWN

    @property
    def to(self):
        return HierarchicalData.__HierarchicalTo(self.__data)

    def get(self, key, default=None):
        return self.__data.get(key, default)

    def __getitem__(self, key):
        if key in self.__data:
            return self.__data[key]
        raise KeyError(key)

    def __setitem__(self, key, value):
        self.__data[key] = value

    def __delitem__(self, key):
        if key in self.__data:
            del self.__data[key]
        else:
            raise KeyError(key)

    def __len__(self):
        return len(self.__data)

    def __contains__(self, key):
        return key in self.__data

    def __str__(self):
        return str(self.__data)
