import os

root = os.path.abspath("..")

tasks = (
    [
        {
            "scanpath": [f"{root}/Core", f"{root}/Events"],
            "scanfile": [
                f"{root}/Kernel.py",
                f"{root}/Main.py",
                f"{root}/Setting.py",
                f"{root}/Window.py",
            ],
            "targetpath": f"{root}/FMCL/Translations/System",
        }
    ]
    + [
        {
            "scanpath": [f"{root}/FMCL/Functions/{i}"],
            "scanfile": [],
            "targetpath": f"{root}/FMCL/Functions/{i}/Translations",
        }
        for i in os.listdir(f"{root}/FMCL/Functions")
    ]
    + [
        {
            "scanpath": [f"{root}/FMCL/Help/{i}"],
            "scanfile": [],
            "targetpath": f"{root}/FMCL/Help/{i}/Translations",
        }
        for i in os.listdir(f"{root}/FMCL/Help")
    ]
    + [
        {
            "scanpath": [f"{root}/FMCL/Extras/FMCL/Functions/{i}"],
            "scanfile": [],
            "targetpath": f"{root}/FMCL/Extras/FMCL/Functions/{i}/Translations",
        }
        for i in os.listdir(f"{root}/FMCL/Extras/FMCL/Functions")
    ]
)


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
                    files.append(root + "/" + filename)
    files = list(map(os.path.abspath, files))
    print("\n".join(files))
    for lang in ("简体中文", "English"):
        if not os.path.exists(task["targetpath"]):
            os.makedirs(task["targetpath"])
        args = [
            "pylupdate5",
            " ".join(files),
            "-ts",
            f"{task['targetpath']}/{lang}.ts",
            "-noobsolete",
        ]
        os.system(" ".join(args))


def main():
    for task in tasks:
        dotask(task)
        print("=" * 64)


if __name__ == "__main__":
    main()
