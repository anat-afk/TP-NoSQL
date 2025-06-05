# api.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["stockx"]
ventes = db["ventes"]

@app.route("/total-ventes")
def total_ventes():
    total = ventes.count_documents({})
    return jsonify({"total": total})

@app.route("/marques")
def marques():
    brands = ventes.distinct("Brand")
    return jsonify({"marques": brands})

@app.route("/regions")
def regions():
    regions = ventes.distinct("Buyer Region")
    return jsonify({"regions": regions})

@app.route("/echantillon")
def echantillon():
    docs = ventes.find({}, {
        "_id": 0, "Sneaker Name": 1, "Brand": 1, "Sale Price": 1,
        "Shoe Size": 1, "Buyer Region": 1, "releasedate": 1
    }).limit(5)
    return jsonify(list(docs))

@app.route("/ventes-par-marque")
def ventes_par_marque():
    pipeline = [{"$group": {"_id": "$Brand", "total": {"$sum": 1}}}, {"$sort": {"total": -1}}]
    results = list(ventes.aggregate(pipeline))
    return jsonify(results)

@app.route("/ventes-par-mois")
def ventes_par_mois():
    pipeline = [
        {"$group": {"_id": {"$substr": ["$orderdate", 0, 7]}, "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}, {"$limit": 12}
    ]
    results = list(ventes.aggregate(pipeline))
    return jsonify(results)

@app.route("/marques-par-region")
def marques_par_region():
    pipeline = [
        {"$group": {"_id": {"region": "$Buyer Region", "brand": "$Brand"}, "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}, {"$limit": 20}
    ]
    results = list(ventes.aggregate(pipeline))
    return jsonify(results)

@app.route("/top-modeles")
def top_modeles():
    pipeline = [
        {"$group": {"_id": "$Sneaker Name", "total": {"$sum": 1}}},
        {"$sort": {"total": -1}}, {"$limit": 10}
    ]
    results = list(ventes.aggregate(pipeline))
    return jsonify(results)

@app.route("/ventes-par-region")
def ventes_par_region():
    pipeline = [{"$group": {"_id": "$Buyer Region", "total": {"$sum": 1}}}, {"$sort": {"total": -1}}]
    results = list(ventes.aggregate(pipeline))
    return jsonify(results)

@app.route("/taille-chaussures")
def taille_chaussures():
    pipeline = [{"$group": {"_id": "$Shoe Size", "total": {"$sum": 1}}}, {"$sort": {"_id": 1}}]
    results = list(ventes.aggregate(pipeline))
    return jsonify(results)

@app.route("/evolution-temporelle")
def evolution_temporelle():
    pipeline = [
        {"$group": {
            "_id": {"$substr": ["$orderdate", 0, 7]},
            "ventes": {"$sum": 1},
            "prix_moyen": {"$avg": "$Sale Price"}
        }},
        {"$sort": {"_id": 1}}
    ]
    results = list(ventes.aggregate(pipeline))
    return jsonify(results)

@app.route("/dates-de-sortie")
def dates_de_sortie():
    results = list(ventes.find({}, {
        "_id": 0,
        "Sneaker Name": 1,
        "releasedate": 1
    }))
    return jsonify(results)

@app.route("/explorer-par-marque")
def explorer_par_marque():
    marque = request.args.get("marque")
    if not marque:
        return jsonify([])

    docs = ventes.find({"Brand": marque}, {
        "_id": 0, "Sneaker Name": 1, "Sale Price": 1
    })
    return jsonify(list(docs))

if __name__ == "__main__":
    app.run(debug=True)
