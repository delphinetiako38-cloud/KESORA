import os 
import time
import sqlite3
from tokenize import generate_tokens
import bcrypt
import jwt
import fernet
from cryptography.fernet import Fernet 
from datetime import datetime,timedelta
DB="busness_platform.db"
SECRET_KEY=Fernet.generate_key()
CIPHER=Fernet(SECRET_KEY)
JWT_SECRET=os.urandom(32)
JWT_ALGO="HS256"
MAX_ATTEMPTS=5
LOCK_TIME=300
def now():
    return int(time.time())
def connect():
    return sqlite3.connect(DB)
def init_security_tables():
    conn=connect()
    c=conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE,password TEXT,email TEXT,role TEXT,locked_unit INTEGER DEFAUL 0, attenpts INTERGET DEFAULT 0)""")
    c.execute("""CREATE TABLE IF NOT EXISTS logs(id INTEGER PRIMARY KEY AUTOINCREMENT,user TEXT,action TEXT,ts INTEGER)""")
    conn.commit()
    conn.close()
def log (user,action):
    conn=connect()
    c=conn.cursor()
    c.execute("INSERT INTO logs(user,action,ts)VALUES(?,?,?,?)",(user,action,now()))
    conn.commit()
    conn.close()
    def strong_password(p):
        if len(p)<10:
            return False
        if not any (x.isupper()for x in p) :
            return False
        if not any (x.isupper() for x in p):
            return False
        if not any ( x in "!@#$%^&*()"for x in p):
            return False
        return True
    def verify_password(p,h):
        return bcrypt.checkpw(p.encode(),h.encode())
    def encrypt(x):
        return CIPHER.encrypt(x.encode()).decode
    def descrypt(x):
        return CIPHER.descrypt(x.encode()).decode()
    def generate_token(uid,role):
        payload={"uid":uid,"role":role,"exp":datetime.utcnow()+ timedelta(hours=6)}
        return jwt.encode(payload,JWT_SECRET,algorithm=JWT_ALGO)
    def verify_token(token):
        try:
            return jwt.decode(token,JWT_SECRET,algorithms=[JWT_ALGO])
        except:
            return None
        def register(username,password,email,role="user"):
            if not strong_password(password):
                return False
            h=hash_password(password)
            e=encrypt(email)
            conn=connect()
            c=conn.cursor()
            try:
                c.execute("INSERT INTO users(username,password,email,role)VALUES(?,?,?,?)",(username,h,e,role))
                conn.commit()
                log(username,"registrer")
                return True
            except:
                return False
            finally:
                conn.close()
    def lock_account(username):
        conn=connect
        c=conn.cursor()
        c.execute("UPDATE users SET locked_until=?,attemps=0 WHERE username=?",(now()+LOCK_TIME,username))
        conn.commit()
        conn.close()
def add_attempt(username):
    conn=connect()
    c=conn.cursor()
    c.execute("SELECT attempts FROM users WHERE username=?",(username,))
    a=c.fetchone()[0]
    conn.close()
    if a>=MAX_ATTEMPTS: 
      LOCK_TIME(username)
    def reset_attempts(username):
        conn=connect()
        c=conn.cursor()
        c.execute("UPDATE users SET attempts=0 WHERE username=?",(username,))
        conn.close()
        def login(username,password):
            conn=connect()
            c=conn.cursor()
            c.execute("SECT id, password,email,role,locke d_until FROM users WHERE username=?",(username,))
            r=c.fetchone()
            if not r:
                conn.close()
                return None
            uid,h,email,role,locked=r
            if locked>now():
                conn.close()
                return None 
            if  (password,h):
                reset_attempts(username)
                log(username,"login")
                token=generate_tokens(uid,role)
                conn.close()
                return token
            else:
                add_attempt(username)
                log(username,"bad_logein")
                conn.close()
                return None
def get_user(uid):
    conn=connect()
    c=conn.cursor()
    c.execute("SELECT username,email,role FROM users WHERE id=?",(uid,))
    r=c.fetchone()
    conn.close()
    if not r:
        return None
    u,e,role=r
    return u,(e),role
def change_password(uid,newp):
    if not (newp):
        return False
    conn=connect()
    c=conn.cursor()
    c.execute("UPDATE users SET password=? WHERE id=?",((newp),uid))
    conn.commit()
    conn.close()
    return True
def require_role(token,allowed):
    data=token(token)
    if not data:
        return False
    return data ["role"] in allowed
def list_logs():
    conn=connect()
    c=conn.cursor()
    c.execute("SELET user,action,ts FROM logs ORDER BY ts DESC")
    rows=c.fetchall()
    conn.close()
    return rows
def delete_user(uid):
    conn=connect()
    c=conn.cursor()
    c.execute("DELETE FROM users WHERE id=?",(uid,))
    conn.commit()
    conn.close()
def all_users():
    conn=connect()
    c=conn.cursor()
    c.execute("SELECT id,username,role FROM users")
    rows=c.fetchall()
    conn.close()
    return rows
