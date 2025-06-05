import streamlit as st
import pandas as pd
from pymongo import MongoClient

# Connexion MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["stockx"]
ventes = db["ventes"]

# Interface Streamlit
st.set_page_config(page_title="Analyse StockX", page_icon="👟", layout="wide")
st.title("👟 Analyse des ventes de sneakers sur StockX")

# Menu latéral
section = st.sidebar.selectbox("📌 Choisir une analyse", [
    "Accueil",
    "Vue globale",
    "Ventes par marque", 
    "Mois avec le plus de ventes",
    "Marques par région",
    "Top modèles",
    "Par région",
    "Taille des chaussures",
    "Évolution temporelle",
    "Dates de sortie",
    "Explorer les données"
])

# PAGE D'ACCUEIL
if section == "Accueil":
    st.header("Bienvenue sur le tableau de bord StockX 👋")
    st.markdown("""
    Cette application vous permet d'explorer les ventes de sneakers sur la plateforme **StockX**.
    
    Voici ce que vous pouvez analyser :
    - 📈 Évolution des ventes au fil du temps
    - 🏷️ Marques les plus populaires
    - 🌎 Répartition des ventes par région
    - 🔝 Modèles et couleurs les plus vendus
    - 📅 Dates de sortie des sneakers
    - 🔍 Exploration personnalisée des données
    
    """)
    
    # Aperçu des données
    col1, col2, col3 = st.columns(3)
    with col1:
        total = ventes.count_documents({})
        st.metric("Ventes totales enregistrées", total)
    
    with col2:
        marques = ventes.distinct("Brand")
        st.metric("Nombre de marques", len(marques))
    
    with col3:
        regions = ventes.distinct("Buyer Region")
        st.metric("Régions couvertes", len(regions))

    st.subheader("📊 Exemple de données")
    sample = pd.DataFrame(list(ventes.find({}, {
        "_id": 0,
        "Sneaker Name": 1,
        "Brand": 1,
        "Sale Price": 1,
        "Shoe Size": 1,
        "Buyer Region": 1,
        "releasedate": 1
    }).limit(5)))
    st.dataframe(sample)

# AUTRES SECTIONS
elif section == "Vue globale":
    total = ventes.count_documents({})
    st.metric("Nombre total de ventes", total)

elif section == "Ventes par marque":
    pipeline = [{"$group": {"_id": "$Brand", "total": {"$sum": 1}}}, {"$sort": {"total": -1}}]
    df = pd.DataFrame(list(ventes.aggregate(pipeline)))
    df = df.rename(columns={"_id": "Marque", "total": "Ventes"})
    st.bar_chart(df.set_index("Marque"))

elif section == "Mois avec le plus de ventes":
    pipeline = [
        {"$group": {"_id": {"$substr": ["$orderdate", 0, 7]}, "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}, 
        {"$limit": 12}
    ]
    df = pd.DataFrame(list(ventes.aggregate(pipeline)))
    df = df.rename(columns={"_id": "Mois", "count": "Ventes"})
    st.bar_chart(df.set_index("Mois"))

elif section == "Marques par région":
    pipeline = [
        {"$group": {"_id": {"region": "$Buyer Region", "brand": "$Brand"}, "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 20}
    ]
    result = list(ventes.aggregate(pipeline))
    df = pd.DataFrame([{"Région": r["_id"]["region"], "Marque": r["_id"]["brand"], "Ventes": r["count"]} for r in result])
    st.dataframe(df.sort_values("Ventes", ascending=False))

elif section == "Top modèles":
    pipeline = [
        {"$group": {"_id": "$Sneaker Name", "total": {"$sum": 1}}}, 
        {"$sort": {"total": -1}}, 
        {"$limit": 10}
    ]
    df = pd.DataFrame(list(ventes.aggregate(pipeline)))
    df = df.rename(columns={"_id": "Modèle", "total": "Ventes"})
    st.bar_chart(df.set_index("Modèle"))

elif section == "Par région":
    pipeline = [{"$group": {"_id": "$Buyer Region", "total": {"$sum": 1}}}, {"$sort": {"total": -1}}]
    df = pd.DataFrame(list(ventes.aggregate(pipeline)))
    df = df.rename(columns={"_id": "Région", "total": "Ventes"})
    st.bar_chart(df.set_index("Région"))

elif section == "Taille des chaussures":
    pipeline = [{"$group": {"_id": "$Shoe Size", "total": {"$sum": 1}}}, {"$sort": {"_id": 1}}]
    df = pd.DataFrame(list(ventes.aggregate(pipeline)))
    df = df.rename(columns={"_id": "Pointure", "total": "Ventes"})
    st.bar_chart(df.set_index("Pointure"))

elif section == "Évolution temporelle":
    pipeline = [
        {"$group": {
            "_id": {"$substr": ["$orderdate", 0, 7]},
            "ventes": {"$sum": 1},
            "prix_moyen": {"$avg": "$Sale Price"}
        }},
        {"$sort": {"_id": 1}}
    ]
    result = list(ventes.aggregate(pipeline))
    df = pd.DataFrame(result)
    df = df.rename(columns={"_id": "Mois", "ventes": "Ventes", "prix_moyen": "Prix moyen"})
    
    col1, col2 = st.columns(2)
    with col1:
        st.line_chart(df.set_index("Mois")["Ventes"])
    with col2:
        st.line_chart(df.set_index("Mois")["Prix moyen"])

elif section == "Dates de sortie":
    pipeline = [
        {
            "$project": {
                "_id": 0,
                "Modèle": "$Sneaker Name",
                "Date de sortie": "$releasedate"
            }
        },
        {"$sort": {"Date de sortie": 1}}
    ]
    
    df = pd.DataFrame(list(ventes.aggregate(pipeline)))
    df["Date de sortie"] = pd.to_datetime(df["Date de sortie"], errors='coerce')
    df = df.sort_values("Date de sortie")
    
    st.write("📅 Liste des dates de sortie des modèles")
    st.dataframe(df)

elif section == "Explorer les données":
    marque = st.selectbox("Choisir une marque", sorted(ventes.distinct("Brand")))
    df = pd.DataFrame(list(ventes.find({"Brand": marque}, {"_id": 0, "Sneaker Name": 1, "Sale Price": 1})))
    st.dataframe(df)

# Pied de page
st.sidebar.markdown("---")
st.sidebar.info("TP NoSQL")