from pymongo import MongoClient

try:
    # Replace 'mydatabase' with your actual database name
    client = MongoClient('mongodb+srv://rohit:Rohit2004@cluster0.oxj1e.mongodb.net/movies?retryWrites=true&w=majority')
    print("Connected to MongoDB")
    client.close()
except Exception as e:
    print("Error connecting to MongoDB:", e)