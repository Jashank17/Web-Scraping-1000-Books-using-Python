from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd
all_url=['https://books.toscrape.com/catalogue/page-1.html']
current_url= "https://books.toscrape.com/catalogue/page-1.html"
base="https://books.toscrape.com/catalogue/"
respons=requests.get(current_url)
while respons.status_code == 200:
    data=bs(respons.text,'html.parser')
    url=data.find(class_="next")
    if url is None:
        break
    next_url=base + url.a["href"]
    
    all_url.append(next_url)
    current_url=next_url
    respons=requests.get(current_url)

nu=[]
for ele in all_url:
    response=requests.get(ele)
    data=bs(response.text,'html.parser')
    find=data.find_all(class_="product_pod")
    base="https://books.toscrape.com/catalogue/"
    for i in find:
        new_url= base+ i.h3.a["href"]
        nu.append(new_url)
book_details=[]       
for n in nu:
    response=requests.get(n)
    data=bs(response.text,'html.parser')
    title=data.h1.string
    price = data.find(class_="price_color").string
    quantity=data.find(class_="instock availability").contents[-1].strip()
    quantity=re.search('\d+',quantity).group()
    price=re.search('[\d.]+',price).group()
    book_details.append([title,price,quantity])
    df=pd.DataFrame(book_details,columns=["Name of the Book","Price of the book", "Quantity of book available"])
df.to_csv("books6.csv",index=False)

        