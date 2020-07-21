from config_yaml import config
import requests
import bs4

class NewsPage:
    def __init__(self, news_site_uid, url):
        self._config = config()['news_sites'][news_site_uid]
        self._queries = self._config['queries']
        self._html = None
        self._visit(url)
        self._url = url

    def _select(self, query_string):
        return self._html.select(query_string)

    def _visit(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            self._html = bs4.BeautifulSoup(response.text, 'html.parser')
        except:
            self._html = bs4.BeautifulSoup('')


class HomePage(NewsPage):
    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid,url) #se hace hijo de NewsPage

    @property
    def article_links(self):
        link_list = []
        for link in self._select(self._queries['homepage_article_links']):
            if link and link.has_attr('href'):
                link_list.append(link)

        return set(link['href'] for link in link_list)

class ArticlePage(NewsPage):
    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url) #se hace hijo de NewsPage

    def url(self):
        return self._url


    @property
    def body(self):
        result = self._select(self._queries['article_body']) #se agrega a la estructura //:'news_page´/news_site_uid/queries/article_body

        return result[0].text if len(result) else '' #solo lanza el primer resultado y solo si es que hay, si no lanza ''

    @property
    def title(self):
        result = self._select(self._queries['article_title']) #se agrega a la estructura //:'news_page´/news_site_uid/queries/article_title

        return result[0].text if len(result) else ''
