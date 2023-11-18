import os
import re
from zipfile import *

root=os.path.abspath("..")

tasks = [
    {
        "target": "Functions",
        "path": f"{root}/FMCL/Functions",
        "filter": [
            r".*?\.ui",
            r".*?\.ts",
            r".*?__pycache__.*?"
        ]
    },
    {
        "target": "Translations",
        "path": f"{root}/FMCL/Translations",
        "filter": [
            r".*?\.ts"
        ]
    }
]


def dotask(task: dict):
    zippath = f"{root}/Pack/{task['target']}Pack.zip"
    zipfile = ZipFile(zippath, "w", ZIP_DEFLATED)
    for dirpath, _, files in os.walk(task["path"]):
        for file in files:
            filepath = f"{dirpath}/{file}"
            for f in task["filter"]:
                if re.match(f, filepath):
                    break
            else:
                print(filepath)
                zipfilepath = filepath.replace(task["path"], "")[1:]
                zipfile.write(filepath, zipfilepath)
    zipfile.close()
    with open(f"{root}/Pack/{task['target']}.py", mode="w")as file:
        file.write(
            f"""import io
zipfile_bytes=io.BytesIO({open(zippath,mode='rb').read()})""")


def main():
    for task in tasks:
        dotask(task)
        print("="*64)


if __name__ == "__main__":
    main()
