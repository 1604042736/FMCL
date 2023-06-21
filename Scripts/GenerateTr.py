import json
import os
import re

filters = [
    r".*?\.git.*?",
    r".*?\.minecraft.*?",
    r".*?ui_.*?",
    r".*?_rc.*?",
    r".*?__pycache__.*?",
    r".*?release.*?",
    r".*?Languages.*?",
    r".*?Resources.*?",
    r".*?3dparty.*?"
]


def generate(target_path, save_path):
    translation = {}
    for root, dirs, files in os.walk(target_path):
        for file in files:
            file_path = os.path.join(root, file)
            name, ext = os.path.splitext(file_path)
            for filter in filters:
                if re.match(filter, file_path):
                    break
            else:
                if ext == ".py":
                    content = open(file_path, encoding="utf-8").read()
                    for match in re.finditer(r"_translate\((.*?)\)", content):
                        text = match.group(1)
                        if text[0] == "'" or text[0] == '"':
                            text = text[1:-1]
                        else:
                            continue
                        translation[text] = text
    if not translation:
        return
    for i in ("简体中文", "English"):
        path = os.path.join(save_path, "Translations")
        if not os.path.exists(path):
            os.makedirs(path)
        file_path = os.path.join(path, f"{i}.json")
        if os.path.exists(file_path):
            translation |= json.load(open(file_path, encoding="utf-8"))
        json.dump(translation,
                  open(file_path, encoding="utf-8", mode="w"),
                  sort_keys=True, ensure_ascii=False, indent=4)
    print(translation)


def main():
    for i in os.listdir("../FMCL/Functions"):
        generate(f"../FMCL/Functions/{i}", f"../FMCL/Functions/{i}")
    generate(f"../Core", f"../FMCL")


if __name__ == "__main__":
    main()
