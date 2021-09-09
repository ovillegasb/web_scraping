import scrapy

"""
Module dedicated to extract information about publications in
ACS(American Chemistry Society).

"""

# XPaths

xpaths = {
    'decade': '//ul[contains(@class, "rlist")]/li/a/@href',
    'issue': '//ul[contains(@class, "rlist")]/li/div/a/@href',
    'articles': '//h5/a/@href',
    'title': '//h1/span/text()',
    'authors': ('//span[@class="hlFld-ContribAuthor"]/*/text() | //ul[@class="loa"]/li/span/span/text()'),
    'cite': '(//div[@class="article_header-cite-this"]/span/text() | //div[@class="article_header-epubdate"]/span/text())',
    'abstract': '//div[@id="abstractBox"]/p/text()',
    'doi': '//div[@class="article_header-doiurl"]/a/@href'
}


class SpiderEnfuel(scrapy.Spider):
    # Journal Energy & Fuels ACS

    # Referece name
    name = 'energyfuel'

    start_urls = [
        'https://pubs.acs.org/loi/enfuem'
    ]

    custom_settings = {
        'FEEDS': {
            'articles.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'indent': 0,
            }
        },
        'ROBOTSTXT_OBEY': True
    }

    def parse(self, response):
        links_decades = response.xpath(xpaths['decade']).getall()

        for link in links_decades:
            # print(link)
            yield response.follow(link, callback=self.parse_decade)

    def parse_decade(self, response):
        links_issues = response.xpath(xpaths['issue']).getall()

        for link in links_issues:
            # print(link)
            yield response.follow(link, callback=self.parse_issue)

    def parse_issue(self, response):
        links_articles = response.xpath(xpaths['articles']).getall()

        for link in links_articles:
            # print(link)
            yield response.follow(
                link,
                callback=self.parse_article,
                cb_kwargs={'url': response.urljoin(link)}
            )

    def parse_article(self, response, **kwargs):
        link = kwargs['url']
        title = response.xpath(xpaths['title']).get()
        abstract = response.xpath(xpaths['abstract']).getall()
        authors = response.xpath(xpaths['authors']).getall()
        cite = response.xpath(xpaths['cite']).getall()

        date = cite[-1]

        # cleanning
        abstract = ' '.join(abstract)
        authors = '; '.join(authors)

        yield {
            'title': title,
            'authors': authors,
            'date': date,
            'abstract': abstract,
            'url': link
        }
