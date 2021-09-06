#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module dedicated to extract information about publications in ACS.

Orlando Villegas
orlando.villegas@univ-pau.fr
08/2021

"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import geckodriver_autoinstaller

geckodriver_autoinstaller.install()  # Check if the current version of geckodriver exists
                                     # and if it doesn't exist, download it automatically,
                                     # then add geckodriver to path


options = webdriver.FirefoxOptions()

# options.add_argument('--headless')
options.add_argument('--private-window')


driver = webdriver.Firefox(options=options)


# Journal Energy & Fuels ACS

url_home = 'https://pubs.acs.org'

url = f'{url_home}/loi/enfuem/'

driver.get(url)

# decade = driver.find_elements_by_xpath('//a[@class="tab__nav__item__link"]')
decade = driver.find_elements_by_xpath('//div[@class="loi tab loi-tab-1"]/div[@class="swipe__wrapper loi-list__wrapper"]/div[@class="scroll"]/ul/li/a')
years = driver.find_elements_by_xpath('//div[@class="loi tab loi-tab-2"]/div/div/ul/li/a')

# decade = content.find_elements_by_xpath('.//a[@class="tab__nav__item__link"]')
print(len(decade))

for d in decade:
    print(d.get_attribute('title'))
    print(d.get_attribute('href'))


print(len(years))
for y in years:
    print(y.get_attribute('title'))
    print(y.get_attribute('href'))


decade[0].click()
decade[1].click()
decade[2].click()
decade[3].click()
decade[4].click()

# driver.close()

exit()

pag = requests.get(url)


print('Status Code:')
print(pag.status_code)
print(pag.request.url)

# print(pag.text)
# print(pag.content)
# print(pag.headers)
# print(pag.request.headers)
# print(pag.request.method)

s = BeautifulSoup(pag.text, 'lxml')

# print(type(s))
# print(s.prettify())

Issues = s.find('ul', attrs={'class': 'rlist issue-items pane-sections row__equalize-children-height'}).find_all('li')

decade = s.find('ul', attrs={'class': 'rlist loi__list tab__nav swipe__list'}).find_all('li')
print([i.text for i in decade])

years = s.find('div', attrs={'class': 'tab__content'}).find_all('li')
print([i.text for i in years])

exit()
# issue = Issues[0]

# print(issue.find('a').get('href'))

links_issues = [issue.find('a').get('href') for issue in Issues]

# print(links_issues)

# 1er link

link = url_home + links_issues[0]

issue_articles = requests.get(link)

print('Status Code Issue')
print(issue_articles.status_code)
print(issue_articles.request.url)

s_issue_articles = BeautifulSoup(issue_articles.text, 'lxml')

articles_section = s_issue_articles.find('div', attrs={'class': 'toc'}).find_all('h5')

featured_articles = [article.find('a') for article in articles_section]

# print(featured_articles[0])

articles_links = [article.get('href') for article in featured_articles]

# print(articles_links[0])

# article_link = url_home + articles_links[0]

# article_page = requests.get(article_link)

# print('Status Code Article')
# print(article_page.status_code)
# print(article_page.request.url)

# s_article_page = BeautifulSoup(article_page.text, 'lxml')
# print(s_article_page.prettify())


def get_article_info(soup):
    title = soup.find('h1').find('span').text
    article_authors = soup.find('ul', attrs={'class': 'loa'}).find_all('li')
    authors = [author.find('span', attrs={'class': 'hlFld-ContribAuthor'}).text for author in article_authors]

    cite = soup.find('div', attrs={'class': 'article_header-cite-this'})

    abstract_page = soup.find('div', attrs={'class': 'article_content-left'}).find_all('p')
    abstract = ' '.join([p.text for p in abstract_page])

    article_subjects = soup.find('div', attrs={'class': 'article_header-taxonomy'})

    print('Title:')
    print(title)

    print('Authors:')
    print(', '.join(authors))

    # print('Abstract:', end='\n---------\n')
    # print(abstract)

    # print(article_subjects)

    # if article_subjects is not None:
    #     print('Subjects:', end='\n---------\n')
    #     for sub in article_subjects.find_all('a'):
    #         print(sub.get('title'))

    print('Cite:')
    print(cite.text)


def read_all_articles(home, links):
    for article in links:
        article_link = home + article

        try:
            article_page = requests.get(article_link)
            if article_page.status_code == 200:
                s_article_page = BeautifulSoup(article_page.text, 'lxml')

                get_article_info(s_article_page)

        except Exception as e:
            print('Error:')
            print(e)
            print('\n')
