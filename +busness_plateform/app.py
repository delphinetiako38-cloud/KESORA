from flask import Flask,render_template,request,redirect,session
import commerce_core as shop
import ai_engine as ai
import secrets 

app=Flask(__name__)
app.secret_key=secrets.token_hex(32)

user={}
product=[]

def stats():
    revenue=sum(p["sell"]) * p["stock"] 
    for p in product ():
        cost=sum(p["buy"]*p["stock"])
        for p in product():
            profit=revenue-cost
        return{"revenue":revenue,"cost":cost,"profit":profit}
    
@app.route("/")
def index():
    return render_template(
  "index.html")
    user=session.get("user"),
    product=product,stats=stats()

@app.post("/register")
def register():
    user[request.form["username"]]= request.form["password"]
    return redirect("/")
@app.post("/login")
def login():
    u=request.form["username"]
    p=request.form["password"]
    if user.get(u)==p:
        session["user"]=u
        return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.post("/add")
def add():
    try:
        product.append({
            "name":
            request.form["name"],
            "buy":
            float(request.form["buy"]),
            "sell":
            float(request.form["sell"]),
            "stock":int(request.form ["stock"])
            })
    except:
        pass
    return redirect("/")

if __name__=="_main_":
    app.run (debug=True,port=8000)