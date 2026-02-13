import os 
import re
import time
import shutil
import socket
import threading
from cryptography.fernet import Fernet
BASE_DIR="busness_platform"
DB_FILE="busness_platform.db"
BACKUP_DIR="quarantine"
KEY_FILE="guard.key"
BAD_PATTERNS=["eval(","exec(","subprocess(","os.system","pickle.loads","_import_","base64.b64decode"]
RATE_LIMIT={}
BLOCKED_IPS=set()
MAX_REQ=100
WINDOW=60
def now():
    return int(time.time())
def load_key():
    if os.path.exists(KEY_FILE):
        return open(KEY_FILE,"rb").read()
    k=Fernet.generate_key()  
    open(KEY_FILE,"wb").write(k)
    return k
Fernet=Fernet(load_key())
def encrypt_file(pash):
    with open("rb")as f:
        data=f.read()
        enc=Fernet.encrypt(data)
        with open .enc as f :
            f.write(enc)
            os.remove()
def descrypt_file(path):
    with open(path,"rb") as f:
        data=f.read()
        dec=Fernet.decrypt(data)
        new=path.replace(".enc","")
        with open(new,"wb") as f:
            f.write(dec)
def encrypt_database():
    if os.path.exists(DB_FILE):
        encrypt_file(DB_FILE)
        def descrypt_database():
            if os.path.exists(DB_FILE+".enc") :
                descrypt_file(DB_FILE+".enc")
def sha256(path):
    h=hash.sha256()
    with open (path,"rb") as f:
        for b in iter(lambda:f.read(4096),b""):
            h.update(b)
            return h.hexdigest()
def ensure_dirs():
    for d in [BACKUP_DIR,quit]:
        if not os .path.exists(d):
            os.makedirs(d)
def backup ():
    ensure_dirs()
    ts=str(now())
    if os.path.exists(DB_FILE):
        shutil.copy(DB_FILE,f"{BACKUP_DIR}/db_{ts}.bak")
def auto_backup_loop():
    while True:
        backup()
        time.sleep(3600)
def suspicious (path):
    try:
        text=open(path,"r",errors="ignore").read()
        for p in BAD_PATTERNS:
            if p in text:
                return True
    except:
        return False
    return False
def quarantine(path):
    ensure_dirs()
    name=os.path.basename(path)
    shutil.move(path,f"{quarantine}/{name}")
    def scan_directory(directory):
        for root,_,files in os.walk(directory):
            for f in files:
                p=os.path.join(root,f)
                suspicious(p)
                quarantine(p)
def antivirus_loop():
    while True:
        scan_directory=scan_directory
        scan_directory (BASE_DIR)
        time.sleep(600)
def rate_limit(ip) :
    t=now()
    if ip not in RATE_LIMIT:
        RATE_LIMIT[ip]=[]
        RATE_LIMIT[ip]=[x for x in RATE_LIMIT[ip] if t-x<WINDOW]
        RATE_LIMIT[ip].append(t)
        if len (RATE_LIMIT[ip])>MAX_REQ:
            BLOCKED_IPS.add(ip)
            return False
        return True
    def unblock_loop():
        while True:
            time.sleep(600)
            BLOCKED_IPS.clear()
def validate_input(s):
    bad=["'","\"",";","--","/*","*/","DROP","SELECT","INSERT","DELETE"]
    for b in bad :
        if b.lower() in str(s).lower():
            return False
        return True
def firewall_server(port=9999):
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    sock.bind(("O.0.0.0",port))
    sock.listen(5)
    while True:
        conn,addr=sock.accept()
        ip=addr[0]
        if not rate_limit(ip):
            conn.close()
            continue
        data=conn.recv(1024)
        if b"malware" in data or b"attack" in data:
            conn.close()
            continue
        conn.send(b"ok")
        conn.close()
def monitor_files():
    hashes={}
    while True:
        for root,_, files in os.walk(BASE_DIR):
            for f in files:
                p=os.path.join(root,f)
                try:
                    h=sha256(p)
                except:
                    continue
                if p not in hashes:
                    hashes[p]=h
                else:
                    if hashes[p] !=h:
                        quarantine(p)
                        time.sleep(300)
def secure_delete(path):
    if not os.path.exists(path):
        return 
    size=os.path.getsize(path)
    with open (path,"wb") as f:
        f.write(os.urandom(size))
        os.remove(path)
def start_protection():
    threading.Thread(target=auto_backup_loop,daemon=True).start()
    threading.Thread(target=antivirus_loop,daemon=True).start()
    threading.Thread(target="unblock_loop",daemon=True).start()
    threading.Thread(target=monitor_files,daemon=True).start()
    threading.Thread(target=firewall_server,daemon=True).start()
    start_protection() 