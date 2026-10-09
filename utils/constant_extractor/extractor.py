import csv
import re

import requests
from bs4 import BeautifulSoup
from lxml import etree, html

constant_table = 'https://wiki.rotaeno.cn/%E5%AE%9A%E6%95%B0%E8%AF%A6%E8%A1%A8'
table_xpath = '/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/table[2]'
id_from_href = r'^\/File:Songs_(.*)\.png$'


r = requests.get(constant_table)

dom = etree.HTML(r.content)
table = dom.xpath(table_xpath)

table_str = html.tostring(table[0], method="html", encoding="utf-8")
soup = BeautifulSoup(table_str, "lxml")

constants = []

body = soup.find("tbody")
for song in body.find_all('tr', recursive=False):
    if row := song.find_all('td', recursive=False):
        info = [re.match(id_from_href, row[0].find('a')['href'])[1]]
        info += (cell.get_text(strip=True) for cell in row[1:])
        constants.append(info)

with open('constant.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(constants)
