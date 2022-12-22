import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

url = "http://www.atmovies.com.tw/movie/next/"
Data = requests.get(url)
Data.encoding = "utf-8"
sp = BeautifulSoup(Data.text, "html.parser")
result=sp.select(".filmListAllX li")
info = ""


for item in result:
	
	hyperlink = "http://www.atmovies.com.tw" + item.find("div", class_="filmtitle").find("a").get("href")
	#網頁連結
	
	show = item.find("div", class_="runtime").text.replace("上映日期：", "")
	show = show.replace("片長：", "")
	show = show.replace("分", "")
	showDate = show[0:10]
	
	showLength = show[13:]
	
	#片長有些怪怪
	picture = item.find("img").get("src").replace(" ", "")
	#照片網址
	
	images = item.select("img")
	if len(images) == 1:
		rate = "目前尚無分級資訊"
	else:
		rate = images[1].get("src")
		if rate=="/images/cer_G.gif":
			rate = "普遍級(一般觀眾皆可觀賞)"
		if rate=="/images/cer_P.gif":
			rate = "保護級(未滿六歲之兒童不得觀賞，六歲以上未滿十二歲之兒童須父母、師長或成年親友陪伴輔導觀賞)"
		if rate=="/images/cer_F2.gif":
			rate = "輔導級(未滿十二歲之兒童不得觀賞)"
		if rate=="/images/cer_F5.gif":
			rate = "輔導級(未滿十五歲之人不得觀賞)"
		if rate=="/images/cer_R.gif":
			rate = "限制級(未滿十八歲之人不得觀賞)"
	
	title = item.find("div", class_="filmtitle").text
	#電影名稱
	movie_id = item.find("div",class_="filmtitle").find("a").get("href").replace("/","").replace("movie", "")
	lastUpdate = sp.find("div", class_="smaller09").text[5:]
	docs = [
	{
	"lastUpdate": lastUpdate,
	"hyperlink": hyperlink,
	"showDate" : showDate,
	"showLength" : showLength,
	"picture" : picture,
	"title": title,
	"rate" : rate,
	}
	]

	collection_ref = db.collection("苓苓電影").document(movie_id)
	for doc in docs:
		collection_ref.set(doc)



