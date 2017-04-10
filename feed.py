#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup, SoupStrainer
# from selenium import webdriver
import requests, re

##########
## http://stackoverflow.com/questions/25539330/speeding-up-beautifulsoup
session = requests.Session()
response = session.get("https://www.treasury.gov/resource-center/sanctions/OFAC-Enforcement/Pages/OFAC-Recent-Actions.aspx")
# strainer = SoupStrainer("table")
strainer = SoupStrainer("table", {"class": "ms-rteTable-default"})

soup = BeautifulSoup(response.content, "lxml", parse_only=strainer)

# print(soup.get_text)
row_data = []
for row in soup.find_all("tr"):
    temp = []
    cols = row.find_all("td")
    cols = [ele.text.strip() for ele in cols]
    row_data.append(cols)