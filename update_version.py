import os
import re

with open("pyproject.toml", "rt", encoding="utf-8") as f:
    for line in f.read().splitlines():
        if line.startswith("version"):
            version_toml = line.split("=")[1].strip()[1:-1]
            break

with open("format_flex/__init__.py", "rt", encoding="utf-8") as f:
    for line in f.read().splitlines():
        if line.startswith("__version__"):
            version_package = line.split("=")[1].strip()[1:-1]

print(f'pyptoject.toml: {version_toml}')
print(f'format_flex/__init__.py: {version_package}')
if version_toml != version_package:
    print("Incorrect Version")

new_version = input("Enter new version: ")

print(f'Version: {version_toml} => {new_version}')
check = input('Update version(y,n): ')
if check == "y":
    for file in ['pyproject.toml', 'format_flex/__init__.py']:
        with open(file, "rt", encoding="utf-8") as f:
            data = f.read().replace(version_toml, new_version)
        with open(file, "wt", encoding="utf-8") as f:
            f.write(data)
else:
    print("Cancel update")
