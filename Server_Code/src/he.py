# -*- coding: utf-8 -*-
import cgi
import re
import os
import hmac
import random
import string
import hashlib
import pymysql
import session
import sys
import bottle
import datetime
import session
from config import open_connection



# makes a little salt
STATIC_ROOT = "D:\iwant\i-Want\iwantv2\static"

def make_salt():
    salt = ""
    for i in range(5):
        salt = salt + random.choice(string.ascii_letters)
    return salt

# implement the function make_pw_hash(name, pw) that returns a hashed password
# of the format:
# HASH(pw + salt),salt
# use sha256


def make_pw_hash(pw, salt=None):
    if (salt is None):
        salt = make_salt()
        pw_bytes = pw.encode('utf-8')
        salt_bytes = salt.encode('utf-8')
        return hashlib.sha256(pw_bytes + salt_bytes).hexdigest() + "," + salt


def make_pw_hash1(pw,salt):
    if (salt == None):
        salt = make_salt();
        print(salt)
    pw_bytes = pw.encode('utf-8')
    salt_bytes = salt.encode('utf-8')
    return hashlib.sha256(pw_bytes + salt_bytes).hexdigest()+","+ salt


# validates that the user information is valid, return True of False
# and fills in the error codes


def validate_signup(username, password, verify, email, errors, Role):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    PASS_RE = re.compile(r"^.{3,20}$")
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

    errors['username_error'] = ""
    errors['password_error'] = ""
    errors['verify_error'] = ""
    errors['email_error'] = ""
    errors['mobile_error'] = ""
#
    if not USER_RE.match(username):
        errors['username_error'] = "invalid username. try again"
        return False

    if not PASS_RE.match(password):
        errors['password_error'] = "invalid password."
        return False
    if password != verify:
        errors['verify_error'] = "password must match"
        return False
    if email != "":
        if not EMAIL_RE.match(email):
            errors['email_error'] = "invalid email address"
            return False
    return True
    if Role != "":
        return True

#########################################################################################
# validates the login, returns True if it's a valid user login. false otherwise
##
def validate_login(username, password):
    conn = pymysql.connect(host='127.0.0.1', port=3306,
    user='root', passwd='', db='iwant')

    user = conn.cursor()
    print("inside Validate _login")
    print(username,password)
    session_id = session.start_session(user, username)
    if (session_id == -1):
        print ("session failed")
        bottle.redirect("/internal_error")
        cookie = session.make_secure_val(session_id)
        bottle.response.set_cookie("session", cookie)
    else:
        print ("session suceeded")
        cookie = session.make_secure_val(session_id)
        bottle.response.set_cookie("session", cookie)
    try:
        print("in try")
        sql = "SELECT username, password, salt, usr_email, mobile_number, usr_role, usr_status FROM login_details WHERE username = '%s' " % (username)
        print("in Find")
        print(sql)
        if(not user.execute(sql)):
            return False
        # Fetch all the rows in a list of lists.
        #print "suceeed"
        results = user.fetchall()
        print "Su"
        #status = results[6]
        #status_id = session.make_secure_val(status)
        #bottle.response.set_cookie("session_status", status_id)

    except Exception,e:
        print (e)
        print("Unable to query database for user")
        return bottle.redirect("/login?error=3")

    if results is None:
        print("User not in database")
        return False
    for row in results:
        print (row)
        userrole = row[5]
        print (userrole)
        user_role = session.make_secure_val(userrole)
        bottle.response.set_cookie("session_role", user_role)

        salt = row[1].split(',')[1]
        print (salt)
        hashed_pwd = make_pw_hash1(password,salt)
        print (hashed_pwd)
        print ("------------")
        print (row[1])
        if (row[1] == hashed_pwd):
            start_session(username)
            print("start_session-----------")
            sql4 = "SELECT * FROM `session` WHERE `username` = '%s'"%(username)
            print (sql4)
            if(user.execute(sql4)):
                 results = user.fetchone()
                 print (results)
                 session_id= str(results[0])
                 print (session_id)
                 print ("__________")
                 bottle.response.set_cookie("session_id1", session_id)
                 aaa = bottle.request.get_cookie("session_id1")
                 print (aaa)
