from python:3.12-slim
WORKDIR/app
#copier tous les fichiers
COPY . .
# Installer dependances
RUN pip Install
--no-cache-dir flask bcrypt
cryptography pyjwt
matplotlib openpyxl
#exposer le port du serveur web
EXPOSE 8000
# Lancer l'application
CMD ["python","web_app.py"]