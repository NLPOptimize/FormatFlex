from format_flex import HData

# HData can be initialized with either a filename or a JSON, XML, YAML, or TOML string.
with open("sample.json", "rt", encoding="utf-8") as f:
    json_text = f.read()
hdata = HData(json_text)

print(hdata.to.cbor2("./output/sample").summary)
print(hdata.to.msgpack("./output/sample").summary)
print(hdata.to.bson("./output/sample").summary)
print(hdata.to.ubjson("./output/sample").summary)
