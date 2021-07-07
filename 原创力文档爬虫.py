# -*- coding: utf-8 -*-
# @Time ： 2021/7/7 19:40
# @E-mail：yuu_seeing@foxmail.com
# @Auth ： VerNe
# @File ： 原创力文档.py
# @IDE ：  PyCharm
import requests
import re
import json
from PIL import Image
import time
from fpdf import FPDF
import os


def getParameter():
    text_url = input('输入网址：')
    text_response = requests.get(url=text_url, headers=headers).text
    actual_page = int(re.search('actual_page: (\d+), //真实页数', text_response).group(1))
    aid = re.search('aid: (\d+), //解密后的id', text_response).group(1)
    view_token = re.search('view_token: \'(.*?)\'', text_response).group(1)
    title = re.search('title: \'(.*?)\', //文档标题', text_response).group(1)
    return actual_page, aid, view_token, title


def combinePictures2Pdf(path, pdfName, allNum):
    # 合并图片为pdf
    print('Start combining the pictures...')
    pagenum = 1
    file_name = path + str(pagenum) + '.png'
    cover = Image.open(file_name)
    width, height = cover.size
    pdf = FPDF(unit="pt", format=[width, height])
    while allNum >= pagenum:
        try:
            print('combining picture ' + str(pagenum))
            file_name = path + str(pagenum) + '.png'
            pdf.add_page()
            pdf.image(file_name, 0, 0)
            pagenum += 1
        except Exception as e:
            print(e)
            break
    pdf.output(pdfName, "F")


def removePictures(path, allNum):
    pagenum = 1
    while allNum >= pagenum:
        try:
            print('deleting picture ' + str(pagenum))
            file_name = path + str(pagenum) + '.png'
            os.remove(file_name)
            pagenum += 1
        except Exception as e:
            print(e)
            break


def downloadPictures(aid, vie_token, page):
    params = {
        'project_id': '1',
        'aid': aid,
        'view_token': vie_token,
        'page': page
    }
    response = requests.get(url=url, headers=headers, params=params).text
    # print(response)
    response_json = re.search('jsonpReturn\((.*?)\);', response).group(1)
    data = json.loads(response_json)['data']
    for i in data.items():
        img_url = 'https:' + i[1]
        print(i[0], img_url)
        img_req = requests.get(url=img_url, headers=headers)
        file_name = path + str(i[0]) + '.png'
        f = open(file_name, 'wb')
        f.write(img_req.content)
        f.close()
        im = Image.open(file_name)
        im.save(file_name)
    time.sleep(5)


path = r''
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
url = 'https://openapi.book118.com/getPreview.html'
actual_page, aid, vie_token, title = getParameter()
print(title)
print(actual_page)
last = 0
for page in range(1, actual_page, 6):
    downloadPictures(aid, vie_token, page)
    last = page + 6

if last < actual_page or last == actual_page:
    downloadPictures(aid, vie_token, last)

pdfName = title + '.pdf'
combinePictures2Pdf(path, pdfName, actual_page)
time.sleep(0.5)
removePictures(path, actual_page)
