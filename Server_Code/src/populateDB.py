import requests
import pymysql
import DBConfig
from pymongo import MongoClient
from apscheduler.scheduler import Scheduler

# Start the scheduler
sched = Scheduler(standalone=True)

client = MongoClient()
db = client. iwant
collection = db.coupons


COUPONS_KEY = "5d4d4f0cc20146c65020048ce228c6621e3b19f419051bd3dcd195978a49150d8361d6f92234d57771861f4d5ed427c2"
urls = {}

urls['categories'] = "http://api.8coupons.com/v1/getcategory";
urls['subCategory'] = "http://api.8coupons.com/v1/getsubcategory";
urls['dealType'] = "http://api.8coupons.com/v1/getdealtype";
urls['stores'] = "http://api.8coupons.com/v1/getchainstorelist?key=" + COUPONS_KEY;
urls['dealsOfTheDay'] = "http://api.8coupons.com/v1/getrealtimelocaldeals?key=" + COUPONS_KEY + "&userid=18381";
urls['travelDeals'] = "http://api.8coupons.com/v1/getrealtimetraveleals?key=" + COUPONS_KEY;
urls['productDeals'] = "http://api.8coupons.com/v1/getrealtimeproductdeals?key=" + COUPONS_KEY;
urls['storeDeals'] = "http://api.8coupons.com/v1/getrealtimechaindeals?key=" + COUPONS_KEY;

def insertMongoDB(jsonObject, documentKey):
    if documentKey == "categories":
        collection = db.categories
    elif documentKey == "subCategory":
        collection = db.subcategory
    elif documentKey == "dealType":
        collection = db.dealtype
    elif documentKey == "stores":
        collection = db.stores
    elif documentKey == "dealsOfTheDay":
        collection = db.dealsoftheday
    elif documentKey == "travelDeals":
        collection = db.traveldeals
    elif documentKey == "productDeals":
        collection = db.productdeals
    elif documentKey == "storeDeals":
        collection = db.storedeals

    for entry in jsonObject:
        print(entry)
        collection.insert(entry)

def fetch_Coupons_API_Data():
    print("Fetching data from API and inserting into DB...")
    for url in urls:
        print((urls[url]))
        r = requests.get(urls[url]).json()
        insertMongoDB(r, url)

# Schedule job_function to be called using the time provided in file
file_obj = open('C:\\Users\\Sudharshan\\Desktop\\sample.txt')
data = file_obj.readline().split(",")
dy = int(data[0])
hr = int(data[1])
mnts = int(data[2])
sec = int(data[3])
sched.add_interval_job(fetch_Coupons_API_Data, days=dy, hours=hr, minutes=mnts, seconds=sec)
sched.start()