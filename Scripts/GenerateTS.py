import os


def getUiFiles(path: str) -> list:
    result = []
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            result.extend(getUiFiles(filepath))
        elif filename.endswith(".py"):
            if "_translate" in open(filepath, encoding="utf-8").read():
                result.append(filepath)
    return result


def main():
    ts_path = os.path.abspath("../Languages")
    if not os.path.exists(ts_path):
        os.makedirs(ts_path)
    ui_files = getUiFiles(os.path.abspath("../"))
    for lang in ("zh_CN.ts", "en.ts"):
        args = f"pylupdate5 {' '.join(ui_files)} -ts {ts_path}/{lang} -noobsolete"
        print(args)
        os.system(args)


if __name__ == "__main__":
    main()
