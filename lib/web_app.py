import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY=os.getenv("SECREY_KEY")
JWT_SECRET=os.getenv("JWT_SECRET")
LANGUAGES={
    "fr":{"logout":
          "Connexion","logout":
          "Deconnexion"},
          "en":
          {"login":"Login",
           "logout":"Logout"},
           "es":{"login":"Iniciar session","logout":"Cerrar session"}
           }
CURRENCIES={
    "XAF":1,
    "USD":0.0017,
    "EUR":0.0015
}
def translet(key,
             lang="fr"):
    return
lang="fr"
LANGUAGES.get(lang,
              LANGUAGES["fr"]).get 
USD_RATE=float(os.getenv("USD_RATE",600))
EUR_RATE=float(os.getenv("EUR_RATE",655))

def convert_fcfa_to_usd(amount):
    return amount / USD_RATE
def convert_fcfa_to_eur(amount):
    return amount/EUR_RATE
if __name__=="_main_":
    fcfa=120000
    print(f"{fcfa} FCFA={convert_fcfa_to_usd(fcfa):2f}USD")
    print(f"{fcfa} FCFA={convert_fcfa_to_eur(fcfa):2f}EUR")