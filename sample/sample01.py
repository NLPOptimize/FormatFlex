from format_flex import HData

# HData can be initialized with either a filename or a JSON, XML, YAML, or TOML string.
hdata = HData("sample.json")

print(hdata.to.xml().text)
print(hdata.to.json().text)
print(hdata.to.yaml().text)
print(hdata.to.toml().text)
