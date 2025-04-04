# FormatFlex

**FormatFlex** is a flexible Python library designed to seamlessly handle various text and data formats.

## Supported Data Formats

### Hierarchical Data (`HData`)
- XML
- JSON
- YAML
- TOML
- CBOR2
- MSGPACK
- BSON
- UBJSON

### Tabular Data (`TData`)
- CSV
- Excel
- Parquet
- ORC
- Feather
- HDF5

### Serialization (`GData`)
- Pickle
- Dill
- Cloudpickle
- Joblib

## Installation
```bash
pip install format_flex
```

## Usage

### Hierarchical Data Example (`HData`)

```python
from format_flex import HData

with open("sample/sample.json", "rt", encoding="utf-8") as f:
    data = f.read()

hdata = HData(data)
save_path = "./output/hdata_example"

# Convert and save in various formats
print(hdata.to.xml(save_path).summary)
print(hdata.to.json(save_path).summary)
print(hdata.to.yaml(save_path).summary)
print(hdata.to.toml(save_path).summary)
print(hdata.to.bson(save_path).summary)
print(hdata.to.cbor2(save_path).summary)
print(hdata.to.msgpack(save_path).summary)
print(hdata.to.ubjson(save_path).summary)
```

### Tabular Data Example (`TData`)

```python
from format_flex import TData

tdata = TData("sample/music_dataset.csv")
save_path = "./output/tdata_example"

print(tdata.to.csv(save_path).summary)
print(tdata.to.excel(save_path).summary)
print(tdata.to.parquet(save_path).summary)
print(tdata.to.orc(save_path).summary)
print(tdata.to.feather(save_path).summary)
print(tdata.to.hdf5(save_path).summary)
```

### Serialization Example (`GData`)

```python
import numpy as np
from format_flex import GData

data = {
    "name": "Alice",
    "age": 30,
    "scores": [95, 87, 78],
    "numbers": np.random.random((10, 10)),
    "details": {
        "hobbies": ["reading", "cycling", "hiking"],
        "active": True,
        "balance": 1234.56
    }
}

save_path = "./output/gdata_example"
gdata = GData(data)

print(gdata.to.pickle(save_path).summary)
print(gdata.to.dill(save_path).summary)
print(gdata.to.cloudpickle(save_path).summary)
print(gdata.to.joblib(save_path).summary)
```

## License

This project is licensed under the MIT License.

