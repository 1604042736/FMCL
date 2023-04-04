import qtawesome as qta

from .News import News


def functionInfo():
    return {
        "name": "新闻",
        "icon": qta.icon("fa.newspaper-o")
    }


def main():
    news = News()
    news.show()
