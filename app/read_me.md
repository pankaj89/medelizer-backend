# Libraries
```commandline
pip install fastapi
pip install langchain
pip install pymongo
pip install langchain-ollama
pip install python-multipart
```
# Ollama Server
## Install new model
```
ollama run meditron
```

## Start 
```
ollama run llama3.2 
```

# Fast API Server
## Start 
```
uvicorn main:app --reload  
```
---
# Mongo Db
### Install community
```
 brew install mongodb-community@8.0  
 ```

### Install py mongo for python -> mongodb connectivity
```
 pip install pymongo  
 ```

### Run community
```
brew services start mongodb-community@8.0        
```

### Restart Run community
```
brew services restart mongodb-community@8.0        
```
 
### Stop community
```
brew services stop mongodb-community@8.0
```

### Export single table directly to json
```
mongoexport --db=myDatabase --collection=users --out=/Users/1000060295/Desktop/backup/users.json
```

### Export whole bson (Backup)
```
mongodump --db myDatabase --out /Users/1000060295/Desktop/backup
```

### Mongo sh (Terminal directly run command)
```
mongosh   
STOP : Ctrl + d   
```

### Sample (Python)
```
from pymongo import MongoClient

# Connect to MongoDB (default localhost:27017)
client = MongoClient("mongodb://localhost:27017/")
db = client["myDatabase"]

# Select (or create) a collection
users_collection = db["users"]

# Insert a document
user_data = {
    "name": "Alice",
    "email": "alice1@example.com",
    "age": 28,
    "school": "kv"
}
insert_result = users_collection.insert_one(user_data)
print(f"Inserted user with ID: {insert_result.inserted_id}")

# Find the document we just inserted
found_user = users_collection.find_one({"email": "alice@example.com"})
print("Found user:", found_user['school'])

for user in users_collection.find():
    print(user)
```

### Sample (Mongosh)
```
#use <database name>
use medical

#Find All
db.records.find()

#Delete All
db.records.deleteMany({})

#Update
db.records.updateOne({'task_id':'3785aee6-e45a-4ae3-bbcb-f7ede0a03d45'},{'$set':{'status':'failed'}}) 
```


