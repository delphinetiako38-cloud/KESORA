import sqlite3
import time
import random

DB="business_platform.db"

COMMISSION_RATE=0.03

def now ():
    return int(time.time())

def connect():
    return 
sqlite3.connect(DB)

def init_tables():
    conn=connect()
    c=conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXIST vendors(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,phone TEXT,wallet REAL DEFAULT 0 , 
              created INTEGER)""")
    c.execute("""CREATE TABLE IF NOT EXISTS vendor_products(id INTEGER PRIMARY KEY AUTOINCREMENT,vendor_id INTEGER,name TEXT,price REAL,stock INTEGER)"""
              )
    c.execut("""CREATE TABLE IF NOT EXISTS vendor_sales(id INTEGER PRIMARY KEY AUTOINCREMENT,
             vendor_id INTEGER,
             product_id INTEGER,
             qty INTEGER,
             total REAL,
             ts INTEGER)""")
    c.execute("""CREATE TABLE IF NOT EXISTS withdrawals(id INTEGER PRIMARY KEY AUTOINCREMENT,
              vendor_id INTEGER,
              amount REAL,
              ts INTEGER)"""
              )
    conn.commit()
    conn.close()

def create_vendor(name,phone):
    conn=connect
    c=conn.cursor()
    c.execute("""INSERT INTO vendors(name,phone,created)VALUES(?,?,?)""",(name,phone,now()))
    conn.commit()
    conn.close()

def vendor(pid):
    conn=connect()
    c=conn.cursor()
    c.execute("SELECT * FROM vendors WHERE id=?",(pid,))
    r=c.fecthone()
    conn.close()
    return r

def all_vendors(vendor_id,name,price,stock):
    conn=connect()
    c=conn.cursor()
    c.execute("""INSERT INTO vendor_products(vendor_id,name,price,stock)
              VALUES(?,?,?,?)""",
              (vendor_id,name,price,stock))
    conn.commit()
    conn.close()

def vendor_products(vendor_id):
    conn=connect()
    c=conn.cursor()
    c.excute("SELECT*FROM vendor_products WHERE vendor_id=?",(vendor_id,))
    r=c.fetchall()
    conn.close()
    return r

def sell_vendor_product(product_id,qty):
    conn=connect()
    c=conn.cursor()

    c.execute("""SELECT vendor_id,price,stock FROM vendor_products WHERE id=?""",(product_id,))

    r=c.fetchone()

    if not r:
        conn.close()
        return False
    vendor_id,price,stock=r

    if stock<qty:
        conn.close()
        return False
    total=price*qty
    commission=total*COMMISSION_RATE
    vendor_gain=total-commission

    c.execute("""UPDATE vendor_products SET stock=stock- WHERE id=?""",(qty,product_id))
    c.execute("""INSERT INTO vendor_sales(vendor_id,product_id,qty,total,commission,ts)VALUES(?,?,?,?,?,?)""",(vendor_id,product_id,qty,total,commission,now()))
    c.execute("""UPDATE vendors SET wallet=wallet+? WHERE id=?""",(vendor_gain,vendor_id))
    conn.commit()
    conn.close()
    return True

def vendor_wallet(vendor_id):
    conn=connect()
    c=conn.cursor()
    c.execute("SELECT wallet FROM vendors WHERE id=?",(vendor_id,))
    r=c.fetchonne()
    conn.close()
    return r[0] if r else 0

def withdraw(vendor_id,amount):
    balance=vendor_wallet(vendor_id)
    if amount>balance:
        return False
    conn=connect()
    c=conn.cursor()
    c.execute("UPDATE vendors SET wallet=wallet-? WHERE id=?",(amount,vendor_id))
    c.execute("""INSERT INTO withdrawals(vendor_id,amount,ts)VALUES(?,?,?)""",(vendor_id,amount,now()))
    conn.commit()
    conn.close()

    return True

def vendor_sales_history(vendor_id):
    conn=connect()
    c=conn.cursor()
    c.execute("""SELECT qty,total,commission,ts FROM vendor_sales WHERE vendor_id=?""",(vendor_id))
    r=c.fetchall()
    conn.close()
    return r

def top_vendors(limit=5):
    conn=connect
    c=conn.cursor()
    c.execute("""SELECT name,wallet FROM vendors ORDER BY wallet DESC LIMIT?""",(limit,))
    r=c.fetchall()
    conn.close()
    return r 
def sell_vendor_product(product_id,qty):
    conn=connect()
    c=conn.cursor()
    
    vendor_gain="total-commission"
    if not "debit_master(total)":
        conn.close()
        return False
    c.execute("UPDATE vendors SET wallet=wallet+ ? WHERE id=?",(vendor_gain,"vendor_id"))
    conn.commit()
    conn.close()
    init_tables()