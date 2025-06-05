from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # Autorise les requêtes depuis Streamlit

client = MongoClient("mongodb://localhost:27017/")
db = client["stockx"]
ventes = db["ventes"]

@app.route("/ventes/total")
def total_ventes():
    total = ventes.count_documents({})
    return jsonify({"total": total})

@app.route("/ventes/marques")
def marques():
    pipeline = [{"$group": {"_id": "$Brand", "total": {"$sum": 1}}}, {"$sort": {"total": -1}}]
    data = list(ventes.aggregate(pipeline))
    return jsonify(data)

@app.route("/ventes/mois")
def ventes_par_mois():
    pipeline = [
        {"$group": {"_id": {"$substr": ["$orderdate", 0, 7]}, "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}, 
        {"$limit": 12}
    ]
    data = list(ventes.aggregate(pipeline))
    return jsonify(data)

@app.route("/ventes/evolution")
def evolution():
    pipeline = [
        {"$group": {
            "_id": {"$substr": ["$orderdate", 0, 7]},
            "ventes": {"$sum": 1},
            "prix_moyen": {"$avg": "$Sale Price"}
        }},
        {"$sort": {"_id": 1}}
    ]
    data = list(ventes.aggregate(pipeline))
    return jsonify(data)

@app.route("/ventes/sample")
def sample():
    docs = list(ventes.find({}, {
        "_id": 0,
        "Sneaker Name": 1,
        "Brand": 1,
        "Sale Price": 1,
        "Shoe Size": 1,
        "Buyer Region": 1,
        "releasedate": 1
    }).limit(5))
    return jsonify(docs)

if __name__ == "__main__":
    app.run(debug=True)
