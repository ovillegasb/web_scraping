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

# Journal Energy & Fuels ACS

url_home = 'https://pubs.acs.org'

url = f'{url_home}/loi/enfuem/'

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

article_link = url_home + articles_links[0]

article_page = requests.get(article_link)

print('Status Code Article')
print(article_page.status_code)
print(article_page.request.url)

s_article_page = BeautifulSoup(article_page.text, 'lxml')
# print(s_article_page.prettify())

title = s_article_page.find('h1').find('span').text

print('Title')
print(title)

article_authors = s_article_page.find('ul', attrs={'class': 'loa'}).find_all('li')

authors = [author.find('span', attrs={'class': 'hlFld-ContribAuthor'}).text for author in article_authors]
print('Authors')
print(authors)

article_ref = s_article_page.find('div', attrs={'class': 'article_header-cite-this'})
print(article_ref.text)

abstract_page = s_article_page.find('div', attrs={'class': 'article_content-left'}).find_all('p')
abstract = ' '.join([p.text for p in abstract_page])

print(abstract)

article_subjects = s_article_page.find('div', attrs={'class': 'article_header-taxonomy'})
# print(article_subjects)

if article_subjects is not None:
    for sub in article_subjects.find_all('a'):
        print(sub.get('title'))
