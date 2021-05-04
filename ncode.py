#!/usr/bin/python3
#entity015 ~ https://t.me/rzeee
import os
import sys
import filetype
import requests
import imagesize
from fpdf import FPDF
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool

def soup(code):
	u = f"https://nhentai.net/g/{code}"
	r = requests.get(u,headers=header,timeout=7)
	run(BeautifulSoup(r.content,'html.parser'))

def run(content):
	code = content.find("h3",id="gallery_id").text.replace("#","")
	os.mkdir(code)
	mangatitle = content.find(property='og:title')['content']
	gallery_id = content.find(property='og:image')['content'].split('/')[4]
	file_links = content.find_all('div',class_='thumb-container')
	file_count = len(file_links)

	print (f" ({code}) -> {mangatitle.strip()} ({file_count} Pages)")

	for index,value in enumerate(file_links,1):
		file_lnk = value.find_all('img')[1]['src']
		file_ext = file_lnk.split('.')[-1]
		file_url = f"https://i.nhentai.net/galleries/{gallery_id}/{index}.{file_ext}"
		file_dir = f"{code}/{str(index).zfill(len(str(file_count)))}.{file_ext}"
		dloads(file_dir,file_url)
		filter(file_dir,file_ext)
	merge(code)
	print(f" Saved {code}.pdf")

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
			with Pool(len(line)) as pool:
				pool.map(soup,line)
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
