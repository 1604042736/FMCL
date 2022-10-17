import os
import re


def getUiFiles(path: str) -> list:
    result = []
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            result.extend(getUiFiles(filepath))
        elif filename.endswith(".py"):
            content = open(filepath, encoding="utf-8").read()
            if "_translate" in content:
                result.append(filepath)
            else:
                chinese = re.finditer(r'[^"]"[\u4e00-\u9fa5]+"', content)
                for i in chinese:
                    print(f'警告:"{filepath}"中可能存在的未翻译内容:')
                    for index, code in enumerate(content.split("\n")):
                        if i.group() in code:
                            print(f"{index}|\t{code.strip()}")
                            break
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
