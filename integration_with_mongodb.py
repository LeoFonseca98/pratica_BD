import pymongo as pyM
import pprint
import os
from dotenv import load_dotenv

load_dotenv()

mongo_user = os.getenv("MONGO_USER")
mongo_password = os.getenv("MONGO_PASSWORD")

client = pyM.MongoClient(f"mongodb+srv://{mongo_user}:{mongo_password}@cluster0.btpzb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")


db = client.finance
collection = db.finance_collection
print(db.finance_collection)

bank = [{
    "nome": "Mariana Alves Souza",
    "email": "mariana.souza@email.com",
    "tipo_conta": "Corrente"
},
{
    "nome": "Carlos Eduardo Lima",
    "email": "carlos.lima@email.com",
    "tipo_conta": "Poupança"
},
{
    "nome": "Leonardo Moreira Fonseca",
    "email": "leonardo.fonseca@email.com",
    "tipo_conta": "Poupança"
}]

banks = db.banks
result = banks.insert_many(bank)
print(result.inserted_ids)

pprint.pprint(db.banks.find_one({"nome": "Leonardo Moreira Fonseca"}))