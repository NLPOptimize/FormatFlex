from format_flex import TData

tdata = TData("sample.csv")

print(tdata.to.csv("output/output").summary)
print(tdata.to.excel("output/output").summary)
print(tdata.to.parquet("output/output").summary)
print(tdata.to.orc("output/output").summary)
print(tdata.to.feather("output/output").summary)