#   #         session_row = user.fetchone()
#    #        print ("SSS_")
#     #       print (session_row)
#      #      bottle.response.set_cookie("session_id", user_role)
#       #     print("user password is not a match")
            return True
    print ("No Match found")
    return False
    # looks good
    #for key in user:
        #user_record[key] = user[key]                      ## perform a copy
    #print("in user ")
    #print(firsttime_check)
    #print(user['firsttime'])
    #firsttime_check = user['firsttime']
    #Login = 1
    #return (firsttime_check, Login)
# will start a new session id by adding a new document to the sessions collection


def start_session(username):
    print("started new session")

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
    cur = conn.cursor()

    try:
        insquery = "INSERT INTO `session`(`username`, `time`) VALUES ('%s', now())"%(username)
        if(cur.execute(insquery)):
            conn.commit()
            bottle.response.set_cookie("username", username)
            return str(username)
        else:
            return -1
    except:
        print(("Unexpected error on start_session:", sys.exc_info()[0]))
        return -1

    return str(username)


# will send a new user session by deleting from sessions table
def end_session(session_id):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
    session = conn.cursor()
    # this may fail because the string may not be a valid bson objectid
    try:
        session.execute("delete from session WHERE username = %s" % (session_id))

    except:
        print(("Unexpected error on end_session:", sys.exc_info()[0]))
        return -1


# if there is a valid session, it is returned
def get_session(session_id):

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
    session = conn.cursor()

    # this may fail because the string may not be a valid bson objectid
    #try:
        #id = bson.objectid.ObjectId(session_id)
    #except:
        #print("bad sessionid passed in")
        #return None
    selectquery = "SELECT * FROM `session` WHERE `username` = '%s'" % (session_id)
    if(session.execute(selectquery)):
        print("returning a session or none")
        return session_id
    return session_id


# creates a new user in the database
def newuser(username, password, email, mobile_num, Role, db ):
    # the hashed password is what we insert
    password_hash = make_pw_hash(password)

    #user = {'_id':username, 'password':password_hash, 'firsttime' : "T"}
    #if (email != ""):
        #user['email'] = email
    #if (Role != ""):
        #user['Role'] = Role


    #users = db.users
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
    add_user = conn.cursor()
    status = 1

    try:
        add_user.execute("INSERT INTO login_details"
        "(username, password, usr_email, mobile_number, usr_role, usr_status)"
        "VALUES (% (username)s, %(password_hash)s, %(email)s, %(mobile_num)s,%(Role)s, %(status)s)")

    except pymysql.err.OperationalError as e:
        print(("Could not take flights from database", e))
        return False
    return True


#########################################################################################################
#  Checks for the username already present in database If present then throws up error                  #
# Insert the values into fDB.                                                                            #
#########################################################################################################
def register(cur, username, password, mobile_number, confirmpwd, email, usr_role):
    # Open Database connections
    # Passwords is hashed - Encrypted for security purpose SHA256 encryption used.
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
    curr = conn.cursor()	
    password_hash = make_pw_hash(password)
    print ("------------")
    print (password_hash)
    if (password!=confirmpwd):
        # Checks the password and confirm password
        return bottle.redirect("/register?error=1")
    try:
        print (username)
        sql = "SELECT username, password, usr_email, usr_role, usr_status FROM login_details WHERE username='%s' or usr_email='%s' LIMIT 1" % (username ,email)
        cur.execute(sql)
        results = cur.fetchone()
        if (results):
            print("User Already Exist")
            #	return bottle.redirect("/register?error=2")
            return False
        else:
            #cur.close()
            print("Inside Insert loop")
            usr_status = 1
            sql2 = "INSERT INTO login_details (username, password, mobile_number, usr_email,usr_role,usr_status) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"%(username ,password_hash, mobile_number, email, usr_role, usr_status)
            print (sql2)
            #cur = conn.cursor()
            if(curr.execute(sql2)):
                conn.commit()
                return True
            else:
                print ("In INsert Error")
                return false
            return bottle.redirect("/error")
    except:
        #return bottle.redirect("/register?error=1")
        #print("Unable to query database for user")
        return false


