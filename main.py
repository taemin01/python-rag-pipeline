import module.chromadb_connection as chromadb_connection

collection = chromadb_connection.load_collction()
print(collection.get())