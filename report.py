import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

url = "https://www.aniceholiday.com.tw/menu"
Data = requests.get(url)
Data.encoding = "utf-8"
sp = BeautifulSoup(Data.text, "html.parser")
result = sp.select(".item-inner li")#在.item-inner這個class尋找
#result=sp.select(".item-inner li")

for item in result:
  name = item.find("div", class_="col1").text #飲料名稱
  price = item.find("div", class_="col2").text #價錢
  if item.find("div", class_="col3").find("span", class_="icon1"):
    hot = "hot"
  else:
    hot ="nohot" #有沒有熱飲提供的概念
  #print(name+" "+price+" "+hot+"\n\n") 
  docs = [
  {
  "class": " ",
  "name": name,
  "price" : price,
  "hotOrNot" : hot,
  }
  ]

  collection_ref = db.collection("drink")
  for doc in docs:
    collection_ref.add(doc)

