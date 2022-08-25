from importlib import import_module
import os
import Globals as g
import Translate.English as English
import Translate.Chinese as Chinese

all_languages = ("简体中文", "English")
language_map = {
    "简体中文": Chinese,
    "English": English
}

try:
    for i in os.listdir("FMCL/Language"):
        if i != "__init__.py" and i.endswith(".py"):
            name = os.path.splitext(i)[0]
            module = import_module(f"FMCL.Language.{name}")
            config = module.config
            display_name = config["display_name"]  # 显示在设置里的名称
            if display_name in all_languages:  # 如果该语言已经有了
                # 拓展这个语言
                language_map[display_name].translate |= module.translate
            else:
                # 添加这个语言
                all_languages += (display_name,)
                language_map[display_name] = module

    if not os.path.exists("FMCL/__init__.py"):
        with open("FMCL/__init__.py", "w", encoding='utf-8'):
            pass

    if not os.path.exists("FMCL/Language/__init__.py"):
        with open("FMCL/Language/__init__.py", "w", encoding='utf-8'):
            pass
except:
    pass

lang = language_map[g.language]


def tr(text) -> str:
    """翻译text"""
    if text in lang.translate:
        return lang.translate[text]
    else:
        g.logapi.error(f'"{text}"没有{g.language}翻译')
        return text
