#Importing necessary library

from bs4 import BeautifulSoup
import requests as req
import numpy as np
import pandas as pd
import os
import lxml
import mysql.connector

#Image directory
img_dir=r"celebrityImg"

mydb=mysql.connector.connect(host="localhost",user="root",passwd="Vikas1998",database="moviecelebrity")
mycursor=mydb.cursor()

#define function to add data to database
def insertTodb(l):
	for data in l:
		try:
			mycursor.execute("INSERT INTO celebrity(ranking,name,movie,personality_trait,image_location) VALUES ('{}','{}','{}','{}','{}')".format(data[0],data[1],data[2],data[3],data[4]))
		except Exception as e:
			pass
		mydb.commit()

#list
l=[]

#Define a function to extract required data from  given website
def ExtractFromWeb(web_link):
	global l
	res=req.get(web_link)
	soup=BeautifulSoup(res.text,'lxml')
	
	for div in soup.find_all('div',class_='lister-item mode-detail'):
		div1=div.find('div',class_="lister-item-content")
		name=div1.a.text.split('\n')[0].lstrip()
		rank=int(div1.h3.span.text.split('.')[0].lstrip())
		movie=div1.p.a.text.split('\n')[0].lstrip()
		div2=div.find('div',class_="lister-item-image")
		img_url=div2.a.img['src'].split('/n')[0]
		trait=div1.p.text.split('\n')[1].lstrip().split('|')[0]
		img_location=f"{name}.jpg"
		x=[rank,name,movie,trait,img_location,img_url]
		l.append(x)





#Crawling on web 1
ExtractFromWeb("https://www.imdb.com/list/ls068010962/")
print("Page 1, Done..")

#Crawling on web 2
ExtractFromWeb("https://www.imdb.com/list/ls068010962/?sort=list_order,asc&mode=detail&page=2")
print("Page 2, Done..")


#make directory and download images to directory
os.mkdir("celebrityImg")
for data in l:
	img_data=req.get(data[5]).content
	with open("celebrityImg/"+data[1]+".jpg",'wb+') as f:
		f.write(img_data)

#Insert data to database
insertTodb(l)


print("Done")


