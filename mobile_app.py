import tkinter as tk
import requests
import json

API="http://192.168.45.223"

class BsinessApp:
    def __init__(self,root):
        self.root=root
        self.root.title("Business app")
        self.root.title("400x300")

        self.username_label=tk.Label(root,text="Username")
        self.username_label.pack()
        self.username_entry=tk.Entry(root)
        self.username_entry.pack()

        self.pasword_label=tk.Label(root,text="password")
        self.pasword_label.pack()
        self.pasword_entry=tk.Entry(root,show="*")
        self.pasword_entry.pack()

        self.login_button=tk.Button(root,text="login",
                                    command=self.login)
        self.login_button.pack(pady=5)
        self.products_button=tk.Button(root,text="voir produits",
                                       command=self.products)
        self.products_button.pack(pady=5)

        self.status=tk.Label(root,text="status...")
        self.status.pack(pady=10)
        def login(self):
            username=self.username_entry.get()
            password=self.password_entry.get()
            data={"username":username,"password":password}
            try:
                response=requests.post(f"{API}/login",json=data)
                if response.status_code==200:
                    self.status.config(text="connecte !")
                else:
                    self.status.config(text="Erreur login")
            except Exception as e :
                self.status.config(text=f"Erreur:{e}")
                def products(self):
                    try:
                        response=requests.get(f"{API}/product")
                        if response.status_code==200:
                            self.status.config(text=str(response.json()))
                        else:
                            self.status.config(text="Erreur recuperation produits")
                    except Exception as e:
                        self.status.config(text="Erreur:{e}")
                        if __name__=="_main_":
                            root=tk.Tk()
                            app=BsinessApp(root)
                            root.mainloop()