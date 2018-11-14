#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
一个批量下载人人网相册照片的工具，提供账号密码和相册地址即可。
'''
__author__ = 'S4kur4'

import re
import os
import sys
import json
import time
import requests
import argparse
from selenium import webdriver

# 动态输出消息
def stdout(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()

# 登录并获取requesttoken和_rtk以及Cookie
def Login(username, password):
	browser = webdriver.Chrome()
	stdout('[*] 正在登录\r')
	browser.get('http://www.renren.com')
	browser.find_element_by_id('email').send_keys(username)
	browser.find_element_by_id('password').send_keys(password)
	browser.find_element_by_id('login').click()
	time.sleep(3)
	cookie_raw = browser.get_cookies() # len(Cookie) = 18

	# 将selenium得到的原始cookie转化为dict对象_Cookie
	_Cookie = {}
	for item in cookie_raw:
		_Cookie[item['name']] = item['value']
	
	# 获取requesttoken、_rtk、Cookie
	header = {'Referer': 'http://www.renren.com/SysHome.do'}
	Cookie = ''
	for key, value in _Cookie.items():
		Cookie = Cookie + key + '=' + value + ';'
	header['Cookie'] = Cookie
	stdout('[*] 正在拉取首页\r')
	homepage = requests.get(url='http://www.renren.com/{}'.format(_Cookie['id']), headers=header, timeout=10).text
	requesttoken = re.search(r'requestToken\ \:\ \'(\-\d{10})\'', homepage).group(1)
	_rtk = re.search(r'_rtk\ \:\ \'(\w{8})\'', homepage).group(1)

	return requesttoken, _rtk, Cookie

# 获取相册所有照片的url
def Crawler(album_url, requesttoken, _rtk, Cookie):
	photolist = []
	header = {
	'Referer': album_url,
	'X-Requested-With': 'XMLHttpRequest',
	'Cookie': Cookie
	}
	
	stdout('[*] 正在拉取所有照片链接\r')
	page = 1
	data_url = album_url.rstrip('v7') + 'bypage/ajax/v7?page=1&pageSize=100&requestToken={}&_rtk={}'.format(requesttoken, _rtk)
	json_photolist = json.loads(requests.get(url=data_url, headers=header, timeout=10).text)
	pagesize = len(json_photolist['photoList'])
	for photo in json_photolist['photoList']:
		photolist.append(photo['url'])

	# 照片数大于100张，由于每页最多100条数据，因此循环拉取
	while 100 == pagesize:
		page = page + 1
		data_url = album_url.rstrip('v7') + 'bypage/ajax/v7?page={}&pageSize=100&requestToken={}&_rtk={}'.format(page, requesttoken, _rtk)
		json_photolist = json.loads(requests.get(url=data_url, headers=header, timeout=10).text)
		pagesize = len(json_photolist['photoList'])
		for photo in json_photolist['photoList']:
			photolist.append(photo['url'])
	
	return photolist

# 根据phoholist保存每一个照片
def Store(photolist, Cookie):
	album_name = os.getcwd() + '/Album_{}'.format(int(time.time()))
	if not os.path.exists(album_name):
		os.makedirs(album_name)
	print '[*] 此相册共有{}张照片'.format(len(photolist))

	for photo_url in photolist:
		i = photolist.index(photo_url)
		header = {'Cookie': Cookie}
		stdout('[*] 正在保存第{}张\r'.format(i+1))
		photo_data = requests.get(url=photo_url, timeout=10).content
		with open(album_name+'/{}.jpg'.format(i), 'wb') as photo:
			photo.write(photo_data)

	print '[+] 所有照片已保存至{}'.format(album_name)

# 接收参数
def Parse():
	parser = argparse.ArgumentParser(description='Example: crawler.py -u 12345@qq.com -p 123456 -a \\ http://photo.renren.com/photo/123456789/album-123456789/v7', add_help=False)
	option = parser.add_argument_group('Options')
	option.add_argument('-h', '--help', action='help', help='Show Help Message And Exit')
	option.add_argument('-u', '--username', dest='username', type=str, metavar='USERNAME', help='Specify RenRen Username')
	option.add_argument('-p', '--password', dest='password', metavar='PASSWORD', help='Specify Corresponding Password')
	option.add_argument('-a', '--album', dest='album_url', metavar='ALBUM_URL', help='Specify Album URL Of Yours Or Your Friends')
	
	args = parser.parse_args().__dict__

	if len(sys.argv) <= 4:
		msg = 'crawler.py: error: missing mandatory options (-u, -p, -a), use -h for help'
		sys.exit(msg)
	if not re.match(r'http\:\/\/photo\.renren\.com', args['album_url']):
		msg = msg = 'crawler.py: error: album url your specified is invalid'
		sys.exit(msg)
	
	return args

def main():
	try:
		args = Parse()
		requesttoken, _rtk, Cookie = Login(args['username'], args['password'])
		photolist = Crawler(args['album_url'], requesttoken, _rtk, Cookie)
		Store(photolist, Cookie)
	except Exception:
		msg = 'crawler.py: error: some unknown errors have occurred :-('

if __name__ == '__main__':
	main()