#<----Code By Niva----->
# Edit and Update Users
def update_users(cur, username, password, mobile_number, confirmpwd, email, toedit):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
    cur = conn.cursor()
    # the hashed password is what we insert

    if (password!=confirmpwd):
        return bottle.redirect("/adminadd_users?error=2")
    try:
        print (username)
        sql = "SELECT username, password, usr_email, usr_role, usr_status FROM login_details WHERE username='%s' LIMIT 1" % (toedit)
        print (sql)
        cur.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cur.fetchone()
        db_pwd = results[1]
        #salt = results[3]
        #usr_email = results[4]
        #usr_role = results[5]
        #usr_status = results[6]
        print ("ssss")
        if (not(db_pwd==password)):
            password_hash = make_pw_hash(password)
            print("Password hashed")
        elif (db_pwd==password):
            password_hash = password
            print("password not hashed")
        usr_role = 1
        usr_status = 1
        sql2 = "UPDATE login_details SET username = '%s', password = '%s', mobile_number = '%s', usr_email = '%s',usr_role = '%s',usr_status = '%s' WHERE username = '%s'"%(username ,password_hash, mobile_number, email, usr_role, usr_status, toedit)
        print (sql2)
        cur = conn.cursor()
        if(cur.execute(sql2)):
            print ("Inside Execute")
            conn.commit()
            bottle.redirect("/adminadd_users")
        else:
            return bottle.redirect("/adminadd_users?error=3")
        return bottle.redirect("/adminadd_users")
    except:
        #return bottle.redirect("/register?error=1")
        #print("Unable to query database for user")
        return True


#<----Code By Niva----->
# Add new Products
def addproducts(cur, name, description, price, quantity, category, subcategory, tags, image, image_old):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
    cur = conn.cursor()
    try:
        image_name = image.filename
        sql = "SELECT name, description, price, quantity, category, subcategory, tags, image FROM product_details where name = '%s' " %(name)
        print (sql)
        cur.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cur.fetchone()
        #salt = results[3]
        #usr_email = results[4]
        #usr_role = results[5]
        #usr_status = results[6]
        print ("ssss")
        if (results):
            print("User Already Exist")
            return bottle.redirect("/addproducts?error=1")
            return False
        else:
            #cur.close()
            print("Inside Insert loop")
            if image is not None:
                name1, ext = os.path.splitext(image.filename)
                if ext not in ('.png', '.jpg', '.pdf', '.mp3', '.doc', '.docx', '.txt'):
                    return "File extension not allowed."
                save_path = STATIC_ROOT
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                file_path = "{path}/{file}".format(path=save_path, file=image.filename)
                with open(file_path, 'wb') as open_file:
                    open_file.write(image.file.read())
                    print("file saved successfully")

            sql2 = "INSERT INTO product_details (name, description, price, quantity,category,subcategory,tags, image) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(name ,description, price, quantity, category, subcategory, tags, image_name)
            print (sql2)
            cur = conn.cursor()
            if(cur.execute(sql2)):
                print ("Inside Execute")
                conn.commit()
                bottle.redirect("/viewproducts")
                return True
            else:
                return bottle.redirect("/addproducts?error=3")
            return bottle.redirect("/addproducts")
    except:
        #return bottle.redirect("/register?error=1")
        #print("Unable to query database for user")
        return True


#<----Code By Niva----->
# Edit and Update Products
def update_product(cur, name, description, price, quantity, category, subcategory, tags, image, image_old, toedit):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
    cur = conn.cursor()
    try:
        if image is not None:
            image_name = image.filename
        else:
            image_name = image_old
        print (name, image_name)
        sql = "SELECT name, description, price, quantity, category, subcategory, tags, image FROM product_details where product_id = '%s' " %(toedit)
        print (sql)
        cur.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cur.fetchone()
        #name = results[1]
        #salt = results[3]
        #usr_email = results[4]
        #usr_role = results[5]
        #usr_status = results[6]
        print ("ssss")
        if image is not None:
            name1, ext = os.path.splitext(image.filename)
            if ext not in ('.png', '.jpg', '.pdf', '.mp3', '.doc', '.docx', '.txt'):
                return "File extension not allowed."
            save_path = STATIC_ROOT
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            file_path = "{path}/{file}".format(path=save_path, file=image.filename)
            with open(file_path, 'wb') as open_file:
                open_file.write(image.file.read())
                print("file saved successfully")
        else:
            image_name = image_old
        sql2 = "UPDATE product_details SET name = '%s', description = '%s', price = '%s', quantity = '%s',category = '%s', subcategory = '%s',tags = '%s' ,image = '%s' WHERE product_id = '%s'"%(name ,description, price, quantity, category, subcategory, tags, image_name, toedit)
        print (sql2)
        cur = conn.cursor()
        if(cur.execute(sql2)):
            print ("Inside Execute")
            conn.commit()
            bottle.redirect("/viewproducts")
        else:
            return bottle.redirect("/addproducts?error=3")
        return bottle.redirect("/addproducts")
    except:
        #return bottle.redirect("/register?error=1")
        #print("Unable to query database for user")
        return True


