from flask import Flask, request, jsonify
import json

app = Flask(__name__)


@app.route("/msg", methods=["GET"])
def get_msg():
    msg = request.args.get("msg")
    with open("msg.json", "at") as pf:
        mload = json.load(pf)
    mid = mload.get(msg)
    return jsonify({"msg_id": mid})


@app.route("/tables", methods=["GET"])
def get_tables():
    table = request.args.get("table")
    with open("tables.json", "at") as tf:
        tload = json.load(tf)
    tid = tload.get(table)
    return jsonify({"table_id": tid})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Run on all interfaces, port 5000
