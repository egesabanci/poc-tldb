from flask import Flask, request

api: Flask = Flask(__name__)

@api.route("/", methods = ["POST"])
def handle():
  query = request.get_json()["query"]
  pass

if __name__ == "__main__":
  api.run(host = "localhost", port = 5199)