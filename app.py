import streamlit as st
import pandas as pd
import requests

BASE_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Analyse StockX", page_icon="👟", layout="wide")
st.title("👟 Analyse des ventes de sneakers via API")

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

if section == "Accueil":
    st.header("Bienvenue 👋")
    st.markdown("""
    Explorez les données de vente StockX à travers notre API Flask :
    - 📊 Marques, régions, tailles
    - 📈 Évolution mensuelle
    - 🔝 Modèles populaires
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        total = requests.get(f"{BASE_URL}/total-ventes").json()["total"]
        st.metric("Ventes totales", total)

    with col2:
        marques = requests.get(f"{BASE_URL}/marques").json()
        st.metric("Nombre de marques", len(marques))

    with col3:
        regions = requests.get(f"{BASE_URL}/regions").json()
        st.metric("Régions couvertes", len(regions))

    st.subheader("📋 Échantillon de données")
    echantillon = pd.DataFrame(requests.get(f"{BASE_URL}/echantillon").json())
    st.dataframe(echantillon)

elif section == "Vue globale":
    total = requests.get(f"{BASE_URL}/total-ventes").json()["total"]
    st.metric("Nombre total de ventes", total)

elif section == "Ventes par marque":
    df = pd.DataFrame(requests.get(f"{BASE_URL}/ventes-par-marque").json())
    st.bar_chart(df.set_index("Marque"))

elif section == "Mois avec le plus de ventes":
    df = pd.DataFrame(requests.get(f"{BASE_URL}/ventes-par-mois").json())
    st.bar_chart(df.set_index("Mois"))

elif section == "Marques par région":
    df = pd.DataFrame(requests.get(f"{BASE_URL}/marques-par-region").json())
    st.dataframe(df)

elif section == "Top modèles":
    df = pd.DataFrame(requests.get(f"{BASE_URL}/top-modeles").json())
    st.bar_chart(df.set_index("Modèle"))

elif section == "Par région":
    df = pd.DataFrame(requests.get(f"{BASE_URL}/ventes-par-region").json())
    st.bar_chart(df.set_index("Région"))

elif section == "Taille des chaussures":
    df = pd.DataFrame(requests.get(f"{BASE_URL}/taille-chaussures").json())
    st.bar_chart(df.set_index("Pointure"))

elif section == "Évolution temporelle":
    df = pd.DataFrame(requests.get(f"{BASE_URL}/evolution-temporelle").json())
    df["Prix moyen"] = df["Prix moyen"].round(2)
    col1, col2 = st.columns(2)
    with col1:
        st.line_chart(df.set_index("Mois")["Ventes"])
    with col2:
        st.line_chart(df.set_index("Mois")["Prix moyen"])

elif section == "Dates de sortie":
    df = pd.DataFrame(requests.get(f"{BASE_URL}/dates-de-sortie").json())
    df["Date de sortie"] = pd.to_datetime(df["Date de sortie"], errors='coerce')
    df = df.sort_values("Date de sortie")
    st.write("📅 Dates de sortie")
    st.dataframe(df)

elif section == "Explorer les données":
    marques = requests.get(f"{BASE_URL}/marques").json()
    marque = st.selectbox("Choisir une marque", sorted(marques))
    if marque:
        df = pd.DataFrame(requests.get(f"{BASE_URL}/explorer", params={"marque": marque}).json())
        st.dataframe(df)

st.sidebar.markdown("---")
st.sidebar.info("Données via API Flask 🧪")
