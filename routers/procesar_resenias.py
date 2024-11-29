import plotly.graph_objects as go
import plotly.express as px
from plotly.colors import sequential
import spacy
from nltk.sentiment import SentimentIntensityAnalyzer
import streamlit as st

nlp = spacy.load("en_core_web_sm")
sia = SentimentIntensityAnalyzer()

def procesar_resenias(reseñas, tipo):
    textos = reseñas['frase']
    complaints = {"Food": [], "Service": [], "Ambience": [], "Prices": [], "Organization": []}
    praise = {"Food": [], "Service": [], "Ambience": [], "Prices": []}
    
    for texto in textos.dropna():
        sentimiento = sia.polarity_scores(texto)
        doc = nlp(texto)
        for sent in doc.sents:
            if sentimiento["compound"] < 0:  # Reseñas negativas
                for token in sent:
                    if token.pos_ in ["NOUN", "ADJ"]:
                        if token.text.lower() in ["food", "meal", "dish", "cuisine"]:
                            complaints["Food"].append(token.text)
                        elif token.text.lower() in ["service", "staff", "waiter", "server"]:
                            complaints["Service"].append(token.text)
                        elif token.text.lower() in ["ambience", "atmosphere", "environment"]:
                            complaints["Ambience"].append(token.text)
                        elif token.text.lower() in ["price", "cost", "value"]:
                            complaints["Prices"].append(token.text)
                        elif token.text.lower() in ["organization", "management", "operation"]:
                            complaints["Organization"].append(token.text)
            elif sentimiento["compound"] > 0:  # Reseñas positivas
                for token in sent:
                    if token.pos_ in ["NOUN", "ADJ"]:
                        if token.text.lower() in ["ambience", "atmosphere", "environment"]:
                            praise["Ambience"].append(token.text)
                        elif token.text.lower() in ["food", "meal", "dish", "cuisine"]:
                            praise["Food"].append(token.text)
                        elif token.text.lower() in ["service", "staff", "waiter", "server"]:
                            praise["Service"].append(token.text)
                        elif token.text.lower() in ["price", "cost", "value"]:
                            praise["Prices"].append(token.text)

    if tipo == 'positivos':
        etiquetas = list(praise.keys())
        tamaños = [len(praise) for praise in praise.values()]
        colores = px.colors.sequential.Blues
    elif tipo == 'negativos':
        etiquetas = list(complaints.keys())
        tamaños = [len(complaints) for complaints in complaints.values()]
        colores = px.colors.sequential.Reds

    if sum(tamaños) == 0:
        st.warning(f"No hay datos suficientes para generar un gráfico de {tipo}.")
        return

    # Crear gráfico de pastel con Plotly
    fig = go.Figure(data=[go.Pie(
        labels=etiquetas,
        values=tamaños,
        hole=0.4,
        textinfo='label+percent',
        marker=dict(colors=px.colors.sequential.Blues if tipo == 'positivos' else px.colors.sequential.Reds)
       
    )])
    fig.update_layout(title=f"Frecuency of {'praise' if tipo == 'positivos' else 'complaints'}")

    st.plotly_chart(fig)