#<----Code By Niva----->
# Add new Products
def addreply(cur, to, fromid, price, message, bidding_id):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
    cur = conn.cursor()
    try:
        #cur.close()
        print("Inside Insert loop")
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        #print to
        sql2 = "INSERT INTO reply_details (`from_id`, `to_id`, `price`, `message`, `bidding_id`, `date`, `is_read`, `is_replied`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', 'Yes', 'Yes')" %(to ,fromid, price, message, bidding_id, date)
        #print sql2
        cur = conn.cursor()
        if(cur.execute(sql2)):
            print ("Inside Execute")
            conn.commit()
            rowid = calltable(bidding_id)
            reply_id = rowid[0]
            sql3 = "UPDATE bidding_details SET is_read = 'No', is_replied = 'Yes', current_price = '%s', current_bidder = '%s',requestor_id = '%s',reply_id = '%s' WHERE bidding_id = '%s'"%(price ,fromid, to, reply_id, bidding_id)
            print (sql3)
            cur = conn.cursor()
            if(cur.execute(sql3)):
                bottle.redirect("/products-bids")
            return True
        else:
            return bottle.redirect("/reply?error=3")
        return bottle.redirect("/reply")
    except:
        #return bottle.redirect("/register?error=1")
        #print("Unable to query database for user")
        return True


def calltable(bidding_id):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
    cur = conn.cursor()
    query = "SELECT max(reply_id) FROM reply_details where bidding_id=%s" %(bidding_id)
    print (query)
    cur.execute(query)
    #conn.commit();
    data = cur.fetchall()
    return data[0]


def count_msg(session_id):
    cookie = bottle.request.get_cookie("session")
    print (session_id) # = check_secure_val(cookie)
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
    cur = conn.cursor()
    query = "SELECT count(bidding_id) FROM bidding_details A INNER JOIN merchant_details B ON A.requestor_id = B.merchant_id where B.Merchant_name = 'billa'"
#    query = "SELECT count(bidding_id) FROM `bidding_details` where requestor_id = '%s' and `is_read` = 'No'" % (session_id)
    print (query)
    cur.execute(query)
    #conn.commit();
    data = cur.fetchall()
    return data[0]

def ins_transaction(status,transid):
    query = "SELECT `to_id`, `from_id`, `message`, `date`, `price` FROM reply_details where reply_id=(select max(reply_id) from reply_details)"
    print (query)
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
    cur = conn.cursor()
    cur.execute(query)
    #conn.commit();
    data = cur.fetchall()
    for datas in data:
        receiver=datas[0]
        sender=datas[1]
        date=datas[3]
        amount=datas[4]
    invoice_no = "INV_000"+str((int(transid) + 1))
    query2 = "INSERT into transaction_details (`sender`, `receiver`, `invoice_no`, `amount`, `date`, `status`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (sender, receiver, invoice_no, amount, date, status)
    print (query2)
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
    cur1 = conn.cursor()
    #conn.commit();
    #cur1.close();
    if(cur1.execute(query2)):
        print ("Inside Execute")
        #conn.commit();
        return True
#####################################################################################
#                                                                                   #
# Insert the merchant information in the merchant table and creates an merchant id  #
# Loads the login template from the static folder                                   #
#                                                                                   #
#####################################################################################

def addmerchant(cur, username):
    try:
        #cur.close()
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='iwant')
        curr = conn.cursor()
        #date = datetime.datetime.now().strftime("%Y-%m-%d")
        sql2 = "INSERT INTO `merchant_details` (`username`, `merchant_name`) VALUES ('%s', '%s')" % (username, username)
        if(curr.execute(sql2)):
            conn.commit()
            return True
        else:
            print("Database Error Can't able to connect DB")
            return False
    except:
        print("Unable to query database for user")
        return True

SECRET = 'thisisnotsecret'
def hash_str(s):

    hashing = hmac.new(b'SECRET', b's')
    return hashing
# call this to hash a cookie value
def make_secure_val(s):
    print ("in make_secure_val")
    print (s)
    return "%s|%s" % (s, hash_str(s))

# call this to make sure that the cookie is still secure
def check_secure_val(h):
    print("SUD >>>>>>>>>>>>>>")
    print (h)
    if h is None:
        return h
    val = h.split('|')[0]
    temp = make_secure_val(val)
    #if h == temp:
    return val
