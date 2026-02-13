from flask import Flask
import security_core 
import register
import jsonify
import requests
import login
import sqlite3
import time
import math
import commerce_core as shop

app=Flask(__name__)
DB="business_platform.db"
def connect():
    return sqlite3.connect(DB)
def now():
    return int(time.time())
def auth ():
    token=requests.headers.get("Authorization")
    if not token:
        return None
    return token(token)
def distance(lat1,lon1,lat2,lon2):
    r=6371
    dlat=math.radians(lat2-lat1)
    dlon=math.radians(lon2-lon1)
    a=math.sin(dlat/2)**2+math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    return r*c
def init_extra_tables():
    conn=connect
    c=conn=conn.cursor()
    c.execute("""CREAT TABLE IF NOT EXISTS clients(id INTEGER PRIMARY KEY AUTOICREMENT,name TEXT,phone TEXT,lat REAL,lon REAL)""")
    c.execute("""CREATE TABLE IF NOT EXIST transports(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,price_per_km REAL)""")
    c.execute("""CREATE TABLE IF NOT EXISTS projects(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT,budget REAL,commission REAL,ts INTEGER)""")
    conn.commit()
    conn.close()
def route_register():
    d=requests.json 
    ok=register(d["username"],d["password"],d["email"])
    return jsonify({"seccess":ok})
def route_login():
    d=requests.json 
    t=login(d["username"],d["password"])
    return jsonify({"token":t})
def add_product():
    u=auth()
    if not requests(requests.headers.get("Authorization"),['admi']) :
        return jsonify({"error":"forbiddenn"}),403
    d=requests.json 
    shop.add_product(d["name"],d["buy"],d["sell"],d["stock"])
    return jsonify({"success":True})
def sell():
    u=auth
    if not u :
        return jsonify({"erro":"auth"}),403
    d=requests.json 
    ok=shop.sell(d["product_id"],d["qty"])
    return jsonify({"success":ok})
    u=auth()
    if  not u:
     return jsonify({"erro":"auth"}),403
    return jsonify({"revenu":shop.total_revenur(),"cost": shop.total_cost(),"profil":shop.total_profit(),"monthly":shop.monthly_profit()})
def add_client():
    u=auth()
    if not u:
        return jsonify({"error":"auth"}),403
    d=requests.json 
    conn=connect()
    c=conn.cursor()
    c.execute("INSERT INTO clients(name,phone,lat,lon) VALUES(?,?,?,?)",(d["name"], d["phone"],d["lat"],d["lon"]))
    conn.commit()
    conn.close()
    return jsonify({"success":True})
def add_transport():
    d=requests.json 
    conn=connect
    c=conn.cursor()
    c.execute("INSERT INTO transports(name,price_per_km)VALUES(?,?)",(d["name"],d["price"]))
    conn.commit()
    conn.close()
    return jsonify({"succes":True})
def cheapest(cid):
    conn=connect
    c=conn.cursor()
    c.execute("SELECT lat,lon FROM clients WHERE id=?",(cid))
    cl=c.fechone()
    base_lat,base_lon=3.848,11.502
    best=None
    c.execute("SELECT name,price_per_km FROM transports")
    for name, price in c.fetchall():
        d=distance(base_lat,base_lon,cl[0],cl[1])
        cost = d*price
        if not best or cost<best[1]:
            best=(name,cost)
            conn.close()
            return jsonify({"best":best})
def supplier():
    d=requests.json 
    conn=connect
    c=conn.cursor()
    c.execute("INSERT INTO suppliers(name,country,contact) VALUES(?,?,?,?)",(d["name"],d["country"],d["contact"]))
    conn.commit()
    conn.close()
    return jsonify({"success":True})
def suppliers():
    conn=connect
    c=conn.cursor()
    c.execute("SELECT*FROM suppliers ORDER BY rating DSC")
    r=c.fetchall()
    conn.close()
    return jsonify(r)
def projet() :
    d=requests.json 
    commission=d["budget"]*0.05
    conn=connect()
    c=conn.cursor()
    c.execute("""INSERT INTO projects(titl,budget,commission,status,ts)VALUE(?,?,?,?,?)""",(d["title"],d["budget"],commission,"open",now()))
    conn.commit()
    conn.close()
    return jsonify({"commission":commission})
def projects():
    conn=connect()
    c=conn.cursor()
    c.execute("SELECT*FROM PROJECTS")
    r=c.fetchall()
    conn.close()
    return jsonify(r)
def payement():
    u=auth()
    if not u:
        return jsonify({"error":"auth"}),403
    d= requests.json 
    amount=d["amount"]
    ref="TX"+str(int(time.time()*1000))
    return jsonify({"status":"accepted","reference":ref,"amount":amount})
def health():
    return jsonify({"status":"ok"})  
if __name__=="_main_":
    app.run(host="0.0.0.0",port=5000)