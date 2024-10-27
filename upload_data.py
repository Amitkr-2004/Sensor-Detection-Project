from pymongo.mongo_client import MongoClient
import pandas as pd
import json

#mongo url
uri="mongodb+srv://AmitKr:12345@cluster0.bd42a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" 

#create a new client and connect it to server
client=MongoClient(uri)

#create database name and collection name
DATABASE_NAME="Detector"
COLLECTION_NAME="sensor_detector"

df=pd.read_csv("D:\Coding\ML Projects\Sensor Detection\notebooks\wafer_23012020_041211.csv")

df = df.drop("Unnamed: 0",axis=1)

json_record = list(json.loads(df.T.to_json()).values()) #converting data into list of json format

client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)