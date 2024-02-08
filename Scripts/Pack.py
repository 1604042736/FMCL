import os
import re
from zipfile import *

root = os.path.abspath("..")

tasks = [
    {
        "target": "Default",
        "path": f"{root}/FMCL",
        "filter": [
            r".*?\.ui",
            r".*?\.ts",
            r".*?latest.log",
            r".*?settings.json",
            r".*?/__pycache__.*?",
            r".*?/Skin.*?",
            r".*?/Default.*?",
            r".*?/Temp.*?",
            r".*?/Test.*?",
        ],
    }
]


def dotask(task: dict):
    zippath = f"{root}/Pack/{task['target']}Pack.zip"
    zipfile = ZipFile(zippath, "w", ZIP_DEFLATED)
    for dirpath, _, files in os.walk(task["path"]):
        for file in files:
            filepath = f"{dirpath}/{file}"
            for f in task["filter"]:
                if re.match(f, filepath.replace("\\", "/")):
                    break
            else:
                print(filepath)
                zipfilepath = filepath.replace(task["path"], "")[1:]
                zipfile.write(filepath, zipfilepath)
    zipfile.close()
    with open(f"{root}/Pack/{task['target']}.py", mode="w") as file:
        file.write(
            f"""import io
zipfile_bytes=io.BytesIO({open(zippath,mode='rb').read()})"""
        )


def main():
    if not os.path.exists(f"{root}/Pack"):
        os.makedirs(f"{root}/Pack")
    with open(f"{root}/Pack/__init__.py", mode="w") as file:
        file.write("")
    for task in tasks:
        dotask(task)
        print("=" * 64)


if __name__ == "__main__":
    main()
