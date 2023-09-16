import os

tasks = [
    {
        "scanpath": [
            "../Core",
            "../Events"
        ],
        "scanfile":[
            "../Kernel.py",
            "../Main.py",
            "../Setting.py",
            "../Window.py"
        ],
        "targetpath":"../FMCL/Translations"
    }
]+[
    {
        "scanpath": [f"../FMCL/Functions/{i}"],
        "scanfile":[],
        "targetpath":f"../FMCL/Functions/{i}/Translations"
    }for i in os.listdir("../FMCL/Functions")
]


def check_file(name: str):
    return name[-3:] == ".py"


def dotask(task: dict):
    files = []
    for file in task["scanfile"]:
        if check_file(file):
            files.append(file)
    for path in task["scanpath"]:
        for root, _, filenames in os.walk(path):
            for filename in filenames:
                if check_file(filename):
                    files.append(root+"/"+filename)
    files = list(map(os.path.abspath, files))
    print("\n".join(files))
    for lang in ("简体中文", "English"):
        args = [
            "pylupdate5",
            " ".join(files),
            "-ts",
            f"{task['targetpath']}/{lang}.ts"
        ]
        os.system(" ".join(args))


def main():
    for task in tasks:
        dotask(task)
        print("="*64)


if __name__ == "__main__":
    main()
