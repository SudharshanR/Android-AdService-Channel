import DBConfig
import pymysql
from json import dumps
from pymongo import MongoClient
#from bson.json_util import dumps

def getProduct(id):
    conn = pymysql.connect(DBConfig.DB_SERVER,DBConfig.DB_USER,DBConfig.DB_PASSWORD,DBConfig.DB_DATABASE)
    conn.autocommit(1)
    cursor = conn.cursor()
    query = "SELECT * FROM products WHERE productID=%s"
    cursor.execute(query,(id))
    cursor.connection.commit()
    details = {}
    for response in cursor.fetchall():
        details['productID'] = response[0]
        details['productName'] = response[1]
        details['merchantName'] = response[2]
        details['price'] = response[3]
        details['imageURL'] = response[4]
    cursor.close()
    conn.close()
    return details
    #return template('<b>Hello {{name}}</b>!', name=name)

def getProducts():
    conn = pymysql.connect(DBConfig.DB_SERVER,DBConfig.DB_USER,DBConfig.DB_PASSWORD,DBConfig.DB_DATABASE)
    conn.autocommit(1)
    cursor = conn.cursor()
    query = "SELECT name, description, image, price FROM product_details;"
    cursor.execute(query)
    cursor.connection.commit()
    products = {}
    details = []
    for response in cursor.fetchall():
        detail = {}
        detail['name'] = response[0]
        detail['description'] = response[1]
        detail['image'] = response[2]
        detail['price'] = response[3]
        details.append(detail)
    products['products'] = details
    cursor.close()
    conn.close()
    return dumps(products)
    return products

def getTravelDeals():
    client = MongoClient()
    itemCnt = 0
    db = client.iwant
    collection = db.traveldeals
    output = []
    for result in collection.find({},{"_id":0}):
        if itemCnt>=30:
            break
        output.append(result)
        itemCnt+=1
    return dumps({'products' : output})

def getProductDeals():
    itemCnt = 0
    client = MongoClient()
    db = client.iwant
    collection = db.productdeals
    output = []
    for result in collection.find({},{"_id":0}):
        if itemCnt>=30:
            break
        output.append(result)
        itemCnt+=1
    return dumps({'products' : output})

def updateBiddingDetails(username, query, price, merchants):
    conn = pymysql.connect(DBConfig.DB_SERVER,DBConfig.DB_USER,DBConfig.DB_PASSWORD,DBConfig.DB_DATABASE)
    conn.autocommit(1)
    cursor = conn.cursor()
    for merchant in merchants:
        print "DBHandle >>>>> "+merchant
        formatter = ("open", username, price, "date_format(now()),%H:%i:%s", username, "no", "no", price, merchant, query)
        req = "INSERT INTO bidding_details(bid_status, current_bidder, current_price, date, initiator_id, is_read, is_replied, price_opened, requestor_id, search_query) VALUES('%s', '%s', %s, %s, '%s', '%s', '%s', %s, '%s', '%s');" % formatter
        print req
        cursor.execute(req)


