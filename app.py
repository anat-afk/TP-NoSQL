import streamlit as st
import pandas as pd
import requests

API_URL = "http://localhost:5000"

st.set_page_config(page_title="Analyse StockX", page_icon="👟", layout="wide")
st.title("👟 Analyse des ventes de sneakers sur StockX")

section = st.sidebar.selectbox("📌 Choisir une analyse", [
    "Accueil", "Vue globale", "Ventes par marque", "Mois avec le plus de ventes", "Évolution temporelle"
])

# --- ACCUEIL ---
if section == "Accueil":
    st.header("Bienvenue sur le tableau de bord StockX 👋")
    
    # METRICS
    col1, col2, col3 = st.columns(3)
    
    with col1:
        res = requests.get(f"{API_URL}/ventes/total").json()
        st.metric("Ventes totales enregistrées", res["total"])
    
    with col2:
        marques = requests.get(f"{API_URL}/ventes/marques").json()
        st.metric("Nombre de marques", len(marques))
    
    with col3:
        st.metric("API connectée", "✅")

    # Extrait de données
    st.subheader("📊 Exemple de données")
    sample = requests.get(f"{API_URL}/ventes/sample").json()
    df = pd.DataFrame(sample)
    st.dataframe(df)

# --- VUE GLOBALE ---
elif section == "Vue globale":
    res = requests.get(f"{API_URL}/ventes/total").json()
    st.metric("Nombre total de ventes", res["total"])

# --- VENTES PAR MARQUE ---
elif section == "Ventes par marque":
    data = requests.get(f"{API_URL}/ventes/marques").json()
    df = pd.DataFrame(data)
    df = df.rename(columns={"_id": "Marque", "total": "Ventes"})
    st.bar_chart(df.set_index("Marque"))

# --- MOIS AVEC LE PLUS DE VENTES ---
elif section == "Mois avec le plus de ventes":
    data = requests.get(f"{API_URL}/ventes/mois").json()
    df = pd.DataFrame(data)
    df = df.rename(columns={"_id": "Mois", "count": "Ventes"})
    st.bar_chart(df.set_index("Mois"))

# --- EVOLUTION TEMPORELLE ---
elif section == "Évolution temporelle":
    data = requests.get(f"{API_URL}/ventes/evolution").json()
    df = pd.DataFrame(data)
    df = df.rename(columns={"_id": "Mois", "ventes": "Ventes", "prix_moyen": "Prix moyen"})
    
    col1, col2 = st.columns(2)
    with col1:
        st.line_chart(df.set_index("Mois")["Ventes"])
    with col2:
        st.line_chart(df.set_index("Mois")["Prix moyen"])

# Pied de page
st.sidebar.markdown("---")
st.sidebar.info("TP NoSQL - Streamlit & Flask API")
