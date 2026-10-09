import csv
import re

import requests
from bs4 import BeautifulSoup
from lxml import etree, html

constant_table_url = 'https://wiki.rotaeno.cn/%E5%AE%9A%E6%95%B0%E8%AF%A6%E8%A1%A8'
constant_table_xpath = '/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/table[2]'

deprecate_table_url = 'https://wiki.rotaeno.cn/%E9%99%90%E6%97%B6%E4%B8%8A%E6%9E%B6%E6%9B%B2%E7%9B%AE%E5%88%97%E8%A1%A8'
deprecate_table_xpath = '/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/table[1]'

id_from_href = r'^\/File:Songs_(.*)\.png$'

def get_element(url: str, xpath: str) -> BeautifulSoup:
    r = requests.get(url)

    dom = etree.HTML(r.content)
    table = dom.xpath(xpath)

    table_str = html.tostring(table[0], method="html", encoding="utf-8")
    return BeautifulSoup(table_str, "lxml")

def parse_table(soup: BeautifulSoup) -> list[list]:
    table = []

    body = soup.find("tbody")
    for song in body.find_all('tr', recursive=False):
        if row := song.find_all('td', recursive=False):
            info = [re.match(id_from_href, row[0].find('a')['href'])[1]]
            info += (cell.get_text(strip=True) for cell in row[1:])
            table.append(info)

    return table

def write_csv(file_name: str, table: list[list]) -> None:
    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(table)


if __name__ == '__main__':
    constant_table = get_element(constant_table_url, constant_table_xpath)
    constant_table_parsed = parse_table(constant_table)
    write_csv('constant.csv', constant_table_parsed)
    
    deprecate_table = get_element(deprecate_table_url, deprecate_table_xpath)
    deprecate_table_parsed = parse_table(deprecate_table)
    write_csv('deprecated.csv', deprecate_table_parsed)
