import mysql.connector as ml
import pandas as pd
import openpyxl
from sqlalchemy import create_engine
import mysql
import urllib.request as ul
from bs4 import BeautifulSoup

#function to read html data from website
def read_data(webUrl):
    req=ul.Request(webUrl,headers={'User-Agent': 'Mozilla/5.0'})
    cl=ul.urlopen(req)
    htmldata=cl.read()
    soup=BeautifulSoup(htmldata,'html.parser')
    return soup

#connect python to mysql 
conc=ml.connect(host="localhost",user="root",passwd="9896",database="db")

#check status
if conc.is_connected():
    print("sucessfully connected")

else:
    print("Not connected")

#create engine
engine=create_engine("mysql+mysqlconnector://root:9896@localhost/db")
cur=conc.cursor(buffered=True)

#read data from excel using pandas
data= pd.read_excel("C:\Python\Blackcoffer\input.xlsx")

#feed the data to sql table
data.to_sql(name='inputs',con=engine, if_exists='fail',index=False)
cur.commit()

#query to get the data from sql table as input
q="select * from inputs"
cur.execute(q)
inp=cur.fetchall()

#web scrapping
for i in range(170):
    
    webUrl=inp[i][1]
    
    soup=read_data(webUrl)

    #find all the elements with class td-post-content
    itemlocator=soup.findAll('div',{"class":"td-post-content"})

    #open txt file to write desired elements 
    f = open(url_id+".txt", "w", encoding="utf-8")

    #find and write title in txt file
    for title in soup.findAll('title'):
        f.write(title.text)

    for items in itemlocator:

        #write various elements in the txt file if exist
        try:
            h1container=items.findAll("h1")
            h1=h1container[0].text
            f.write(h1)

        except IndexError:
            print("No h1 in the class")

        try:
            h2container=items.findAll("h2")
            h2=h2container[0].text
            f.write(h2)

        except IndexError:
            print("No h2 in the class")
    
        try:
            h3container=items.findAll("h3")
            h3=h3container[0].text
            f.write(h3)

        except IndexError:
            print("No h3 in the class")

        try:
            h4container=items.findAll("h4")
            h4=h4container[0].text
            f.write(h4)

        except IndexError:
            print("No h4 in the class")

        try:
            h5container=items.findAll("h5")
            h5=h5container[0].text
            f.write(h5)

        except IndexError:
            print("No h5 in the class")

        try:
            h6container=items.findAll("h6")
            h6=h6container[0].text
            f.write(h6)

        except IndexError:
            print("No h6 in the class")
    
        try:
            ulcontainer =items.findAll("ul")
            ul= ulcontainer[0].text
            f.write(ul)

        except IndexError:
            print("No ul in the class")

        pcontainer=items.findAll("p")
        p=pcontainer[0].text

        f.write(p)
        f.close()
        
cur.close()


