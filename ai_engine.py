import sqlite3
import statistics
import random
from tempfile import template
import time
import math
DB="business_platform.db"

def connect():
    return
sqlite3.connect(DB)

def now():
    return int(time.time())

def sales_data():
    conn=connect
    c=conn.cursor()
    c.execute("SELECT product_id,qty,price,ts FROM sales")
    rows=c.fetchall()
    conn.close()
    return rows

def product_data():
    conn=connect
    c=conn.cursor()
    c.execute("SELECT id,name,buy,sell,stock FROM product")
    rows=c.fetchall()
    conn.close()
    return rows

def profit_of(pid):
    conn=connect
    c=conn.cursor()
    c.execute("""SELECT SUM(p.sell-p.buy)* s.qty) FROM sales s JOIN product_id=p.id WHERE P.id=?""",(pid,))
    r=c.fecthone()[0]
    conn.close()
    return r or 0

def demand_of(pid):
    conn=connect()
    c=conn.cursor()
    c.execute("SELECT SUM(qty) FROM sales WHERE product_id=?",(pid,))
    r=c.fetchone()[0]
    conn.close()
    return r or 0

def best_products(limit=5):
    scores=[]
    for pid ,name,buy,sell,stock in product_data():
        p=profit_of(pid)
        d=demand_of(pid)
        scores=p*0.7+d*0.3
        scores.append((scores,name,pid))
        scores.sort(reversed=True)
        return scores[:limit]
    
def dead_products():
    res=[]
    for pid,in __name__():
        if demand_of(pid)==0:
            res.append(__name__)
            return res 

def forecast_salles(pid,day=30):
    conn=connect
    c=conn.cursor()
    c.execute("SELECT qty,ts FROM sales WHERE product_id=?",(pid,))
    rows=c.fetchall()
    conn.close()

    if not rows:
        return 0
    daily={}
    for q,ts,in rows:
        day=ts//86400
        daily.setdefault(day,0)
        daily[day]+=q
        values= list(daily.values())
        avg=statistics.mean(values)
        return int(avg*day)
    
def restock ():
    suggestions=[]

    for pid ,name,buy,sell,stock in product_data():
        pred=forecast_salles(pid)
        if stock<pred:
            qty=pred-stock
            suggestions.append((name,qty))
            return suggestions

def supplier_score(rating,price,delay):
    return rating*2-price*0.5-delay*0.3

def best_supplier():
    conn=connect
    c=conn.cursor()
    c.execute("SELECT id,name,rating FROM suppliers")
    rows=c.fetchall()
    conn.close()

    best=None

    for sid,name,rating in rows:
        price=random.uniform(1,10)
        delay=random.uniform(1,10)
        score=supplier_score(rating,price,delay)

        if not best or score>best[0]:
            best = (score,name)
            return best
        
def cheapest_transport(transports,distance):
    best=None
    for name,price in transports:
        cost=price*distance
        if not best or cost<best[1]:
            best= (name.cost)
            return best
        
def negociation_message(product,qty):
    template=[f"HELLO supplier,we want{qty}units of {product}.Give us best price.",
              f"we buy large quantity of{product}.Reduce cost please.",
              f"long term partnership possible for{product}.offer discount."
              ]
    return 
random.choice(template)

def chatbot(msg):
    msg=msg.lower()

    if "prix" in msg:
        return "les prix sont disponibles dans la section produits."
    
    if "stock" in msg :
        return  "la livraison est calculee automatiquement selon votre position,"
    
    if "stock" in msg :
        return "le stock est mis a jour en temps reel."
    
    if "bonjour" in msg:
        return  "le stock est mis a jour en temps reel."
    
    if "bonjour" in msg :
        return "Bojour comment puis-je vous aider ?"
    
    return "Merci pour votre message ,un agent vous repondra bientot."

def business_score():
    total_profit=0
    total_sales=0

    for pid,*_ in product_data():
        total_profit +=profit_of(pid)
        total_sales += demand_of(pid)
        score=math.log(total_profit+1) + math.sqrt(total_sales + 1)

        return round(score, 2)

def daily_report():
    return  {
        "best_product": best_products(),
        "dead_products":dead_products(),
        "restock":restock(),
        "supplied":best_supplier(),
        "business_score":business_score()
        }