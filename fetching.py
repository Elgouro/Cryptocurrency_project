import pyodbc as odbc
import requests
import pandas as pd
import sqlalchemy
import os
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Récupérer les informations de connexion à partir des variables d'environnement
servername = os.getenv('DB_SERVER')
database = os.getenv('DB_DATABASE')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
try:
    #conn = odbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+servername+';DATABASE='+database+';UID='+username+';PWD='+password)
    
    # Connexion à la base de données avec SQLAlchemy
    engine = sqlalchemy.create_engine(f'mssql+pyodbc://{username}:{password}@{servername}/{database}?driver=ODBC+Driver+17+for+SQL+Server')
    print('connected successfully')
except Exception as e:
    print('veuillez revoir vos information de connection ',e)

# Chargement des données depuis l'API et intégration dans la base de données
url = "http://api.coincap.io/v2/assets"
header = {"Content-Type": "application/json", "Accept-Encoding":"deflate"}

response = requests.get(url, headers=header)
responseData = response.json()
df = pd.json_normalize(responseData, 'data')

try:
    # Charger les données dans la table 'cryptotable'
    df.to_sql(name="cryptotable", con=engine, index=False, if_exists="replace")
    print("Vos données ont bien été intégrées à la base de données")
except Exception as e:
    print('Erreur lors du chargement des données dans la base de données:', e)