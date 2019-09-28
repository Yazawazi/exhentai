import requests
import os
import multiprocessing
from bs4 import BeautifulSoup
import time
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','Upgrade-Insecure-Requests':'1'}
cookies = {
	'igneous': "df9724040",
	'ipb_member_id': "4483572",
	'ipb_pass_hash': 'b1d7d5acd649a01a1643124c8a0918a8',
	'sk': '',
	'yay': '0'
}

def start():
	start_num = 0
	while True:
		url = "https://exhentai.org?page=" + str(start_num)
		site = requests.get(url, headers=headers, cookies=cookies)
		content = site.text
		soup = BeautifulSoup(content, 'lxml')
		hrefs = soup.find_all(class_ = 'glname')
		i = 0
		time.sleep(0.5)
		for href in hrefs:
			benzi = href.a.get('href')
			print('== 本子信息 ==')
			print('[!] 地址：' + benzi)
			benzi_url = benzi
			benzi_site = requests.get(benzi_url, headers=headers, cookies=cookies)
			benzi_content = benzi_site.text
			benzi_soup = BeautifulSoup(benzi_content, 'lxml')
			print('[!] 标题：' + benzi_soup.h1.get_text())
			print('[!] 分类：' + benzi_soup.find_all(id = "gdc")[0].div.get_text())
			print('[!] 作者：' + benzi_soup.find_all(id = "gdn")[0].a.get_text())
			print('[!] 时间：' + benzi_soup.find_all(class_ = "gdt2")[0].get_text())
			print('[!] 父元素：' + benzi_soup.find_all(class_ = "gdt2")[1].get_text())
			print('[!] 可见性：' + benzi_soup.find_all(class_ = "gdt2")[2].get_text())
			print('[!] 语种：' + benzi_soup.find_all(class_ = "gdt2")[3].get_text())
			print('[!] 大小：' + benzi_soup.find_all(class_ = "gdt2")[4].get_text())
			print('[!] 页数：' + benzi_soup.find_all(class_ = "gdt2")[5].get_text())
			print('[!] 收藏次数：' + benzi_soup.find_all(class_ = "gdt2")[6].get_text())
			time.sleep(0.5)
			print('== 下载本子 ==')
			# 进行判断到底有几页
			try:
				pageBig = int(benzi_soup.find_all(class_ = "ptt")[0].find_all('a')[-2].get_text())
			except:
				# 只有一页
				print('[@] 只有一页。')
				time.sleep(1)
				pics = benzi_soup.find_all(class_ = "gdtm")
				for pic in pics:
					i = i + 1
					pic_benzi = pic.a.get("href")
					pic_benzi_site = requests.get(pic_benzi, headers=headers, cookies=cookies)
					pic_benzi_content = pic_benzi_site.text
					pic_benzi_soup = BeautifulSoup(pic_benzi_content, 'lxml')
					pic_benzi_url = pic_benzi_soup.find_all(id="img")[0].attrs["src"]
					print('[$] 地址：' + pic_benzi_url)
					time.sleep(1)
					if not os.path.exists('./comic/' + benzi_soup.h1.get_text().replace('/', '斜杠')):
						os.mkdir('./comic/' + benzi_soup.h1.get_text())
					try:
						pic_benzi_response = requests.get(pic_benzi_url, headers=headers)
						with open("./comic/" + benzi_soup.h1.get_text().replace('/', '斜杠') + '/' + benzi_soup.h1.get_text().replace('/', '斜杠') + str(i) + '.jpg', "wb") as f:
							f.write(pic_benzi_response.content)
							f.flush()
					except:
						print('[#] 失败！正在重新尝试')
						time.sleep(0.5)
						pic_benzi_response = requests.get(pic_benzi_url, headers=headers)
						time.sleep(0.5)
						with open("./comic/" + benzi_soup.h1.get_text().replace('/', '斜杠') + '/' + benzi_soup.h1.get_text().replace('/', '斜杠') + str(i) + '.jpg', "wb") as f:
							f.write(pic_benzi_response.content)
							f.flush()
					else:
						print('[#] 完毕！')
			else:
				# 多页组合
				print('[@] 多页。')
				time.sleep(1)
				texts = '*' * pageBig
				a = 0
				for text in texts:
					text_url = benzi_url + "?p="+str(a)
					time.sleep(1)
					text_site = requests.get(text_url, headers=headers, cookies=cookies)
					text_content = text_site.text
					text_soup = BeautifulSoup(text_content, 'lxml')
					pics = benzi_soup.find_all(class_ = "gdtm")
					for pic in pics:
						i = i + 1
						pic_benzi = pic.a.get("href")
						time.sleep(1)
						pic_benzi_site = requests.get(pic_benzi, headers=headers, cookies=cookies)
						pic_benzi_content = pic_benzi_site.text
						pic_benzi_soup = BeautifulSoup(pic_benzi_content, 'lxml')
						pic_benzi_url = pic_benzi_soup.find_all(id="img")[0].attrs["src"]
						print('[$] 地址：' + pic_benzi_url)
						time.sleep(1)
						if not os.path.exists('./comic/' + benzi_soup.h1.get_text().replace('/', '斜杠')):
							os.mkdir('./comic/' + benzi_soup.h1.get_text().replace('/', '斜杠'))
						try:
							pic_benzi_response = requests.get(pic_benzi_url, headers=headers)
							with open("./comic/" + benzi_soup.h1.get_text().replace('/', '斜杠') + '/' + benzi_soup.h1.get_text().replace('/', '斜杠') + str(i) + '.jpg', "wb") as f:
								f.write(pic_benzi_response.content)
								f.flush()
						except:						
							print('[#] 失败！正在重新尝试')
							time.sleep(1)
							pic_benzi_response = requests.get(pic_benzi_url, headers=headers)
							time.sleep(1)
							with open("./comic/" + benzi_soup.h1.get_text().replace('/', '斜杠') + '/' + benzi_soup.h1.get_text().replace('/', '斜杠') + str(i) + '.jpg', "wb") as f:
								f.write(pic_benzi_response.content)
								f.flush()
						else:
							print("[#] 完毕！")
					a = a +1
		start_num = start_num + 1

start()
