import DBHandler
import requests
from bson.json_util import dumps
import bottle
from bottle import route, run, post
import pymysql
import solr

@route('/getproducts')
def getProducts():
    return DBHandler.getProducts()

@route('/gettraveldeals')
def getTravelDeals():
    return DBHandler.getTravelDeals()
    #deals = {}
    #deals['deals'] = DBHandler.getTravelDeals()
    #return deals

@route('/getproductdeals')
def getGoodsDeals():
    return DBHandler.getProductDeals()

@route('/getlocationdeals/<lat>/<lon>')
def getlocationdeals(lat, lon):
    url = "http://api.8coupons.com/v1/getdeals?key=5d4d4f0cc20146c65020048ce228c6621e3b19f419051bd3dcd195978a49150d8361d6f92234d57771861f4d5ed427c2"
    mileRadius = "&mileradius=20"
    limit = "&limit=1000"
    order = "&orderby=radius"
    return dumps({'locationdeals':requests.get(url+"&lat="+lat+"&lon="+lon+mileRadius+limit+order).json()})


@post('/searchproduct')
def searchProduct():
    search_str = bottle.request.json
    query = search_str["query"]
    s = solr.SolrConnection('http://localhost:8983/solr')
    #r = s.query('*:*', fq='price:[0 TO 130.00]')
    solrQuery = 'text:' + query
    r = s.query(solrQuery)
    products = {}
    details = []
    for hit in r.results:
        if hit["score"] < 0.9:
            break
        detail = {}
        detail["product_id"] = hit["product_id"]
        detail["name"] = hit["name"]
        detail["shortdescription"] = hit["shortdescription"]
        detail["description"] = hit["description"]
        detail["smallimage"] = hit["smallimage"]
        detail["image"] = hit["image"]
        detail["price"] = hit["price"]
        details.append(detail)

    products['products'] = details
    return dumps(products)


@post('/android/bid')
def bidProduct():
    search_str = bottle.request.json
    query = search_str["bid_Query"]
    price = search_str["bid_Price"]
    username = search_str["userName"]
    s = solr.SolrConnection('http://localhost:8983/solr')
    #r = s.query('*:*', fq='price:[0 TO 130.00]')
    solrQuery = 'text:' + query
    print solrQuery
    r = s.query(solrQuery)
    merchants = []
    added_Merchants = {}
    for hit in r.results:
        if hit["score"] < 0.9:
            break
        #merchant = {}
        #merchant["name"] = hit["manufacturer"]
        #merchants.append(merchant)
        merchant_ID = hit["Merchant_id"]
        if merchant_ID in added_Merchants:
            continue
        merchants.append(hit["Merchant_id"])
        added_Merchants[merchant_ID] = 1

    print merchants
    print type(merchants)
    DBHandler.updateBiddingDetails(username, query, price, merchants)


run(host='192.168.1.4', port=8099, debug=True)
