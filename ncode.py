#!/usr/bin/python3
#entity015 ~ https://t.me/rzeee
import os
import sys
import filetype
import requests
import threading
import imagesize
from fpdf import FPDF
from bs4 import BeautifulSoup

def soup(code):
	u = f"https://nhentai.net/g/{code}"
	r = requests.get(u,headers=header,timeout=7)
	run(BeautifulSoup(r.content,'html.parser'))

def run(content):
	try:
		code = content.find(id="gallery_id").find(text=True,recursive=False)
		os.mkdir(code)
		gallery_id = content.find(property='og:image')['content'].split('/')[4]
		file_links = content.find_all('div',class_='thumb-container')
		file_count = len(file_links)

		for index,value in enumerate(file_links,1):
			file_lnk = value.find_all('img')[1]['src']
			file_ext = file_lnk.split('.')[-1]
			file_url = f"https://i.nhentai.net/galleries/{gallery_id}/{index}.{file_ext}"
			file_dir = f"{code}/{str(index).zfill(len(str(file_count)))}.{file_ext}"
			sys.stdout.write(" [%s] Downloading [%s/%s] ...\n" % (code,index,file_count))
			dloads(file_dir,file_url)
			filter(file_dir,file_ext)
		merge(code)
		print(f" Saved {code}.pdf")
	except Exception as e:
		print(e)

def dloads(path,url):
	image = requests.get(url,headers=header,timeout=7)
	open(path,'wb').write(image.content)

def filter(path,ext):
	real_ext = filetype.guess(path).extension
	if(real_ext != ext):
		newpath = f"{path.split('.')[0]}.{real_ext}"
		os.rename(path,newpath)

def merge(code):
	papers = [986,1276]
	images = sorted(os.listdir(code))
	file_pdf = FPDF(orientation="P",unit="pt",format=papers)
	file_out = f"{code}.pdf";
	for index,image in enumerate(images,1):
		path = f"{code}/{image}"
		width,height = imagesize.get(path)
		if(width > height):
			x = 0
			w = papers[0]
			h = int((w/width) * height)
			y = int((papers[1]-h) / 2)
		elif(width < height):
			y = 0
			h = papers[1]
			w = int((h/height) * width)
			x = int((papers[0]-w) / 2)
		file_pdf.add_page()
		file_pdf.image(path,x,y,w,h)
	file_pdf.output(file_out,"F")

def main():
	try:
		os.system("clear" if os.name=="posix" else "cls")
		print(banner)
		i = input("−−$ ")
		if i == "1":
			code = input("Code: ")
			soup(code)
		elif i == "2":
			file = input("List: ")
			line = open(file).read().splitlines()
			args = []
			[args.append(x) for x in line if x]
			a = 0
			b = 3
			count = len(args)
			while count > 0:
				threads = []
				for i in range(a,b):
					t = threading.Thread(target=soup,args=(args[i],))
					threads.append(t)
				for t in threads:
					t.start()
				for t in threads:
					t.join()
				count-=3
				if count < 3:
					a+=3
					b+=count
				else:
					a+=3
					b+=3
		elif i == "0":
			exit("Exit.")
		else: exit("Wrong input.")
	except KeyboardInterrupt:
		exit("\nExit.")

TEA = "\033[1;32m"
RED = "\033[1;31m"
SUN = "\033[1;33m"
END = "\033[0;00m"
banner = f"""{RED}
     _   ________          __   
    / | / / ____/___  ____/ /__ 
   /  |/ / /   / __ \/ __  / _ \\
  / /|  / /___/ /_/ / /_/ /  __/
 /_/ |_/\____/\____/\__,_/\___/
{SUN}
 ｢ Nuke Code Download As PDF ｣
          Entity015 ♥
{TEA}
 1. Single
 2. Multi
 0. Exit
{END}"""
header = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
main()
