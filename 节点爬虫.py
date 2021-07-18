# -*- coding: utf-8 -*-
# @Time ： 2021/7/15 21:06
# @E-mail：yuu_seeing@foxmail.com
# @Auth ： VerNe
# @File ： 节点爬虫.py
# @IDE ：  PyCharm
import lxml
from bs4 import BeautifulSoup
import requests
import chardet
import win32clipboard
import win32con
import os
from pip._internal import main

# x = ['bs4.BeautifulSoup', 'requests', 'chardet', 'win32clipboard', 'win32con']
# for i in x:
#     try:
#         if 'bs4' in i:
#             from bs4 import BeautifulSoup
#         else:
#             import i
#     except ModuleNotFoundError:
#         main(['install', i ])


def set_text(aString):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_TEXT, aString)
    win32clipboard.CloseClipboard()


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'}
results = requests.get(url='https://github.com/freefq/free', headers=header)
results.close()
results.encoding = chardet.detect(results.content)['encoding']
text = results.text
soup = BeautifulSoup(text, 'lxml')
vmss = soup.select('#readme > div.Box-body.px-5.pb-5 > article > p:nth-child(17)')[0]
vmss = str(vmss)
vmss = vmss.replace('<br/>', '\n')
vmss = vmss.replace('<p>', '\n')
set_text(vmss.encode('ansi'))
