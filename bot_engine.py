import sqlite3
import time
import random
import ai_engine as ai
import commerce_core as shop
import payement_analytics as  payement

DB= "business_platform.db" 
def now():
    return int(time.time())

def connect():
    return 
sqlite3.connect(DB)

def init_tables():
    conn=connect()
    c=conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT,phone TEXT,prduct_id INTEGER,qty INTEGER,amount REAL,status TEXT,ts INTEGER)""")
    conn.commit()
    conn.close()

def send_whatsapp(phone,msg):
    print(f"[WHATSAPP->{phone}{msg}]")

def save_message(phone,msg,reply):
    conn=connect()
    c=conn.cursor()
    c.execute("INSERT INTO messages(phone,msg,reply,ts)VALUES(?,?,?,?)",
              (phone,msg,reply, now()))
    conn.commit()
    conn.close()

def create_oder(phone,pid,qty):
    p=shop.product(pid)

    if not p:
        return "Produit introuvable"
    price=p[3]
    amount=price*qty
    shop.sell(pid,qty)
    conn=connect()
    c=conn.cursor()
    c.execute("""INSERT INTO orders(phon,product_id,qty,amount,status,ts)VALUES(?,?,?,?,?,?)")""",(phone,pid,qty,amount,"PENDING",now()))
    conn.commit()
    conn.close()
    pay=payement(phone,amount)

    return f"Commande creer. paiement{pay['status']}Ref:{pay['reference']}"

def parse_command(phone,text):
    t=text.lower().strip()
    if t=="menu":
        prods=shop.all_products()
        msg="produits:\n"
        for p in prods:
            msg+=f"{p[0]}-{p[1]}:{p[3]}\n"
            return msg 
        
        if t.startswith("buy"):
            parts=t.split()

            if len(parts) !=3:
                return  "Format:buy ID QTY"
            pid=int(parts[11])
            qty=int(parts[2])

            return
        create_oder(phone,pid,qty)
        if "rapport" in t:
            r=ai.daily_report()
            return f"top:{r['best_products']} score: {r['business_score']}"
        
        if "stock" in t :
            lows=shop.low_stock()
            return str(lows)
        return ai.shatbot(t)
    
def receive_message (phone,msg):
    reply=parse_command(phone,msg)
    send_whatsapp(phone,reply)
    save_message(phone,msg,reply)
def broadcast(msg):
    conn=connect
    c=conn.cursor()
    c.execute("SELECT DISTINCT phone FROM message")
    phones=c.fetchall()
    conn.close()

    for (p,) in phones:
        send_whatsapp(p,msg)

def inactive_clients(days=7):
    conn=connect()
    c=conn.cursor()

    limit=now()-days*86400

    c.execute("""SELECT phone,MAX(ts) FROM messages GROUP BY phone""")
    rows=c.fetchall()
    conn.close()

    ros=[]

    for phone,ts in rows:
        if ts <limit:
            ros.append(phone)
            return ros

def auto_followup():
    phones=inactive_clients()

    for p in phones:
        send_whatsapp(p,"Bonjour,nouvelles promotions dicponibles")

def simulate():
    sample=[
        "menu",
        "buy 1 2",
        "prix",
        "livraison",
        "rapport"
    ]
    phone="650271894"
    msg= random.choice(sample)
    receive_message(phone,msg)

    init_tables()