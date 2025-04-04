# FormatFlex

## Installation

```bash
pip install format-flex
```

## Hierarchical Data Conversion and Storage

JSON, XML, YAML, and TOML formats can be converted interchangeably in text form.

For XML, JSON, YAML, and TOML formats, the `DataBlobText` class is returned, providing the methods `text`, `summary`, `size`, and `show`.
Calling `hdata.to.xml("test")` saves the data to `test.xml`.

```python
from format_flex import HData

# HData can be initialized with either a filename or a JSON, XML, YAML, or TOML string.
hdata = HData("sample.json")

print(hdata.to.xml().text)
print(hdata.to.json().text)
print(hdata.to.yaml().text)
print(hdata.to.toml().text)
```

For Msgpack, CBOR2, BSON, and UBJSON formats, a binary `DataBlob` is returned.  
`DataBlob` provides the methods `size`, `show`, and `summary`.

```python
from format_flex import HData

# HData can be initialized with either a filename or a JSON, XML, YAML, or TOML string.
with open("sample.json", "rt", encoding="utf-8") as f:
    json_text = f.read()
hdata = HData(json_text)

print(hdata.to.cbor2("./output/sample").summary)
print(hdata.to.msgpack("./output/sample").summary)
print(hdata.to.bson("./output/sample").summary)
print(hdata.to.ubjson("./output/sample").summary)
```
