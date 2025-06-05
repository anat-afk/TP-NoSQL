from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

# Initialisation
app = Flask(__name__)
CORS(app)

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["stockx"]
ventes = db["ventes"]

@app.route("/total-ventes")
def total_ventes():
    total = ventes.count_documents({})
    return jsonify({"total": total})

@app.route("/marques")
def marques():
    marques = ventes.distinct("Brand")
    return jsonify(marques)

@app.route("/regions")
def regions():
    regions = ventes.distinct("Buyer Region")
    return jsonify(regions)

@app.route("/echantillon")
def echantillon():
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

@app.route("/ventes-par-marque")
def ventes_par_marque():
    pipeline = [{"$group": {"_id": "$Brand", "total": {"$sum": 1}}}, {"$sort": {"total": -1}}]
    results = list(ventes.aggregate(pipeline))
    return jsonify([{"Marque": r["_id"], "Ventes": r["total"]} for r in results])

@app.route("/ventes-par-mois")
def ventes_par_mois():
    pipeline = [
        {"$group": {"_id": {"$substr": ["$orderdate", 0, 7]}, "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}, {"$limit": 12}
    ]
    results = list(ventes.aggregate(pipeline))
    return jsonify([{"Mois": r["_id"], "Ventes": r["count"]} for r in results])

@app.route("/marques-par-region")
def marques_par_region():
    pipeline = [
        {"$group": {"_id": {"region": "$Buyer Region", "brand": "$Brand"}, "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}, {"$limit": 20}
    ]
    results = list(ventes.aggregate(pipeline))
    return jsonify([
        {"Région": r["_id"]["region"], "Marque": r["_id"]["brand"], "Ventes": r["count"]}
        for r in results
    ])

@app.route("/top-modeles")
def top_modeles():
    pipeline = [
        {"$group": {"_id": "$Sneaker Name", "total": {"$sum": 1}}},
        {"$sort": {"total": -1}}, {"$limit": 10}
    ]
    results = list(ventes.aggregate(pipeline))
    return jsonify([{"Modèle": r["_id"], "Ventes": r["total"]} for r in results])

@app.route("/ventes-par-region")
def ventes_par_region():
    pipeline = [{"$group": {"_id": "$Buyer Region", "total": {"$sum": 1}}}, {"$sort": {"total": -1}}]
    results = list(ventes.aggregate(pipeline))
    return jsonify([{"Région": r["_id"], "Ventes": r["total"]} for r in results])

@app.route("/taille-chaussures")
def taille_chaussures():
    pipeline = [{"$group": {"_id": "$Shoe Size", "total": {"$sum": 1}}}, {"$sort": {"_id": 1}}]
    results = list(ventes.aggregate(pipeline))
    return jsonify([{"Pointure": r["_id"], "Ventes": r["total"]} for r in results])

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
    return jsonify([
        {"Mois": r["_id"], "Ventes": r["ventes"], "Prix moyen": r["prix_moyen"]}
        for r in results
    ])

@app.route("/dates-de-sortie")
def dates_de_sortie():
    results = list(ventes.find({}, {
        "_id": 0,
        "Sneaker Name": 1,
        "releasedate": 1
    }))
    return jsonify([
        {"Modèle": r["Sneaker Name"], "Date de sortie": r["releasedate"]}
        for r in results if "Sneaker Name" in r and "releasedate" in r
    ])

@app.route("/explorer")
def explorer():
    marque = request.args.get("marque")
    if not marque:
        return jsonify([])
    results = list(ventes.find({"Brand": marque}, {"_id": 0, "Sneaker Name": 1, "Sale Price": 1}))
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
