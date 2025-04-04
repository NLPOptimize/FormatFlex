from format_flex import HData, TData, GData
import numpy as np


def test1():
    with open("sample/sample.json", "rt", encoding="utf-8") as f:
        data = f.read()

    hdata = HData(data)

    # hdata["tmp"] = {
    #     "a": 1,
    #     "b": None
    # }
    save_path = "./output/test"
    print(hdata.to.xml(save_path).summary)
    print(hdata.to.json(save_path).summary)
    print(hdata.to.yaml(save_path).summary)
    print(hdata.to.toml(save_path).summary)

    print(hdata.to.bson(save_path).summary)
    print(hdata.to.cbor2(save_path).summary)
    print(hdata.to.msgpack(save_path).summary)
    print(hdata.to.ubjson(save_path).summary)
    # print(hdata.get("tmp", 777))

    print(hdata)


def test2():
    tdata = TData("sample/sample.csv")

    save_path = "./output/test_table"
    print(tdata.to.csv(save_path).summary)
    print(tdata.to.excel(save_path).summary)
    print(tdata.to.parquet(save_path).summary)
    print(tdata.to.orc(save_path).summary)
    print(tdata.to.feather(save_path).summary)
    print(tdata.to.hdf5(save_path).summary)


def test3():
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
    save_path = "./output/test_generic"
    gdata = GData(data)
    print(gdata.to.pickle(save_path).summary)
    print(gdata.to.dill(save_path).summary)
    print(gdata.to.cloudpickle(save_path).summary)
    print(gdata.to.joblib(save_path).summary)


if __name__ == '__main__':
    test2()
