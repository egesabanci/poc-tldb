from flask import Flask, request

from src.tldb.tldb import TLDB

api: Flask = Flask(__name__)
database = TLDB(wal_capacity = 100, memtable_capacity= 150)

@api.route("/", methods = ["POST"])
def handle():
  query = request.get_json()["query"]
  res = database.query(query)

  return {"response": res} 

if __name__ == "__main__":
  api.run(host = "0.0.0.0", port = 5199)