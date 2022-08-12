import Globals as g
import Translate.English as English

all_languages = ("简体中文", "English")
language_map = {
    "简体中文": "Chinese",
    "English": "English"
}
language = language_map[g.language]

if language == "English":
    lang = English


def tr(text) -> str:
    """翻译text"""
    if language == "Chinese":
        return text
    if text in lang.translate:
        return lang.translate[text]
    else:
        g.logapi.error(f'"{text}"没有{language}翻译')
        return text
