import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

url = "https://www.aniceholiday.com.tw/contact"
Data = requests.get(url)
Data.encoding = "utf-8"
sp = BeautifulSoup(Data.text, "html.parser")
result = sp.select(".item-inner")#在.item-inner這個class尋找
#result=sp.select(".item-inner li")
info = ""
for item in result:
    add = item.find("dd", class_="icon1").text #地址
    pho = item.find("dd", class_="icon2").text #電話
    time = item.find("dd", class_="icon3").text #營業
    dan = item.find("dt").text #店面
    #info += dan +"\n"+ add +"\n"+ pho +"\n"+ time + "\n\n"
#print(info)
    docs = [
    {
    "name": dan,
    "address": add,
    "phone" : pho,
    "time" : time,
    }
    ]
    collection_ref = db.collection("set")
    for doc in docs:
        collection_ref.add(doc)

