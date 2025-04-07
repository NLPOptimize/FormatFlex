# FormatFlex

## Installation

```bash
pip install format-flex
```

## HData, TData, GData

* HData: Hierarchical Data
* TDate: Tabular Data
* GData: Generic Data


## Hierarchical

JSON, XML, YAML, and TOML formats can be converted interchangeably in text form. Additionally, conversion to Python's dictionary (`dict`) is supported. Hierarchical data is broadly divided into two categories:
First, human-readable text formats (XML, JSON, YAML, TOML) are converted into a `DataBlobText`.
Second, binary formats such as CBOR, MessagePack, BSON, and UBJSON are converted into a `DataBlob`.

For XML, JSON, YAML, and TOML formats, the `DataBlobText` class is returned, providing the methods `text`, `summary`, `size`, and `show`.
Calling `hdata.to.xml("test")` saves the data to `test.xml`.

### Text format
```python
from format_flex import HData

# HData can be initialized with either a filename or a JSON, XML, YAML, or TOML string.
hdata = HData("json_5MB.json")

print(hdata.to.xml().text)
print(hdata.to.json().text)
print(hdata.to.yaml().text)
print(hdata.to.toml().text)
```

### Binary format
Since it cannot be viewed anyway, the `text` method is unavailable.

For Msgpack, CBOR2, BSON, and UBJSON formats, a binary `DataBlob` is returned.  
`DataBlob` provides the methods `size`, `show`, and `summary`.


```python
from format_flex import HData
# `HData` can be initialized exactly as before, and it supports hierarchical binary serialization to produce smaller files.

filename = "json_5MB"
with open(f"{filename}.json", "rt", encoding="utf-8") as f:
    json_text = f.read()
hdata = HData(json_text)

print(hdata.to.cbor2(f"./output/{filename}").summary)
print(hdata.to.msgpack(f"./output/{filename}").summary)
# print(hdata.to.bson(f"./output/{filename}").summary)
print(hdata.to.ubjson(f"./output/{filename}").summary)

```

## Tabular
Since it cannot be viewed anyway, the `text` method is unavailable.

This is a class designed to store tabular data. It returns a `DataBlobTable`, which includes attributes `summary`, `size`, `show`, and additionally, a `path`. The `path` is the absolute path to the converted file.

```python
from format_flex import TData

# `tdata` is typically provided in CSV format.
tdata = TData("sample.csv")

print(tdata.to.csv("output/output").summary)
print(tdata.to.excel("output/output").summary)
print(tdata.to.parquet("output/output").summary)
print(tdata.to.orc("output/output").summary)
print(tdata.to.feather("output/output").summary)
```

## Generic

Generic serialization can be loaded or saved using pickle, dill, cloudpickle, and joblib.
The return format is DataBlobTable, which can accept any data type and is serializable.
pickle used zstandard level 19 while joblib used gzip level 9.


```python
from format_flex import GData
import cv2

img = cv2.imread("Lenna.png", cv2.IMREAD_GRAYSCALE)

item = [
    {"this": "is", "random": "object"},
    {"prime", 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37},
    {"image": img},
    {
        "text": "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    }
]
# Gdata can store any type of data.
gdata = GData(item)

print(gdata.to.pickle("output/output").summary)
print(gdata.to.joblib("output/output").summary)
print(gdata.to.cloudpickle("output/output").summary)
print(gdata.to.dill("output/output").summary)

```

## TODO (help me)
- [ ] HDF5 is not working.
- [ ] We want to integrate the parser of this package as a C++ library.


## Reference

* https://gist.github.com/jcrist/de29815389eaed4eaf5b24fbcfdab5f0
* https://jsonchecker.com/
* https://microsoftedge.github.io/Demos/json-dummy-data/
