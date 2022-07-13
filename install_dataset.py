import json
import sys
import os
import os.path
import pymongo
import urllib.parse

# Saved Credentials
credentials = {
    "host": "localhost",
    "port": "27017",
    "username": "",
    "password": "",
    "authdb": "admin",
    "database": "",
    "collection": ""
}

# Check Dataset
dataset = input("Enter the name of the dataset to load: ")
if not os.path.isdir(f"data/{dataset}"):
    print(f"{dataset} is not a valid dataset")
    sys.exit()

# Ensure valid credentials
for key in credentials:
    if len(credentials[key]) > 0:
        continue
    print(f"missing key value: {key}")
    while len(credentials[key]) == 0:
        credentials[key] = input(f"Please enter a valid for database credential ({key}): ")

# Connect to Server
client = pymongo.MongoClient("mongodb://{username}:{password}@{host}:{port}/{authdb}".format(
    username=urllib.parse.quote_plus(credentials["username"]), password=urllib.parse.quote_plus(credentials["password"]),
    host=credentials["host"], port=credentials["port"], authdb=credentials["authdb"]
))

# Load Dataset
for item in os.listdir(f"data/{dataset}"):
    if not os.path.isfile(f"data/{dataset}/{item}"):
        continue
    elif item.rfind(".json") == (len(item) - 5):
        # Insert JSON Document
        with open(f"data/{dataset}/{item}", "r") as fs:
            payload = json.loads(fs.read())
            print(f"Inserting Document: {payload['name']}")
            client[credentials["database"]][credentials["collection"]].insert_one(payload)
print("Finished")