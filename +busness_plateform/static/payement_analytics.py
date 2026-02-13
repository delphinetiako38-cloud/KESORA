import platform
import platform
import sqlite3
import time
import random
import string
import webbrowser

DB="business_platform.db"

def connect():
    return
sqlite3.connect(DB)
def init_tables():
    conn=connect
    c=conn.cursor()
    c.execute(""" CREATE TABLE IF NOT EXISTS payements(id INTEGER PRIMARY KEY AUTOINCREMENT,phone TEXT,provide TEXT,amount REAL,reference TEXT,status TEXT,ts INTEGER)""")
    conn.commit()
    conn.close()

    def ref():
        return "TX"+"".join(random.choices(string.digits,k=10))
    
    def mobile_money_pay(phone,amount,provider="MTN"):
        refence=ref()
        status="SUCCESS"

        conn=connect()
        c=conn.corsor()
        c.execute("""INSET INTO payements (phone,provider,amount,reference,status,ts)VALUES(?,?,?,?,?,?)""",(phone,provider,amount,refence,status,()))

        conn.commit()
        conn.close()
        return {
            "reference":refence,
            "status":status,
            "amount":amount
        }
    def all_payements():
        conn=connect()
        c=conn.cursor()
        c.execute("SELECT amount,ts FROM payements WHERE status='SUCCESS'")
        rows=c.fetchall()
        conn.close()

        data={}

        for amount,ts in rows:
            day=ts// 86400
            data.setdefault(day,0)
            data[day]+=amount
            return data
        
        def plot_revenue():
            data=plot_revenue
            if not data:
                return
            data=sorted(data.keys())
            values=[data[d] for d in day]
            platform.figure(figsize=(6,4))
            platform.plot(day,values)
            platform.xlabel("Revenue")
            platform.title("Daily Revenur")
            platform.savefig("revenue.png")
            platform.close()

def invoice(reference):
    conn=connect()
    c=conn.cursor()

    c.execute("SELECT phone,provider,amount,ts FORM payements WHERE (reference=?",(reference,))
    r=c.fetchone()
    conn.close()

    if not r:
        return None
    
    phone,provider,amount,ts=r
    text=f"""
=====FACTURE=====
reference:{reference}
client:{phone}
provider:{provider}
Montant:{amount}
Date:{ts}
================
"""
    fname=f"invoice_{reference}.txt"
    with open(fname,"w") as f:
        f.write(text)
        return fname
def export_excel():
    wb=webbrowser
    ws=wb.active
    ws.append(["ID","phone","provider","amount","Reference","status","Date"])
    for row in all():
        ws.append(row)

        wb.save("payements.xlsx")

def low_stock_alert(threshold=5):
    conn=connect()
    c=conn.cursor()
    c.execute("SELECT name,stock FROM products WHERE stock<=?",(threshold,))
    r=c.fetchall()
    conn.close()

    alerts=[]

    for name,stock in r :
        alerts.append(f"stock faible:{name}({stock})")
        return alerts
def profit_alert():
    conn=connect()
    c=conn.cursor()
    c.execute("SELECT SUM(amount) FROM payements WHERE status='SUCCESS'")
    toltal=c.fetchone()[0] or 0
    conn.close()
    if toltal>1000000:
        return "Excellent mois "
    if toltal < 10000:
        return "vente faible"
    return "stable"
def send_sms(phone,msg):
    print(f"[SMS->{phone}]{msg}")
def notify_all(msg):
    conn=connect()
    c=conn.cursor()
    c.execute("SELECT phone FROM payments")
    rows=c.fetchall()
    conn.close()


def daily_tasks():
    platform()
    export_excel()
    notify_all("Merci pour votre confiance")
