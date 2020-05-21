import pymongo

def insert_lead(payload):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["properties"]
    mycol = mydb["ListingDetails"]
    try:
        mycol.insert_one(payload)
    except Exception as e:
        print("A duplicate has been detected", e)
