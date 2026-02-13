import sqlite3
import time
DB="busness_platform.db"
def now():
    return int(time.time())
def connect():
    return
sqlite3.connect(DB)
def init_tables():
    conn=connect()
    c=conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,buy REAL,sell REAL,stock INTEGER,created INTEGER)""")
    c.execute("""CREATE TABLE IF NOT EXISTS sales(id INTERGER PRIMARY KEY AUTOINCREMENT,product_id INTEGER,qty INTEGER,price REAL,ts INTEGER)""")
    c.execute("""CREATE TABLE IF NOT EXISTS purchases(id INTEGER PRIMARY KEY AUTOINCREMENT,product_id INTEGER, cost REAL,ts INTEGER)""")
    conn.commit()
    conn.close()
def add_product(name,buy,sell,stock,min_stock=5):
    conn=connect()
    c=conn.cursor()
    c.execute("INSERT INTO products(name,buy,sell,stock,min_stock,created)VALUES(?,?,?,?,?,?)"(name,buy,sell,stock,min_stock,now()))
    conn.commit()
    conn.close()
def update_price(pid,buy=None,sell=None):
    conn=connect()
    c=conn.cursor()
    if buy is not None:
        c.execute("UPDATE products SET buy=? WHERE id=?",(buy,pid))
    if sell is not None:
        c.execute("UPDATE products SET sell=? WHERE id=?",(sell,pid))
        conn.commit()
        conn.close()
    def restock (pid,qty,cost=None):
        conn=connect()
        c=conn.cursor()
        c.execute("UPDATE products SET stock=stock + ? WHERE id=?",(qty,pid))
        if cost:
            c.execute("INSERT INTO purchases(product_id,qty,cost,ts)VALUES(?,?,?,?)",(pid,qty,cost,now()))
            conn.commit()
            conn.close()
    def sell(pid,qty):
        conn=connect()
        conn=conn.cursor()
        c.execute("SELECT stock,sell FROM products WHERE id=?",(pid,))
        r=c.fetchone()
        if not r:
            conn.close()
            return False
        stock,price=r
        if stock<qty:
            conn.close()
            return False
        c.execute("UPDATE products SET stock=stock-?WHERE id=?",(qty,pid))
        c.execute("INSERT INTO sales(product_id,qty,price,ts)VALUES(?,?,?,?)",(pid,qty,price,now()))
        conn.commit()
        conn.close()
        return True
    def delete_product(pid):
        conn=connect()
        c=conn.cursor()
        c.execute("DELETE FROM products WHERE id=?",(pid,))
        conn.commit()
        conn.close()
    def product (pid):
        conn=connect
        c=conn.cursor()
        c.execute("SELECT*FROM products WHERE id=?",(pid,))
        r=c.fetchone()
        conn.close()
        return r
    def all_products():
        conn=connect()
        c=conn.cursor()
        c.execute("SELECT id,name,buy,sell,stock FROM products")
        rows=c.fetchall()
        conn.close()
        return rows
    def low_stock():
        conn=connect()
        c=conn.cursor()
        c.execute("SELECT id,name,stock,min_stock FROM  products WHERE stock<=min_stock")
        rows=c.fetchall()
        conn.close()
        return rows
    def total_revenue():
        conn=connect()
        c.conn.cursor()
        c.execute("SELECT SUM(price*qty)FROM sales")
        r=c.fetchone()[0]
        conn.close()
        return r or 0
    def total_cost():
        conn=connect()
        c=conn.cursor()
        c.execute("""SELECT SUM(p.buy*s.qty)FROM SALES s JOIUN products p ON s.product_id=p.id""")
        r=c.fetchone()[0]
        conn.close()
        return r or 0
    def total_profit():
        return total_revenue()-total_cost()
    def revenue_between(start,end):
        conn=connect()
        c=conn.cursor()
        c.execute("""SELECT SUM(price*qty)FROM sales WHERE ts BETWEEN ? AND ? """,(start,end))
        r=c.fetchone()[0]
        conn.close()
        return r or 0
    def cost_between(start,end):
        conn=connect()
        c=conn.curso()
        c.execute("""SELECT SUM(p.buy*s.qty)FROM sales s JOIN products p ON s.product_id=p.id WHERE s.ts BETWEEN? AND?""",(start,end))
        r=c.fetchone()[0]
        conn.close()
        return r or 0
    def profit_between(start,end):
        return revenue_between(start,end )-cost_between(start,end)
    def monthy_profit():
        month=30*86400
        return profit_between(now()-month,now())
    def best_sellers(limit=5):
        conn=connect()
        c=conn.curso()
        c.execute("""SELECT p.name,SUM(s.qty)as total FROM sales s JOIN PRODUCTS p ON p.id=s.product_id GROUP BY s.product_id ORDER BY total DESC LIMIT?""",(limit,))
        rows=c.fetchall()
        conn.close()
        return rows
    def worst_sellers (limit=5):
        conn.connect()
        c=conn.cursor()
        c.execute("""SELECT p.name,SUM(s.qty) as total FROM sales s JOIN products p.ON p.id=s.product_id GROUP BY s.product_id ORDER BY total ASC LIMIT ?""",(limit,))
        rows=c.fetchall()
        conn.close()
        return rows
    def inventory_value():
        conn=connect()
        c=conn.cursor()
        c.execute("SELECT SUM(stock*buy)FROM products")
        r=c.fetchone()[0]
        conn.close()
        return r or 0
    def product_profit(pid):
        conn=connect()
        c=conn.cursor()
        c.execute("""SELECT SUM(p.sell-p.buy)*s.qty)FROM sales s JOIN products p ON p.id=s.product_id WHERE p.id=?""",(pid,))
        r=c.fetchone()[0]
        conn.close()
        return r or 0
    def seach(name):
        conn=connect()
        c=conn.cursor()
        c.execute("SELECT*FROM products WHERE name LIKE ?",(f"%{name}%",))
        rows=c.fetchall()
        conn.close()
        return rows
    def sales_history(pid):
        conn=connect()
        c=conn.cursor()
        c.execute("SELECT qty,price,ts FROM sales WHERE product_id=?",(pid,))
        rows=c.fetchall()
        conn.close()
        return rows
    
    def init_master_account():
        conn=connect()
        c=conn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS master_account(id INTEGER PRIMARY KEY,balance REAL DEFAUT 0)""")
        c.execute("SELECT*FROM master_account WHERE id=1")
        if not c.fetchone():
            c.execute("INSERT INTO master_account(id,balance) VALUES(1,0)")
            conn.commit()
            conn.close()