import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connexion à la base de données SQLite
conn = sqlite3.connect('olist.db')

# Fonction pour charger les données à partir de la base de données
def load_data_prediction():
    query = f"SELECT * FROM predictions;"
    df = pd.read_sql(query, conn)
    return df

def load_data_training(model_name):
    if model_name != "tous":
        query = f"SELECT * FROM {model_name}_TrainingDataset;"
    else:
        query = f"SELECT * FROM first_run_2017_TrainingDataset;"
    df = pd.read_sql(query, conn)
    return df

def plot_score_distribution(predictions_data,training_data):
    # Créer une figure avec deux sous-graphiques
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    # Premier sous-graphique : Distribution des scores pour la table "predictions"
    sns.countplot(data=predictions_data, x='prediction', ax=axes[0])
    axes[0].set_title('Distribution des scores - Prédictions')
    # Deuxième sous-graphique : Distribution des scores pour la table "Training"
    sns.countplot(data=training_data, x='score', ax=axes[1])
    axes[1].set_title('Distribution des scores - Entraînement')
    # Afficher les graphiques
    st.pyplot(fig)

def plot_variable_distribution(predictions_data,training_data,variable):
    # Créer une figure avec deux sous-graphiques
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    # Premier sous-graphique : Distribution des scores pour la table "predictions"
    sns.histplot(data=predictions_data,  x=variable, ax=axes[0], kde=True)
    axes[0].set_title('Distribution de {variable} - Prédictions')
    # Deuxième sous-graphique : Distribution des scores pour la table "Training"
    sns.histplot(data=training_data,  x=variable, ax=axes[1], kde=True)
    axes[1].set_title('Distribution de {variable} - Entraînement')
    # Afficher les graphiques
    st.pyplot(fig)



# Charger les données des tables "predictions" et "Training"
predictions_data = load_data_prediction()

# Sidebar pour la sélection du modèle
st.sidebar.header('Sélection du modèle')
selected_model = st.sidebar.selectbox('Choisissez un modèle',['tous'] + list(predictions_data['model'].unique()))

# Filtrer les données en fonction du modèle sélectionné
if selected_model != 'tous':
    filtered_predictions_data = predictions_data[predictions_data['model'] == selected_model]
else:
    filtered_predictions_data = predictions_data

filtered_training_data = load_data_training(selected_model)


# Titre de l'application
st.title('Evaluation du drift')

# Partie "Evaluation du prediction drift"
st.header('Evaluation du drift sur la distribution des prédictions')

plot_score_distribution(filtered_predictions_data,filtered_training_data)

# Partie "Evaluation du data drift"
st.header('Evaluation du drift sur la distribution des variables explicatives')

# Sélection de la variable explicative à afficher
selected_variable = st.selectbox('Sélectionnez une variable explicative', ['produit_recu', 'temps_livraison'])

# Affichage de la distribution de la variable explicative sélectionnée
plot_variable_distribution(filtered_predictions_data,filtered_training_data, selected_variable)

