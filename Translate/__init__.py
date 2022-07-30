import Globals as g
from importlib import import_module

all_languages = ("Chinese", "English")

if g.language != "Chinese":
    lang = import_module(f"Translate.{g.language}")


def tr(text) -> str:
    """翻译text"""
    if g.language == "Chinese":
        return text
    if text in lang.translate:
        return lang.translate[text]
    else:
        g.logapi.error(f'"{text}"没有{g.language}翻译')
        return text
