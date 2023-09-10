import os
import re
from zipfile import *

tasks = [
    {
        "target": "Functions",
        "path": "../FMCL/Functions",
        "filter": [
            r".*?\.ui",
            r".*?\.ts",
            r".*?__pycache__.*?"
        ]
    },
    {
        "target": "Translations",
        "path": "../FMCL/Translations",
        "filter": [
            r".*?\.ts"
        ]
    }
]


def dotask(task: dict):
    zippath = f"../Pack/{task['target']}Pack.zip"
    zipfile = ZipFile(zippath, "w", ZIP_DEFLATED)
    for root, _, files in os.walk(task["path"]):
        for file in files:
            filepath = f"{root}/{file}"
            for f in task["filter"]:
                if re.match(f, filepath):
                    break
            else:
                print(filepath)
                zipfilepath = filepath.replace(task["path"], "")[1:]
                zipfile.write(filepath, zipfilepath)
    zipfile.close()
    with open(f"../Pack/{task['target']}.py", mode="w")as file:
        file.write(
            f"""import io
zipfile_bytes=io.BytesIO({open(zippath,mode='rb').read()})""")


def main():
    for task in tasks:
        dotask(task)
        print("="*64)


if __name__ == "__main__":
    main()
