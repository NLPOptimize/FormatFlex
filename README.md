
![FormatFlex_banner](https://github.com/user-attachments/assets/5dedcbbf-870c-4aa9-ac7d-6abb3474023d)

# FormatFlex

### **FormatFlex** is a flexible Python library designed to seamlessly handle various text and data formats.

#### (This repository welcomes as many pull requests (PRs) as possible. Your active contributions are greatly appreciated!)


## Supported Data Formats

Currently, it is largely divided into three categories: hierarchical, tabular, and general types. If there are other classification methods or missing parts in each type support, it would be better if you could leave it as an issue or send a PR.


[API USAGE](./docs/API_USAGE.md)

### Hierarchical Data (`HData`)
- [XML](https://en.wikipedia.org/wiki/XML)
- [JSON](https://en.wikipedia.org/wiki/JSON)
- [YAML](https://en.wikipedia.org/wiki/YAML)
- [TOML](https://en.wikipedia.org/wiki/TOML)
- [CBOR2](https://github.com/agronholm/cbor2)
- [MSGPACK](https://msgpack.org/)
- ~~BSON~~ 🆘
- [UBJSON](https://ubjson.org/)

### Tabular Data (`TData`)
- [CSV](https://docs.python.org/ko/3.13/library/csv.html)
- [Excel](https://www.microsoft.com/ko-kr/microsoft-365/excel)
- [Parquet](https://parquet.apache.org/)
- [ORC](https://orc.apache.org/)
- [Feather](https://arrow.apache.org/docs/python/feather.html)
- ~~HDF5~~ 🆘

### Serialization (`GData`)
- [Pickle](https://docs.python.org/3/library/pickle.html)
- [Dill](https://github.com/dill-format/dill)
- [Cloudpickle](https://github.com/cloudpipe/cloudpickle)
- [Joblib](https://joblib.readthedocs.io/en/stable/)

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

