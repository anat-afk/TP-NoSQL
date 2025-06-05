# TP-NoSQL

# Catalogue de Sneakers – Analyse & Visualisation

Projet réalisé en binôme dans le cadre d’un travail pratique. L’objectif était de créer une interface interactive pour explorer et analyser des données de ventes de sneakers issues de la plateforme StockX.

---

## Sujet choisi

Création d’un catalogue de produits Sneakers avec visualisation dynamique, filtres, recherches et analyses de ventes.

---

## Objectifs

- Consulter, filtrer et rechercher des modèles de sneakers.
- Visualiser les statistiques de ventes : marques, modèles, tailles, régions, dates.
- Fournir une interface claire et simple pour analyser les tendances du marché.

---

## Technologies utilisées

### MongoDB
- Stockage flexible et structuré en JSON.
- Idéal pour gérer les données imbriquées comme prix, tailles ou historique des ventes.
- Schéma évolutif pour s’adapter facilement aux besoins du projet.

### Streamlit
- Framework Python rapide pour créer des interfaces interactives.
- Intégration facile avec MongoDB via `PyMongo`.
- Permet de créer des graphiques, filtres, menus dynamiques sans complexité.

### Outils de développement
- VS Code pour coder à deux efficacement.
- DBML pour documenter la structure des données MongoDB.

---

## Requêtes MongoDB intégrées

Voici les principales requêtes que nous avons implémentées :

1. Nombre total de ventes
2. Ventes par marque
3. Mois avec le plus de ventes
4. Ventes par région
5. Modèles les plus vendus
6. Marques par région
7. Pointures les plus vendues
8. Évolution des ventes dans le temps
9. Prix moyen par mois
10. Dates de sortie des modèles

---

## Aperçu de l’application

### Accueil & échantillon de données  
Affichage du nombre total de ventes et visualisation rapide des données brutes.

### Analyse visuelle  
- Graphiques par marque, région, mois, taille
- Suivi temporel de la popularité et du prix moyen
- Exploration des dates de sortie
- Filtres interactifs par marque

---
