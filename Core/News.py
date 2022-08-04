from bs4 import BeautifulSoup
import requests
from Core import CoreBase
import Globals as g


class News(CoreBase):

    def get_news(self) -> list[dict]:
        """获取新闻"""
        return self.get_news_way1()

    def get_news_way1(self) -> list[dict]:
        """获取新闻的第一种渠道"""
        result = []
        url = "https://www.minecraftzw.com/category/news"
        g.logapi.info(f'获取来自"{url}"的新闻')
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        div = soup.find("div", class_="post-listing archive-box")
        for article in div.find_all("article"):
            a = article.find("a")
            article_url = a["href"]
            title = a.text
            description = article.find("div", class_="entry").find("p").text
            article_img_url = article.find("img")["src"]
            result.append({
                "article_url": article_url,
                "title": title,
                "description": description,
                "article_img_url": article_img_url
            })
            g.logapi.info(f"{article_url=}")
            g.logapi.info(f"{title=}")
            g.logapi.info(f"{description=}")
        return result

    def get_news_detail(self, info) -> None:
        """获取新闻细节"""
        url = info["article_url"]
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        info["article_body"] = soup.find("div", class_="entry")
