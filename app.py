from flask import Flask, jsonify, request

from HelperRules import HelperGetRules

import pandas

app = Flask(__name__)

@app.route("/", methods=["GET"])
def MainRoute():
  """
  Main Route
  """
  return jsonify({"message":"Year Application !"})

@app.route("/GetRules", methods=["POST"])
def GetFinalRules():
  """
  Set Min. Support & Set Min. Confi

  >>> {"support" : 0.05, "confidence" : 0.3}
  """
  params = request.json
  support = float(params.get("support", 0.05))
  confi = float(params.get("confidence", 0.3))
  result = HelperGetRules(support, confi)
  return jsonify(result)

if __name__ == '__main__':
  # Application Runner
  debug = False
  port = "5000"
  host = "127.0.0.1"
  app.run(debug=debug, host=host, port=port)
