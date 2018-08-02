#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests_html import HTMLSession
from bs4 import BeautifulSoup
import csv


def extract_class_g_divs(r):
    soup = BeautifulSoup(str(r.content), 'html.parser')
    rhs = soup.find('div', {'id': 'rhs'})
    rhs.decompose()
    srgs = soup.find_all('div', {'class': 'srg'})
    test = "".join([str(each) for each in srgs])
    new_soup = BeautifulSoup(test, 'html.parser')
    class_g_divs = new_soup.find_all('div', {'class', 'g'})
    #drop all ol 1.cached 2.simlilar
    for each in new_soup.find_all('ol'):
        each.decompose()
    #drop people also search for
    for each in new_soup.find_all('h4'):
        each.decompose()
    return class_g_divs


html_elements = ""
keywords = 'toyota'
N = 25
element_count = 0
outer_break = False
for i in range(0, 30+1, 10):
    session = HTMLSession()
    response = session.get(f'https://www.google.com.au/search?q={keywords}&start={str(i)}')

    #output sourcecode to a string
    for each in extract_class_g_divs(response):
        html_elements += str(each)
        element_count += 1
        if element_count >= N:
            outer_break =True
            break
    if outer_break:
        break
sarasoup = BeautifulSoup(html_elements,'html.parser')
with open('test.html', 'w', encoding='utf-8') as f:
    f.write(html_elements)
# write  #, title, desc, link to a csv file
with open('names.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['rank', 'link','title','desc']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for rank, each in enumerate(sarasoup.find_all('div', {'class':'g'})):
        link = each.div.div.h3.a['href']
        title = each.div.div.h3.string
        desc_list = each.div.div.div.div.find('span',{'class':'st'}).contents
        desc =""
        for each in desc_list:
            desc+=str(each)
        desc = desc.replace('<em>', '').replace('</em>','')
        print(rank,link,title,desc)
        writer.writerow({'rank': str(rank+1), 'link': link, 'title': title, 'desc': desc})