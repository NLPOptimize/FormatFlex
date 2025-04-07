from format_flex import HData

filename = "json_5MB"
with open(f"{filename}.json", "rt", encoding="utf-8") as f:
    json_text = f.read()
hdata = HData(json_text)

print(hdata.to.cbor2(f"./output/{filename}").summary)
print(hdata.to.msgpack(f"./output/{filename}").summary)
# print(hdata.to.bson(f"./output/{filename}").summary)
print(hdata.to.ubjson(f"./output/{filename}").summary)
