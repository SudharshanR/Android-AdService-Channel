# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
'''
Project Title : I-want Mobile Application for Ad service Channel
Description   : This runs as a server side application for the Andriod application
                And Web-service. Bottle.py Framework is used to routing to different
				pages both on server-side and Android. This path carries our Bidding
				process that carried out between merchant and customer.
Author       : Sagar Shinde, Sudharshan Ramakumar, Vigneshwar M Gopinath under Prof Jerry Gao.

Homepage and documentation: http://54.215.151.161/

Copyright (c) 2014, San Jose State University.

'''
#
__author__ = 'Sagar Shinde, Sudharshan Ramakumar, Vigneshwar M Gopinath under Prof Jerry Gao'
__version__ = '0.4-beta'
#
import bottle
import requests
from bottle import static_file
import datetime
#import random
#import string
import user
import json
from config import open_connection
from bottle import\
        run, \
        debug, \
        request, \
        get, \
        post, \
        redirect, \
        post, \
        route, \
        HTTPError
import pymysql
import re
import session
from simplejson import dumps
import solr
from pymongo import MongoClient
#from bson.json_util import dumps
###############################################################################
# Database connection to MySQL with
# <<Change needed>> - Change the host   ---> Please Delete this line
# host = localhost, port = 3306 and username as root

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')

cur = conn.cursor()

#################################################################################
# Static root the the project folder
# update the path once the code been integrated ---> Please Delete
STATIC_ROOT = "C:\iwant-beta\static"

