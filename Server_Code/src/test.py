import time
from datetime import timedelta
from apscheduler.scheduler import Scheduler
import requests
import pymysql
import solr
from random import randrange

DB_SERVER = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_DATABASE = "iwant"

#s = solr.SolrConnection('http://localhost:8983/solr')
#r = s.query('manufacturer:canon', fq='price:[0 TO 130.00]')
#for hit in r.results:
    #print (hit["prodName"])

def getProds():
    print "CALLING .............."
    insert_merc_success = 0
    insert_merc_exception = 0
    insert_prod_success = 0
    insert_prod_exception = 0
    api_URL = "http://api.remix.bestbuy.com/v1/products(type=HardGood)?apiKey=egvub6bxhj7br8dgh53vnvhd&show=name,thumbnailImage,image,shortDescription,longDescription,regularPrice,class,subclass,manufacturer,productTemplate,department&pageSize=50&format=json&page="
    #api_URL = "http://api.remix.bestbuy.com/v1/products(manufacturer in(canon,sony,nikon))?apiKey=egvub6bxhj7br8dgh53vnvhd&show=name,thumbnailImage,image,shortDescription,longDescription,manufacturer,regularPrice,subclass,class&pageSize=50&format=json&page="
    conn = pymysql.connect(DB_SERVER,DB_USER,DB_PASSWORD,DB_DATABASE)
    conn.autocommit(1)
    cursor = conn.cursor()
    manufacturers = {}
    for i in range(1,10):
        r = requests.get(api_URL+str(i)).json()
        c=r['products']
        for product in c:
            #print product
            print ("===================================")
            #print ((type(product)))
            #print (product)
            name = ""
            thumbnailImage = ""
            image = ""
            shortDescription = ""
            longDescription = ""
            manufacturer = ""
            regularPrice = ""
            department = ""
            producttemplate = ""

            if "name" in product:
                name = product["name"]
                if name is None:
                    continue;
            if "thumbnailImage" in product:
                thumbnailImage = product["thumbnailImage"]
                if thumbnailImage is None:
                    continue;
            if "image" in product:
                image = product["image"]
                if image is None:
                    continue;
            if "shortDescription" in product:
                shortDescription = product["shortDescription"]
                if shortDescription is None:
                    continue;
            if "longDescription" in product:
                longDescription = product["longDescription"]
                if longDescription is None:
                    continue;
            if "regularPrice" in product:
                regularPrice = product["regularPrice"]
                if regularPrice is None:
                    continue;
            if "department" in product:
                department = product["department"]
                if department is None:
                    continue;
            if "productTemplate" in product:
                producttemplate = product["productTemplate"]
                if producttemplate is None:
                    continue;
            if "manufacturer" in product:
                manufacturer = product["manufacturer"]
                if manufacturer is None:
                    continue;
                if manufacturer not in manufacturers:
                    manufacturers[manufacturer] = True
                    try:
                        insert_merc_success = insert_merc_success+1
                        insert = "INSERT INTO merchant_details(merchant_name,username) VALUES('"+manufacturer+"', '"+manufacturer+"')"
                        cursor.execute(insert)
                    except Exception, err:
                        print (err)
                        insert_merc_exception = insert_merc_exception+1
                        continue
            try:
                select = "SELECT merchant_id FROM merchant_details WHERE merchant_name='"+manufacturer+"'"
                cursor.execute(select)
                merchant_id = 0
                for i in cursor.fetchall():
                    merchant_id = i[0]
            except Exception,err:
                print (err)
                continue

            if merchant_id is None:
                continue

            insert_prod_success = insert_prod_success+1
            try:
                formatter = (randrange(50),merchant_id,name,thumbnailImage,image,shortDescription,longDescription,regularPrice,department,producttemplate)
                query = "INSERT INTO product_details(quantity,Merchant_id,name,smallimage,image,shortdescription,description,price,category,subcategory) VALUES(%s, %s, '%s', '%s', '%s', '%s', '%s', %s, '%s', '%s');" % formatter
                cursor.execute(query)
            except Exception,err:
                print(err)
                insert_prod_exception = insert_prod_exception+1
                pass
    print ((insert_merc_success))
    print ((insert_prod_success))
    print ((insert_merc_success)-(insert_merc_exception))
    print ((insert_prod_success)-(insert_prod_exception))


getProds()