@bottle.get('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root=STATIC_ROOT)
#####################################################################################
#                                                                                   #
# Redirects when accessed http://54.215.151.161/ to http://54.215.151.161/index     #
#                                                                                   #
#####################################################################################
#
@bottle.route('/')
def blog_index():
    bottle.redirect("/index")
#####################################################################################
#
#####################################################################################
#                                                                                   #
# host: Checks on loading every page in the application                             #
# Inline Function, Checks if the user had any session opened and session is still   #
# Active
#                                                                                   #
#####################################################################################

def login_check():
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
    cur = conn.cursor()
    print ('in login check')
    cookie = bottle.request.get_cookie("session_id1")
    print ('database opened----->')
    print (cookie)
    if cookie is None:
        print ("no cookie...")
        return None

    else:
        print ("in else login check")
        session_id = cookie
        if (session_id is None):
            return None

        else:
            # look up username record
            selectquery = "SELECT `username` FROM `session` WHERE `session_id` = '%s'" % (session_id)
            print(selectquery)
            cur.execute(selectquery)
            usr = cur.fetchone()
            print (usr)
            if (usr is None):
                return None
            else:
                print ("Return")
                return True

    return False
#####################################################################################
#                                                                                   #
#####################################################################################
#                                                                                   #
# host: http://54.215.151.161/register                                              #
# Signup - For Merchant to register with username and email for the merchant        #
#                                                                                   #
#####################################################################################

@bottle.get('/register')
def present_registerclient():
    error = ""
    er = bottle.request.params.get("error")
    if(er):
        if(er == "1"):
            error = "Password and Confirm Password Not Same"
        elif(er == "2"):
            error = "User already registered"
        return bottle.template("register.tpl", dict(user_name="",
         password="", confirmpwd="", email="", mobile_number="", error=error))
    else:
        error = ""
    return bottle.template("register.tpl", dict(user_name="",
     password="", confirmpwd="", email="", mobile_number="", error=""))

#
# Post the form to the database after the user click on submit
#
@bottle.post('/register')
def process_registerclient():
    # Get the values from the Form and store them
    cookie = bottle.request.get_cookie("session")
    email = bottle.request.forms.get("email")
    username = bottle.request.forms.get("user_name")
    password = bottle.request.forms.get("password")
    confirmpwd = bottle.request.forms.get("confirmpwd")
    mobile_number = bottle.request.forms.get("mobile_number")
    # Usr_role is set to one for Merchant
    # For Reference usr_role is 0 for admin and 2 for user(buyers)
    usr_role = 1
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
    cur = conn.cursor()
    if(not user.register(cur, username, password, mobile_number, confirmpwd, email, usr_role)):
        return bottle.redirect("/register?error=2")
    else:
        # Now the merchant is added suceesfully
		# not update the merchant table creating the username and merchant id
        if(not user.addmerchant(cur, username)):
            print("Cannot able to add merchnat")
            return bottle.redirect("/register?error=1")
        return bottle.redirect("/index")
        return True
        #return "<script>window.close();</script>"

#####################################################################################
#
#####################################################################################
#                                                                                   #
# host: http://54.215.151.161/login                                                 #
# Loads the login template from the static folder                                   #
#                                                                                   #
#####################################################################################
@bottle.route('/login')
def present_login():
    #bottle.TEMPLATE_PATH.insert(0, 'views')
    error = ""
    er = bottle.request.params.get("error")
    if(er):
        if(er == "1"):
            error = "Password and Confirm Password Not Same"
        elif(er == "2"):
            error = "Wrong Password"
        elif(er == "3"):
            error = "User Not Found"
        return bottle.template("login.tpl", dict(username="",password="",error=error))
    else:
        error = ""
        return bottle.template("login.tpl", dict(username="",password="",error=error))

########################################################################################

@bottle.post('/login')
def process_login():
    username = bottle.request.forms.get("username")
    password = bottle.request.forms.get("password")
    print ("in process login")
    if (user.validate_login(username, password)):
        print ("in validate lagin:")
        bottle.redirect("/index")
    else:
        print ("in else validate login:")
        return bottle.template("login.tpl", dict(username="", password="", error="Invalid Login"))

#####################################################################################################
#                                                                                                   #
# URl: host: http://54.215.151.161/logout                                                           #
# Description: Deletes the session_id from the database and deletes the session                     #
#                                                                                                   #
#####################################################################################################
#
@bottle.get('/logout')
def process_logout():
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
    conn.autocommit(1)
    cur = conn.cursor()

    cookie = bottle.request.get_cookie("session")
    print ("=======================")
    print (cookie);
    cookie1 = bottle.request.get_cookie("session_id1")
    print ("=======================")
    print (cookie1);

    if (cookie1 == None):
        print ("no cookie...")
        bottle.redirect("/index")

    else:
        session_id = user.check_secure_val(cookie)
        print("+_+_+_+_+_+")
        print(session_id)
        if (session_id == None):
            query2 = "DELETE from session WHERE `session_id`='%s'" % (cookie1)
            print (query2)
            if(cur.execute(query2)):
                #conn.commit();
                print("Session Deleted")
                print("no secure session_id")
                bottle.response.set_cookie("session", "")
                bottle.response.set_cookie("session_id1", "")
                bottle.response.set_cookie("session_id", "")
                bottle.redirect("/login")

        else:
            # remove the session
            session.end_session(cur, session_id)
            print ("clearing the cookie")

            #bottle.response.set_cookie("session", "")

            bottle.redirect("/index")
 #       bottle.redirect("/login")
###########################################################################################

@bottle.get('/viewBid')
def Load_bids():
    username = login_check()  # see if user is logged in
    if (username is None):
        bottle.redirect("/login")
    #To Retrieve session username
    cookie = bottle.request.get_cookie("session")
    session_id = user.check_secure_val(cookie)
    cookierole = bottle.request.get_cookie("session_role")
    user_role = user.check_secure_val(cookierole)
    msg_count = user.count_msg(session_id)
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
    cur = conn.cursor()
    cur.execute("SELECT * FROM message_route")
    r = cur.fetchall();
    #cur.close()
    #conn.close()
    return bottle.template("viewBids.tpl", dict(username=r))


#<------Code by Niva----->


#<-----Code by Niva------>
@bottle.get('/adminadd_users')
def present_adminadd_users():
    username = login_check()  # see if user is logged in
    if (username is None):
        bottle.redirect("/login")
    #To Retrieve session username
    cookie = bottle.request.get_cookie("session")
    session_id = user.check_secure_val(cookie)
    cookierole = bottle.request.get_cookie("session_role")
    user_role = user.check_secure_val(cookierole)
    cookietheme = bottle.request.get_cookie("sessiontheme")
    session_theme = user.check_secure_val(cookietheme)
    msg_count = user.count_msg(session_id)
    deleteid = bottle.request.params.get("deleteuser")
    if(deleteid):
        query2 = "DELETE FROM login_details where username = '%s' " % (deleteid)
        print (query2)
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
        cur1 = conn.cursor()
        #conn.commit();
        if(cur1.execute(query2)):
            print ("Inside Execute")
            conn.commit();
            bottle.redirect("/adminadd_users?error=success")
    toedituser = bottle.request.params.get("toedit")
    #error = bottle.request.params.get("er")
    query = "SELECT username, usr_email, usr_role, usr_role, usr_status FROM login_details "
    print (query)
    cur.execute(query)
    #conn.commit();
    data = cur.fetchall()
    if (toedituser):
        query2 = "SELECT username, password, usr_email, usr_role, mobile_number, usr_role, usr_status FROM login_details where username = '%s' " %(toedituser)
        print (query2)
        cur.execute(query2)
        #conn.commit();
        data2 = cur.fetchall()
        for rows in data2:
            print (rows)
            username = rows[0]
            password = rows[1]
            email = rows[2]
            contactno = rows[4]
            #conn.commit();
        return bottle.template("adminadd_users.tpl", dict(user_name=username, email=email, password=password, confirmpwd=password, mobile_number=contactno, rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    else:
        return bottle.template("adminadd_users.tpl", dict(user_name="", email="", password="", confirmpwd="", mobile_number="", rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    return bottle.template("adminadd_users.tpl", dict(user_name="", email="", password="", confirmpwd="", mobile_number="", rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))


#<---Coded by niva--->
@bottle.post('/adminadd_users')
def process_adminadd_users():
    #username = login_check()  # see if user is logged in
    email = bottle.request.forms.get("email")
    username = bottle.request.forms.get("user_name")
    password = bottle.request.forms.get("password")
    confirmpwd = bottle.request.forms.get("confirmpwd")
    mobile_number = bottle.request.forms.get("mobile_number")
    submit = bottle.request.forms.get("submit")
    if submit == "Submit":
        print ("Inside Submit")
        email = bottle.request.forms.get("email")
        toedit = bottle.request.params.get("toedit")
        username = bottle.request.forms.get("user_name")
        usr_role = 2
        if(toedit):
            print("Inside To edit user")
            if(not user.update_users(cur, username, password, mobile_number, confirmpwd, email, toedit)):
                bottle.redirect("/adminadd_users")
            else:
                bottle.redirect("/users")
        else:
            if(not user.register(cur, username, password, mobile_number, confirmpwd, email, usr_role)):
                bottle.redirect("/adminadd_users?error-1")
            print("User details stored succesfully")
            bottle.redirect("/users")

    bottle.redirect("/users")

########################################################################################################################
#																													  ##
########################################################################################################################
#																													  ##
#   URL: VMIP:9000/viewbids                                          	                                              ##
#   Description: Display the products posted by the user and also allows user to add products                         ##
#   It Does the merchant management stuff for the product                                                             ##
########################################################################################################################

@bottle.get('/viewproducts')
def present_viewproducts():
 #   username = login_check()  # see if user is logged in
    print ("_+_+_+_+_+++++++++++++")
 #   print (username)
    if (login_check() is False):
        bottle.redirect("/login")
    #To Retrieve session username
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
    cur = conn.cursor()
    user_name = bottle.request.get_cookie("session")
    print ("+++++++",user_name)
    username = user.check_secure_val(user_name)
    print ("+++++++",username)
    session_id = bottle.request.get_cookie("session_id1")
    cookierole = bottle.request.get_cookie("session_role")
    user_role = user.check_secure_val(cookierole)
    cookietheme = bottle.request.get_cookie("sessiontheme")
    session_theme = user.check_secure_val(cookietheme)
    msg_count = user.count_msg(session_id)
    deleteid = bottle.request.params.get("deleteuser")
    session_theme = "green.css"
    if(deleteid):
        query2 = "DELETE FROM product_details where product_id = '%s' " % (deleteid)
        print (query2)
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
        cur1 = conn.cursor()
        #conn.commit();
        #cur1.close();
        if(cur1.execute(query2)):
            print ("Inside Execute")
            conn.commit();
            bottle.redirect("/viewproducts?error=success")
    toedituser = bottle.request.params.get("toedit")
    #error = bottle.request.params.get("er")
    if(user_role == "0"):
        query_string = "1"
    else:
        query_string = "Merchant_id=(Select merchant_id from merchant_details where username='" + username + "')"
    query = "SELECT Merchant_id, product_id, name, image, s_description, l_description, price, quantity, category, subcategory, tags FROM product_details where " + query_string + " "
    print (query, "......")
    cur.execute(query)
    #conn.commit();
    data = cur.fetchall()
    #for rows in data2:
        #print rows
        #name = rows[0]
        #description = rows[1]
        #price = rows[2]
        #quantity = rows[3]
        #category = rows[4]
        #subcategory = rows[5]
        #tags = rows[6]
        #image = rows[6]
    if (toedituser):
        return bottle.template("viewproducts.tpl", dict(rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    else:
        return bottle.template("viewproducts.tpl", dict(rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    return bottle.template("viewproducts.tpl", dict(rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))

########################################################################################################################################################################
##
##
##
#<-----Code by Niva------>
@bottle.get('/addproducts')
def present_addproducts():
    username = login_check()  # see if user is logged in
    if (username is None):
        bottle.redirect("/login")
    #To Retrieve session username
    cookie = bottle.request.get_cookie("session")
    session_id = user.check_secure_val(cookie)
    cookierole = bottle.request.get_cookie("session_role")
    user_role = user.check_secure_val(cookierole)
    cookietheme = bottle.request.get_cookie("sessiontheme")
    session_theme = user.check_secure_val(cookietheme)
    cookierole = bottle.request.get_cookie("session_role")
    user_role = user.check_secure_val(cookierole)

    msg_count = user.count_msg(session_id)
    deleteid = bottle.request.params.get("deleteuser")
    if(deleteid):
        query2 = "DELETE FROM login_details where username = '%s' " % (deleteid)
        print (query2)
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
        cur1 = conn.cursor()
        #conn.commit();
        if(cur1.execute(query2)):
            print ("Inside Execute")
            #conn.commit();
            bottle.redirect("/addproducts?error=success")
    toedituser = bottle.request.params.get("toedit")
    if (toedituser):
        if(user_role == "0"):
            query_string = ""
        else:
            query_string = "Merchant_id=(Select merchant_id from merchant_details where username='" + session_id + "') and "
        query2 = "SELECT name, description, price, quantity, category, subcategory, tags, image FROM product_details where " + query_string + " product_id = '%s' " %(toedituser)
        print (query2)
        cur.execute(query2)
        #conn.commit();
        data2 = cur.fetchall()
        for rows in data2:
            print (rows)
            name = rows[0]
            description = rows[1]
            price = rows[2]
            quantity = rows[3]
            category = rows[4]
            subcategory = rows[5]
            tags = rows[6]
            image = rows[7]
            #conn.commit();
            return bottle.template("addproducts.tpl", dict(name=name, description=description, price=price, quantity=quantity, category=category, subcategory=subcategory, tags=tags, image=image, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    else:
        return bottle.template("addproducts.tpl", dict(name="", description="", price="", quantity="", category="", subcategory="", tags="", image="No_Image.png", session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    return bottle.template("addproducts.tpl", dict(name="", description="", price="", quantity="", category="", subcategory="", tags="", image="No_Image.png", session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))


#<---Coded by niva--->
@bottle.post('/addproducts')
def process_addproducts():
    username = login_check()  # see if user is logged in
    if (username is None):
        bottle.redirect("/login")
    name = bottle.request.forms.get("name")
    description = bottle.request.forms.get("description")
    price = bottle.request.forms.get("price")
    quantity = bottle.request.forms.get("quantity")
    category = bottle.request.forms.get("category")
    subcategory = bottle.request.forms.get("subcategory")
    tags = bottle.request.forms.get("tags")
    image = bottle.request.files.get("image")
    image_old = bottle.request.forms.get("image_old")
    submit = bottle.request.forms.get("submit")
    if submit == "Submit":
        print ("Inside Submit")
        toedit = bottle.request.params.get("toedit")
        if(toedit):
            print("Inside To edit user")
            if(not user.update_product(cur, name, description, price, quantity, category, subcategory, tags, image, image_old, toedit)):
                bottle.redirect("/addproducts")
            else:
                bottle.redirect("/viewproducts")
        else:
            if(not user.addproducts(cur, name, description, price, quantity, category, subcategory, tags, image, image_old)):
                bottle.redirect("/addproducts?error-1")
            print("User details stored succesfully")
            bottle.redirect("/viewproducts")

    bottle.redirect("/addproducts")


#<-----Code by Niva------>
@bottle.get('/edit-product')
def present_editproduct():
    username = login_check()  # see if user is logged in
    if (username is None):
        bottle.redirect("/login")
    #To Retrieve session username
    cookie = bottle.request.get_cookie("session")
    session_id = user.check_secure_val(cookie)
    cookierole = bottle.request.get_cookie("session_role")
    user_role = user.check_secure_val(cookierole)
    cookietheme = bottle.request.get_cookie("sessiontheme")
    session_theme = user.check_secure_val(cookietheme)
    msg_count = user.count_msg(session_id)
    deleteid = bottle.request.params.get("deleteuser")
    if(deleteid):
        query2 = "DELETE FROM login_details where username = '%s' " % (deleteid)
        print (query2)
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
        cur1 = conn.cursor()
        #conn.commit();
        if(cur1.execute(query2)):
            print ("Inside Execute")
            #conn.commit();
            bottle.redirect("/edit-product?error=success")
    if(user_role == "0"):
        query = "1"
    else:
        query = "Merchant_id=(Select merchant_id from merchant_details where username='" + session_id + "')"
    query1 = "SELECT name, product_id FROM product_details where " + query + ""
    print (query1)
    cur.execute(query1)
    #conn.commit();
    data2 = cur.fetchall()
    topost = bottle.request.params.get("topost")
    if (topost):
        topost_edited = re.sub(r'\s+', '', topost)
        if(user_role == "0"):
            query_string = ""
        else:
            query_string = "Merchant_id=(Select merchant_id from merchant_details where username='" + session_id + "') and "
        query2 = "SELECT name, description, price, quantity, category, subcategory, tags, image, product_id FROM product_details where " + query_string + " product_id = '%s' " % (topost_edited)
        print (query2)
        cur.execute(query2)
        #conn.commit();
        data3 = cur.fetchall()
        for rows in data3:
            print (rows)
            name = rows[0]
            description = rows[1]
            price = rows[2]
            quantity = rows[3]
            category = rows[4]
            subcategory = rows[5]
            tags = rows[6]
            image = rows[7]
            product_id = rows[8]
            #conn.commit();
            return bottle.template("editproducts.tpl", dict(rows=data2,product_name="",name=name, description=description, price=price, quantity=quantity, category=category, subcategory=subcategory, tags=tags, image=image, product_id=product_id, topost=topost, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    else:
        return bottle.template("editproducts.tpl", dict(rows=data2,product_name="",name="", description="", price="", quantity="", category="", subcategory="", tags="", image="No_Image.png", product_id="", topost="", session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    return bottle.template("editproducts.tpl", dict(rows=data2,product_product_name="",name="", description="", price="", quantity="", category="", subcategory="", tags="", image="No_Image.png", product_id="", topost="", session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))


#<---Coded by niva--->
@bottle.post('/edit-product')
def process_editproducts():
    #username = login_check()  # see if user is logged in
    product_name = bottle.request.forms.get("product_name")
    submit = bottle.request.forms.get("submit")
    if submit == "Submit":
        print ("Inside Submit")
        bottle.redirect("/edit-product?topost=%s"%(product_name))#####ERROR Line####

    bottle.redirect("/edit-product")


#<-----Code by Niva------>
@bottle.get('/products-transaction')
def present_viewtransactions():
    username = login_check()  # see if user is logged in
    if (username is None):
        bottle.redirect("/login")
    #To Retrieve session username
    cookie = bottle.request.get_cookie("session")
    session_id = user.check_secure_val(cookie)
    cookierole = bottle.request.get_cookie("session_role")
    user_role = user.check_secure_val(cookierole)
    cookietheme = bottle.request.get_cookie("sessiontheme")
    session_theme = user.check_secure_val(cookietheme)
    msg_count = user.count_msg(session_id)
    deleteid = bottle.request.params.get("deleteuser")
    if(deleteid):
        query2 = "DELETE FROM transaction_details where transaction_id = '%s' " % (deleteid)
        print (query2)
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
        cur1 = conn.cursor()
        #conn.commit();
        #cur1.close();
        if(cur1.execute(query2)):
            print ("Inside Execute")
            conn.commit();
            bottle.redirect("/products-transaction?error=success")
    toedituser = bottle.request.params.get("toedit")
    #error = bottle.request.params.get("er")
    if(user_role == "0"):
        query_string = "1"
    else:
        query_string = "receiver='" + session_id + "'"
    query = "SELECT transaction_id, sender, receiver, invoice_no, amount, payment_mode, date, status FROM transaction_details where " + query_string + " "
    print (query)
    cur.execute(query)
    #conn.commit();
    data = cur.fetchall()
    #for rows in data2:
        #print rows
        #name = rows[0]
        #description = rows[1]
        #price = rows[2]
        #quantity = rows[3]
        #category = rows[4]
        #subcategory = rows[5]
        #tags = rows[6]
        #image = rows[6]
    if (toedituser):
        return bottle.template("viewtransactions.tpl", dict(rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    else:
        return bottle.template("viewtransactions.tpl", dict(rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    return bottle.template("viewtransactions.tpl", dict(rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))


#<-----Code by Niva------>
@bottle.get('/products-Purchased')
def present_viewrecentpurchase():
    username = login_check()  # see if user is logged in
    if (username is None):
        bottle.redirect("/login")
    #To Retrieve session username
    cookie = bottle.request.get_cookie("session")
    session_id = user.check_secure_val(cookie)
    cookierole = bottle.request.get_cookie("session_role")
    user_role = user.check_secure_val(cookierole)
    cookietheme = bottle.request.get_cookie("sessiontheme")
    session_theme = user.check_secure_val(cookietheme)
    msg_count = user.count_msg(session_id)
    deleteid = bottle.request.params.get("deleteuser")
    if(deleteid):
        query2 = "DELETE FROM purchase_details where invoice_no = '%s' " % (deleteid)
        print (query2)
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
        cur1 = conn.cursor()
        #conn.commit();
        #cur1.close();
        if(cur1.execute(query2)):
            print ("Inside Execute")
            conn.commit();
            bottle.redirect("/products-Purchased?error=success")
    toedituser = bottle.request.params.get("toedit")
    #error = bottle.request.params.get("er")
    if(user_role == "0"):
        query_string = "1"
    else:
            query_string = "Merchant_id=(Select merchant_id from merchant_details where username='" + session_id + "')"
    query = "SELECT invoice_no, date, merchant_id, user_id, type, product_id, price, payment_status , transaction_id FROM purchase_details where " + query_string + " "
    print (query)
    cur.execute(query)
    #conn.commit();
    data = cur.fetchall()
    #for rows in data2:
        #print rows
        #name = rows[0]
        #description = rows[1]
        #price = rows[2]
        #quantity = rows[3]
        #category = rows[4]
        #subcategory = rows[5]
        #tags = rows[6]
        #image = rows[6]
    if (toedituser):
        return bottle.template("viewrecentpurchase.tpl", dict(rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    else:
        return bottle.template("viewrecentpurchase.tpl", dict(rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    return bottle.template("viewrecentpurchase.tpl", dict(rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))


#<-----Code by Niva------>
@bottle.get('/products-bids')
def present_viewbids():
    username = login_check()  # see if user is logged in
    print "!!==1111"
    if (username is None):
        bottle.redirect("/login")
    #To Retrieve session username
    print "!!==1111"
    cookie = bottle.request.get_cookie("session")
    session_id = user.check_secure_val(cookie)
    cookierole = bottle.request.get_cookie("session_role")
    user_role = user.check_secure_val(cookierole)
    cookietheme = bottle.request.get_cookie("sessiontheme")
    session_theme = user.check_secure_val(cookietheme)
    msg_count = user.count_msg(session_id)
    deleteid = bottle.request.params.get("deleteuser")
    print "!!==1111"
    if(deleteid):
        query2 = "DELETE FROM bidding_details where bidding_id = '%s' " % (deleteid)
        print (query2)
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
        cur1 = conn.cursor()
        #conn.commit();
        #cur1.close();
        if(cur1.execute(query2)):
            print ("Inside Execute")
            conn.commit();
            bottle.redirect("/products-bids?error=success")
    accept_id = bottle.request.params.get("accept_id")
    reject_id = bottle.request.params.get("reject_id")
    if(accept_id):
        status = '1'
        if(user.ins_transaction(status,accept_id)):
            bottle.redirect("/products-bids?error=success")
    elif(reject_id):
        status = '2'
        #if(user.ins_transaction(status,reject_id)):
        bottle.redirect("/products-bids?error=success")
    toedituser = bottle.request.params.get("toedit")
    #error = bottle.request.params.get("er")
    if(user_role == "0"):
        query = "1"
    else:

        query = "B.Merchant_name='" + session_id + "'"
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
    cur = conn.cursor()
    query = "SELECT a.initiator_id, a.date, a.search_query, a.price_opened, a.current_price, a.requestor_id, a.current_bidder , a.is_read , a.is_replied, a.bid_status, a.reply_id, a.bidding_id FROM bidding_details A INNER JOIN merchant_details B ON A.requestor_id = B.merchant_id where " + query + " and a.is_read='No' order by a.is_read asc Limit 0,3 "
    ##query = "SELECT initiator_id, date, search_query, price_opened, current_price, requestor_id, current_bidder , is_read , is_replied, bid_status, reply_id, bidding_id FROM bidding_details where " + query + " and is_read='No' order by is_read asc Limit 0,3 "
    print (query)
    cur.execute(query)
    #conn.commit();
    data = cur.fetchall()
    #for rows in data2:
        #print rows
        #name = rows[0]
        #description = rows[1]
        #price = rows[2]
        #quantity = rows[3]
        #category = rows[4]
        #subcategory = rows[5]
        #tags = rows[6]
        #image = rows[6]
    if (toedituser):
        print ("in if")
        print("Sud Dict 1 >>>>>>")
        print(dict(rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
        return bottle.template("viewproductbids.tpl", dict(rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    else:
        print ("ll")
        print("Sud Dict 2 >>>>>>>>>>>")
        print(dict(rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
        print(">>>>>>>>>>>>>>>>>")
        print(data[0][8])
        print(">>>>>>>>>>>>>>>>>")
        print(data[0][7])
        return bottle.template("viewproductbids.tpl", dict(rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    return bottle.template("viewproductbids.tpl", dict(rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))


#<-----Code by Niva------>
@bottle.get('/reply')
def present_replybids():
    username = login_check()  # see if user is logged in
    if (username is None):
        bottle.redirect("/login")
    #To Retrieve session username
    cookie = bottle.request.get_cookie("session")
    session_id = user.check_secure_val(cookie)
    cookierole = bottle.request.get_cookie("session_role")
    user_role = user.check_secure_val(cookierole)
    cookietheme = bottle.request.get_cookie("sessiontheme")
    session_theme = user.check_secure_val(cookietheme)
    msg_count = user.count_msg(session_id)
    print ("SSSS")
    print (msg_count)
    bidding_id = bottle.request.params.get("id")
    print ("SSaaaSS" + bidding_id)
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
    cur = conn.cursor()
    if (bidding_id):
        query = "SELECT initiator_id, date, search_query, price_opened, current_price, requestor_id, current_bidder , is_read , is_replied, bid_status, reply_id, bidding_id FROM bidding_details where bidding_id=%s"%(bidding_id)
        print (query)
        cur.execute(query)
        #conn.commit();
        data = cur.fetchall()
        for rows in data:
            print (rows)
            requestor_id = rows[5]
            current_bidder = rows[6]
            #bidding_id = rows[1]

        #conn.commit();
        return bottle.template("reply_bids.tpl", dict(requestor_id=requestor_id, message="", price="", current_bidder=current_bidder, session_id=session_id, session_theme=session_theme, user_role=user_role, msg_count=msg_count))
    else:
        return bottle.template("reply_bids.tpl", dict(requestor_id=requestor_id, message="", price="", current_bidder=current_bidder, session_id=session_id, session_theme=session_theme, user_role=user_role, msg_count=msg_count))
    return bottle.template("reply_bids.tpl", dict(requestor_id=requestor_id, message="", price="", current_bidder=current_bidder, session_id=session_id, session_theme=session_theme, user_role=user_role, msg_count=msg_count))


#<---Coded by niva--->
@bottle.post('/reply')
def process_replybids():
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
    cur = conn.cursor()
    #username = login_check()  # see if user is logged in
    to = bottle.request.forms.get("to")
    fromid = bottle.request.forms.get("from")
    message = bottle.request.forms.get("message")
    price = bottle.request.forms.get("price")
    bidding_id = bottle.request.params.get("id")
    submit = bottle.request.forms.get("submit")
    if submit == "Submit":
        print ("Inside Submit")
        if(bidding_id):
            print("Inside To edit user")
            if(not user.addreply(cur, to, fromid, price, message, bidding_id)):
                bottle.redirect("/reply")
            else:
                bottle.redirect("/products-bids")
        else:
            bottle.redirect("/products-bids")

    bottle.redirect("/products-bids")


#<-----Code by Niva------>
@bottle.get('/viewmsg')
def present_viewreplies():
    username = login_check()  # see if user is logged in
    if (username is None):
        bottle.redirect("/login")
    #To Retrieve session username
    cookie = bottle.request.get_cookie("session")
    session_id = user.check_secure_val(cookie)
    cookierole = bottle.request.get_cookie("session_role")
    user_role = user.check_secure_val(cookierole)
    cookietheme = bottle.request.get_cookie("sessiontheme")
    session_theme = user.check_secure_val(cookietheme)
    msg_count = user.count_msg(session_id)
    reply_id = bottle.request.params.get("id")
    bid_id = bottle.request.params.get("bid_id")
    if (reply_id):
        if(user_role == "0"):
            query_string = ""
        else:
            query_string = "`to_id`='" + session_id + "' and "
        query = "SELECT `to_id`, `from_id`, `message`, `date`, `price` FROM reply_details where " + query_string + " reply_id=%s"%(reply_id)
        print (query)
        cur.execute(query)
        #conn.commit();
        data = cur.fetchall()
        query2 = "SELECT `to_id`, `from_id`, `message`, `date`, `price` FROM reply_details where " + query_string + " bidding_id=%s"%(bid_id)
        print (query2)
        cur.execute(query2)
        #conn.commit();
        data2 = cur.fetchall()
        for rows in data:
            print (rows)
            requestor_id = rows[0]
            current_bidder = rows[1]
            message = rows[2]
            date = rows[3]
            price = rows[4]
        queryupdate = "UPDATE `bidding_details` SET `is_read`='Yes' where reply_id='%s'"%(reply_id)
        print (queryupdate)
        cur.execute(queryupdate)
            #bidding_id = rows[1]

        #conn.commit();
        return bottle.template("viewreplies.tpl", dict(rows=data2,requestor_id=requestor_id, message=message, price=price, current_bidder=current_bidder, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    else:
        return bottle.template("viewreplies.tpl", dict(rows=data2,requestor_id=requestor_id, message=message, price=price, current_bidder=current_bidder, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    return bottle.template("viewreplies.tpl", dict(rows=data2,requestor_id=requestor_id, message=message, price=price, current_bidder=current_bidder, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
##################################################################################################################################
#
#

@bottle.get('/index')
def index():
    conn = pymysql.connect(host='127.0.0.1', port=3306,
          user='root', passwd='', db='iwant')
    cur = conn.cursor()

    print ("innnnnnsssssn")
    #username = login_check()  # see if user is logged in
    print ("innnnnnsssssn")
    #print (username)
    if (not login_check()):
        print ("dddddddddddddd")
        bottle.redirect("/login")
    print("1111111111111")
    theme = bottle.request.params.get("theme")
    themecss = "blue.css"
    if(theme):
        if(theme == "blue"):
            themecss = "blue.css"
        elif(theme == "green"):
            themecss = "green.css"
        elif(theme == "red"):
            themecss = "red.css"
        else:
            themecss = "blue.css"
        cookiethem = themecss
        #cookiethem = user.make_secure_val(themecss)
        #print(cookiethem)
        bottle.response.set_cookie("sessiontheme", cookiethem)
    cookietheme = bottle.request.get_cookie("sessiontheme")
    print ("111")
    print (cookietheme)
    session_theme = themecss
    #To Retrieve session username
    cookie = bottle.request.get_cookie("session_id1")
    print("2222222:")
    print (cookie)
    query="SELECT `username` FROM `session` WHERE `session_id` = '%s'"%(cookie)
    print (query)
    cur.execute(query)
        #conn.commit();
    data = cur.fetchone()
    usernme = str(data[0])
    session_id = str(user.check_secure_val(cookie))
    print("@222222222222222:")
    print(session_id)
    cookierole = bottle.request.get_cookie("session_role")
    print (cookierole)
    user_role = user.check_secure_val(cookierole)
    #usernme = bottle.request.get_cookie("usrname")
    print("!!!!!!!!!")
    print(usernme)
    print (user_role)
	#Checks Admin Or Other Role
    if(user_role == "0"):
        subquerybid = "1"
        subquerycoupon = "1"
        subquerytrans = "1"
    else:
        subquerybid = "requestor_id='" + str(usernme) + "'"
        subquerycoupon = "receiver='" + str(usernme) + "'"
        subquerytrans = "receiver='" + str(usernme) + "'"

    msg_count = user.count_msg(usernme)
    print(msg_count)
    querybid = "SELECT initiator_id, date, search_query, price_opened, current_price, requestor_id, current_bidder , is_read , is_replied, bid_status, reply_id, bidding_id FROM bidding_details where " + subquerybid + " order by is_read asc "
    print (querybid)
    cur.execute(querybid)
    #conn.commit();
    databid = cur.fetchall()
    querycoupon = "SELECT transaction_id, sender, receiver, invoice_no, amount, payment_mode, date, status FROM transaction_details where " + subquerycoupon + " Limit 0, 4"
    print (querycoupon)
    cur.execute(querycoupon)
    #conn.commit();
    datacoupon = cur.fetchall()
    querytrans = "SELECT transaction_id, sender, receiver, invoice_no, amount, payment_mode, date, status FROM transaction_details where " + subquerytrans + " Limit 0, 4"
    print (querytrans)
    cur.execute(querytrans)
    #conn.commit();
    datatrans = cur.fetchall()

    return bottle.template("dashboard.tpl", dict(rowbid=databid, rowcoupon=datacoupon, rowtrans=datatrans, usernme=usernme, session_id=session_id, user_role=user_role, msg_count=msg_count, themecss=themecss, session_theme=session_theme))


@bottle.get('/coupons')
def display_coupons():
    username = login_check()  # see if user is logged in
    if (username is None):
        bottle.redirect("/login")
    #To Retrieve session username
    cookie = bottle.request.get_cookie("session")
    session_id = user.check_secure_val(cookie)
    cookierole = bottle.request.get_cookie("session_role")
    user_role = user.check_secure_val(cookierole)
    cookierole = bottle.request.get_cookie("session_role")
    user_role = user.check_secure_val(cookierole)
    cookietheme = bottle.request.get_cookie("sessiontheme")
    session_theme = user.check_secure_val(cookietheme)
    msg_count = user.count_msg(session_id)
    return bottle.template("coupon.tpl", dict(session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))


#<-----Code by Niva------>
@bottle.get('/help')
def present_help():
    username = login_check()  # see if user is logged in
    cookietheme = bottle.request.get_cookie("sessiontheme")
    session_theme = user.check_secure_val(cookietheme)
    if (username is None):
        bottle.redirect("/login")
    #To Retrieve session username
    #cookie = bottle.request.get_cookie("session")
    #session_id = user.check_secure_val(cookie)
    #msg_count = user.count_msg(session_id)
    return bottle.template("help.tpl", dict(name="", session_theme=session_theme, message=""))


@bottle.post('/help')
def process_help():
    return "<script>window.close();</script>"


#<-----Code by Niva------>
@bottle.get('/viewusers')
def present_viewusers():
    username = login_check()  # see if user is logged in
    if (username is None):
        bottle.redirect("/login")
    #To Retrieve session username
    cookie = bottle.request.get_cookie("session")
    session_id = user.check_secure_val(cookie)
    cookierole = bottle.request.get_cookie("session_role")
    user_role = user.check_secure_val(cookierole)
    cookietheme = bottle.request.get_cookie("sessiontheme")
    session_theme = user.check_secure_val(cookietheme)
    msg_count = user.count_msg(session_id)
    query = "SELECT username, usr_email, usr_role, usr_role, usr_status FROM login_details "
    print (query)
    cur.execute(query)
    #conn.commit();
    data = cur.fetchall()
    topost = bottle.request.params.get("topost")
    if (topost):
        query2 = "SELECT username, password, usr_email, usr_role, mobile_number, usr_role, usr_status FROM login_details where username = '%s' " %(topost)
        print (query2)
        cur.execute(query2)
        #conn.commit();
        data2 = cur.fetchall()
        for rows in data2:
            print (rows)
            username = rows[0]
            password = rows[1]
            email = rows[2]
            contactno = rows[4]
            #conn.commit();
        return bottle.template("viewusers.tpl", dict(user_name=username, email=email, mobile_number=contactno, rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    else:
        return bottle.template("viewusers.tpl", dict(user_name="", email="", mobile_number="", rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    return bottle.template("viewusers.tpl", dict(user_name="", email="", mobile_number="", rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))


#<---Coded by niva--->
@bottle.post('/viewusers')
def process_viewusers():
    #username = login_check()  # see if user is logged in
    user_name = bottle.request.forms.get("user_name")
    submit = bottle.request.forms.get("submit")
    if submit == "Submit":
        print ("Inside Submit")
        bottle.redirect("/viewusers?topost=%s" % (user_name))

    bottle.redirect("/viewusers")


#<-----Code by Niva------>
@bottle.get('/editusers')
def present_editusers():
    username = login_check()  # see if user is logged in
    if (username is None):
        bottle.redirect("/login")
    #To Retrieve session username
    cookie = bottle.request.get_cookie("session")
    session_id = user.check_secure_val(cookie)
    cookierole = bottle.request.get_cookie("session_role")
    user_role = user.check_secure_val(cookierole)
    cookietheme = bottle.request.get_cookie("sessiontheme")
    session_theme = user.check_secure_val(cookietheme)
    msg_count = user.count_msg(session_id)
    query = "SELECT username, usr_email, usr_role, usr_role, usr_status FROM login_details "
    print (query)
    cur.execute(query)
    #conn.commit();
    data = cur.fetchall()
    topost = bottle.request.params.get("topost")
    if (topost):
        query2 = "SELECT username, password, usr_email, mobile_number, usr_role, usr_status FROM login_details where username = '%s' " %(topost)
        print (query2)
        cur.execute(query2)
        #conn.commit();
        data2 = cur.fetchall()
        for rows in data2:
            print (rows)
            username = rows[0]
            password = rows[1]
            email = rows[2]
            status = rows[5]
            role = rows[4]
            contactno = rows[3]
            #conn.commit();
        return bottle.template("editusers.tpl", dict(user_name=username, password=password, email=email, status=status, role=role, mobile_number=contactno, rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    else:
        return bottle.template("editusers.tpl", dict(user_name="", password="", email="", status="", role="", mobile_number="", rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    return bottle.template("editusers.tpl", dict(user_name="", password="", email="", status="", role="", mobile_number="", rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))


#<---Coded by niva--->
@bottle.post('/editusers')
def process_editusers():
    #username = login_check()  # see if user is logged in
    user_name = bottle.request.forms.get("user_name")
    submit = bottle.request.forms.get("submit")
    if submit == "Submit":
        print ("Inside Submit")
        bottle.redirect("/editusers?topost=%s" % (user_name))

    bottle.redirect("/editusers")


#<-----Code by Niva------>
@bottle.get('/users')
def present_users():
    username = login_check()  # see if user is logged in
    if (username is None):
        bottle.redirect("/login")
    #To Retrieve session username
    cookie = bottle.request.get_cookie("session")
    session_id = user.check_secure_val(cookie)
    cookierole = bottle.request.get_cookie("session_role")
    user_role = user.check_secure_val(cookierole)
    cookietheme = bottle.request.get_cookie("sessiontheme")
    session_theme = user.check_secure_val(cookietheme)
    msg_count = user.count_msg(session_id)
    #error = bottle.request.params.get("er")
    query = "SELECT username, usr_email, usr_role, usr_role, usr_status FROM login_details "
    print (query)
    cur.execute(query)
    #conn.commit();
    data = cur.fetchall()
    return bottle.template("adminusers.tpl", dict(user_name="", email="", password="", confirmpwd="", mobile_number="", rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))


#<-----Code by Niva------>
@bottle.get('/pending-transaction')
def present_pendingtransactions():
    username = login_check()  # see if user is logged in
    if (username is None):
        bottle.redirect("/login")
    #To Retrieve session username
    cookie = bottle.request.get_cookie("session")
    session_id = user.check_secure_val(cookie)
    cookierole = bottle.request.get_cookie("session_role")
    user_role = user.check_secure_val(cookierole)
    cookietheme = bottle.request.get_cookie("sessiontheme")
    session_theme = user.check_secure_val(cookietheme)
    msg_count = user.count_msg(session_id)
    deleteid = bottle.request.params.get("deleteuser")
    if(deleteid):
        query2 = "DELETE FROM transaction_details where transaction_id = '%s' " % (deleteid)
        print (query2)
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
        cur1 = conn.cursor()
        #conn.commit();
        #cur1.close();
        if(cur1.execute(query2)):
            print( "Inside Execute")
            conn.commit();
            bottle.redirect("/pending-transaction?error=success")
    toedituser = bottle.request.params.get("toedit")
    #error = bottle.request.params.get("er")
    if(user_role == "0"):
        query_string = ""
    else:
        query_string = "receiver='" + session_id + "' and "
    query = "SELECT transaction_id, sender, receiver, invoice_no, amount, payment_mode, date, status FROM transaction_details where " + query_string + " status='0' "
    print (query)
    cur.execute(query)
    #conn.commit();
    data = cur.fetchall()
    #for rows in data2:
        #print rows
        #name = rows[0]
        #description = rows[1]
        #price = rows[2]
        #quantity = rows[3]
        #category = rows[4]
        #subcategory = rows[5]
        #tags = rows[6]
        #image = rows[6]
    if (toedituser):
        return bottle.template("pendingtransactions.tpl", dict(rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    else:
        return bottle.template("pendingtransactions.tpl", dict(rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    return bottle.template("pendingtransactions.tpl", dict(rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))


#<-----Code by Niva------>
@bottle.get('/products-bidsread')
def present_viewreadbids():
    username = login_check()  # see if user is logged in
    if (username is None):
        bottle.redirect("/login")
    #To Retrieve session username
    cookie = bottle.request.get_cookie("session")
    session_id = user.check_secure_val(cookie)
    cookierole = bottle.request.get_cookie("session_role")
    user_role = user.check_secure_val(cookierole)
    cookietheme = bottle.request.get_cookie("sessiontheme")
    session_theme = user.check_secure_val(cookietheme)
    msg_count = user.count_msg(session_id)
    deleteid = bottle.request.params.get("deleteuser")
    if(deleteid):
        query2 = "DELETE FROM bidding_details where bidding_id = '%s' " % (deleteid)
        print (query2)
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
        cur1 = conn.cursor()
        #conn.commit();
        #cur1.close();
        if(cur1.execute(query2)):
            print ("Inside Execute")
            conn.commit();
            bottle.redirect("/products-bidsread?error=success")
    accept_id = bottle.request.params.get("accept_id")
    reject_id = bottle.request.params.get("reject_id")
    if(accept_id):
        status = '1'
        if(user.ins_transaction(status,accept_id)):
            bottle.redirect("/products-bidsread?error=success")
    elif(reject_id):
        status = '2'
        #if(user.ins_transaction(status,reject_id)):
        bottle.redirect("/products-bidsread?error=success")
    toedituser = bottle.request.params.get("toedit")
    #error = bottle.request.params.get("er")
    query = "SELECT initiator_id, date, search_query, price_opened, current_price, requestor_id, current_bidder , is_read , is_replied, bid_status, reply_id, bidding_id FROM bidding_details where requestor_id='%s' and is_read='Yes' order by is_read asc Limit 0,3 " % (session_id)
    print (query)
    cur.execute(query)
    #conn.commit();
    data = cur.fetchall()
    #for rows in data2:
        #print rows
        #name = rows[0]
        #description = rows[1]
        #price = rows[2]
        #quantity = rows[3]
        #category = rows[4]
        #subcategory = rows[5]
        #tags = rows[6]
        #image = rows[6]
    if (toedituser):
        return bottle.template("viewreadbids.tpl", dict(rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    else:
        return bottle.template("viewreadbids.tpl", dict(rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
    return bottle.template("viewreadbids.tpl", dict(rows=data, session_id=session_id, user_role=user_role, session_theme=session_theme, msg_count=msg_count))
###################################################################################################################################################
#*************************************************************************************************************************************************#
#                                                |-----------------------------|                                                                  #
##                                               | Data to Android Application |                                                                 ##
#                                                |-----------------------------|                                                                  #
#*************************************************************************************************************************************************#
###################################################################################################################################################

###########
# Login Validation  - Gets username and Password from Android and Return if it matches to database
###########
#
# Input - Json  {USername : <Value>, Password : Value}
# Output- JSON {Status: <Boolean>}
# URL: 54.187.96.220/Android/Login
#
@bottle.post('/Android/Login')
#
def process_androidLogin():
	## Get the Json from User
	login_str= bottle.request.json
	print (login_str)
	print (type(login_str))
    #
	#login_string=json.dumps(login_str)
	#print kkk
	#login_string=json.loads(login_str)[0]
	#print login_string
	username = login_str["username"]
	print username
	password = login_str["password"]
	print password
	usr_status=[]
	status = {}
	list_status = {}
	#list_status[]
	if (user.validate_login(username, password)):
	    # Login Success
		print ("in if")
		list_status['status'] = True
	else:
	    # Login Fails
		print "in ellse"
		list_status['status'] = False
	usr_status.append(list_status)
	#print usr_status
	print list_status
	return list_status
	#status["status"] = usr_status
	#print status
	#return status
#######################################################################################################################################
#
####
# Sign Up Form  - Registration Page to Add user
#
#
# Input - Json  {stremail : <Value>, strPassword : Value, strFirstName : <Value>, strLastName : <Value>}
# Output- JSON {Status: <Boolean>}
# URL: 54.187.96.220/Android/Signup
#
@bottle.post('/Android/Signup')
#
def process_androidSignup():
	## Get the Json from User
	signup_str= bottle.request.json
	print signup_str
    #
	#signup_string=json.loads(signup_str)[0]
	username = signup_str['stremail']
	print username
	password = signup_str['strPassword']
	print password
	confirmpwd = signup_str['strPassword']
	email = signup_str['stremail']
	mobile_number=0000
	usr_status=[]
	status = {}
	list_status = {}
	#list_status[
	usr_role = 1
	if(user.register(cur, username, password, mobile_number, confirmpwd, email, usr_role)):
		
		list_status['Signup_status'] = True
		print "in if"
		print list_status
		return list_status
		print "over"
	else:
		print "in Else"
		list_status['Signup_status'] = False
		return list_status
		print list_status
        #return "<script>window.close();</script>"
	#usr_status.append(list_status)
	#return list_status
	#mails["status"] = usr_status
	#return status
	
#######################################################################################################################################



# Send information on message and Notification
# ON load function to Android Home Screen

@bottle.get('/Android/homescreen/<Userid>')

def Send_notificationcount(Userid):
	print
	conn = pymysql.connect(host='127.0.0.1', port=3306,user='root', passwd='', db='iwant')
	cur = conn.cursor()
	query = "SELECT count(is_read) from reply_details where 'to_id' = '%s' AND is_read = 'NO'" %(Userid);
	print query
	cur.execute(query)
	conn.commit();
	data = cur.fetchone()[0]
#	assert type(data) is str

	return dumps({'count' : data})	
	#for rows in data2:

# View Notification
# View the list of notification by the user

@bottle.get('/Android/Sendnotification/<Userid>')

def Send_notification(Userid):
	conn = pymysql.connect(host='127.0.0.1', port=3306,user='root', passwd='', db='iwant')
	cur = conn.cursor()
	query = "SELECT * from reply_details WHERE `to_id` = '%s'" %(Userid);
	#query = "SELECT * from reply_details where 'to_id' like '%s' " %(Userid);
	
	print query
	cur.execute(query)
	conn.commit();
	kms = []
	notify = {}
	data = cur.fetchall()
	for rows in data:
		list_arr = []
		list_row = {}
		date = rows[4].strftime( '%d %b, %H:%M' )
		print date
		msg = rows[2] + " had responded to your bid on " + date
		print msg
		list_row['reply_id'] = rows[0]
		list_row['msg'] = msg
		print "-----------"
		kms.append(list_row)
	notify['notification'] = kms
	 	
	print notify
	return dumps(notify)

# Display all the message for the particular users
# Display Mailbox
	
@bottle.get('/Android/ViewMessage/<Userid>')

def View_Message(Userid):
        print ("in View  Message-----------")
	conn = pymysql.connect(host='127.0.0.1', port=3306,user='root', passwd='', db='iwant')
	cur = conn.cursor()
	query = "SELECT * from reply_details where `to_id` = '%s' " %(Userid);
        print (query)
	cur.execute(query)
	conn.commit();
	mailbox = cur.fetchall()
	print mailbox
	mail_line=[]
	mails={}
	for msg in mailbox:
		list_arr = []
		list_row = {}
		list_row['reply_id'] = msg[0]
		list_row['bidding_id'] = msg[1]
		list_row['from_id'] = msg[2]
		list_row['date'] = msg[4].strftime( '%d %b, %H:%M' )
		list_row['message'] = msg[5]
		list_row['price'] = msg[6]
		list_row['is_read'] = msg[7]
		mail_line.append(list_row)
	mails["messages"] = mail_line
		
	print mails
	return dumps(mails)

# Displays the Full message and the fill status of the bid. It gives the status of the particular bids and gives bid amount in each phase
# Input is the bidding_id
# Output is the full msg list

@bottle.get('/Android/MessageList/<Userid>/<bidding_id>')

def Message_loop(Userid,bidding_id):
        print ("in Android MessageList Userid Bid id")
	conn = pymysql.connect(host='127.0.0.1', port=3306,user='root', passwd='', db='iwant')
	cur = conn.cursor()
	query = "SELECT * FROM `bidding_details` WHERE `bidding_id` = %s " %(bidding_id) ;
	print query
	cur.execute(query)
	conn.commit();
	maillist = cur.fetchone()
	print maillist
	mail_line=[]
	mails={}
	list_row = {}
	list_row['Sl_no'] = 1
	list_row['From_id']=maillist[1]
	list_row['bid_id']=maillist[0]
	list_row['role'] = "Customer"
	list_row['To_id']=maillist[6]
	list_row['Status']=maillist[9]
	list_row['Description']=maillist[3]
	list_row['date'] = maillist[2].strftime( '%d %b, %H:%M' )
	list_row['Bid_price'] = maillist[3]
	list_row['is_Read'] = maillist[7]
	list_row['is_reply'] = maillist[8]
	list_row['reply_status'] = maillist[10]
	mail_line.append(list_row)
	
	query1 = "SELECT * FROM `reply_details` WHERE `bidding_id` = %s" %(bidding_id);
	print("DUF>>>>>>")
	print(query1)
	curr = conn.cursor()
	curr.execute(query1)
	conn.commit();
	reply_list = curr.fetchall()
	print("DUF>>>>>>")
	print(reply_list)
	inc = 2
	for rows in reply_list:
		list_row = {}
		print("DUF 3 >>>>>")
		print(rows)
		list_row['Sl_No'] = inc
		list_row['bid_id']=rows[1]
		list_row['From_id']=rows[2]
		list_row['Description']=rows[5]
		list_row['date'] = rows[4].strftime( '%d %b %H:%M' )
		list_row['Bid_price'] = rows[6]
		list_row['is_Read'] = rows[7]
		list_row['is_reply'] = rows[8]
		list_row['To_id'] = rows[3]
		mail_line.append(list_row)
		inc = inc + 1
	mails["messages"] = mail_line
	return mails

###########################################################################
### Stores the reply msg from the user
### update reply_details table and bidding_details table
###########################################################################

@bottle.post('/Android/MessageList')
#
#def accpet_bid():
	

def process_replybid():
	#print msg_list
	reply_string= bottle.request.json
	print reply_string
	
	print "----------"
	## Input Values are in JSON's Format
	## Username
	## Reply id
	## Merchant id
	## Price quoted
	## Current mail type

	kkk=json.dumps(reply_string)
	print kkk
	#reply_string=json.loads.(reply_str)[0]
	username = reply_string['user_name']
	bid_id = reply_string['bid_id']
	merchant_id = reply_string['to_id']
	price = reply_string['bid_price']
	message = reply_string['bid_data']
	conn = pymysql.connect(host='127.0.0.1', port=3306,user='root', passwd='', db='iwant')
	cur = conn.cursor()
	query = "UPDATE `reply_details` SET `is_read`= 'Yes',`is_replied`='Yes' WHERE `bidding_id` = '%s' " %(bid_id) ;	
	cur.execute(query)
	conn.commit();
	formatter=(bid_id, username, merchant_id, message, price)
	q2= "INSERT INTO `reply_details`(`bidding_id`, `from_id`, `to_id`, `date`, `message`, `price`, `is_read`, `is_replied`) VALUES ('%s', '%s', '%s', now(), '%s', '%s', 'No', 'No')" % formatter
	print ("q2 >>>>>>>>>>"+q2)
	cur.execute(q2)
	conn.commit();

@bottle.get('/Android/Viewbids/<Userid>')

def View_bids(Userid):
	
	conn = pymysql.connect(host='127.0.0.1', port=3306,user='root', passwd='', db='iwant')
	cur = conn.cursor()
	print (Userid);
	cur = conn.cursor()
	query = "SELECT * from reply_details where `to_id` = '%s' " %(Userid);
	print query
	cur.execute(query)
	conn.commit();
	mailbox = cur.fetchall()

##########################################################
######################SUDHARSHAN START####################
##########################################################
@route('/getproducts')
def getProducts():
    return getProducts()

@route('/gettraveldeals')
def getTravelDeals():
    return getTravelDeals()
    #deals = {}
    #deals['deals'] = DBHandler.getTravelDeals()
    #return deals

@route('/getproductdeals')
def getGoodsDeals():
    return getProductDeals()

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
    r = s.query(query)
    products = {}
    details = []
    for hit in r.results:
        if hit["score"] < 0.3:
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
    print query
    r = s.query(query)
    merchants = []
    added_Merchants = {}
    for hit in r.results:
        if hit["score"] < 0.3:
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
    updateBiddingDetails(username, query, price, merchants)

def getProduct(id):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
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
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
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
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
    conn.autocommit(1)
    cursor = conn.cursor()
    for merchant in merchants:
        print "DBHandle >>>>> "+merchant
        formatter = ("open", username, price, "now()", username, "no", "no", price, merchant, query)
        req = "INSERT INTO bidding_details(bid_status, current_bidder, current_price, date, initiator_id, is_read, is_replied, price_opened, requestor_id, search_query) VALUES('%s', '%s', %s, %s, '%s', '%s', '%s', %s, '%s', '%s');" % formatter
        print req
        cursor.execute(req)

bottle.debug(True)
#bottle.run(host='192.168.1.19', port=9000)
bottle.run(host='0.0.0.0', port=8989)
