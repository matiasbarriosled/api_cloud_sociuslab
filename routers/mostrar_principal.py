import plotly.graph_objects as go
import spacy
from collections import Counter
from fastapi import APIRouter
from models import ShowData
nlp = spacy.load("en_core_web_sm")

mostrar_ppal_router = APIRouter

@mostrar_ppal_router.post("/mostrar_ppal")
def analizar_y_mostrar_principal(data :ShowData):
    textos = data.resenias['frase']
    sustantivos_adjetivos = {}

    # Extraer sustantivos y adjetivos
    for texto in textos.dropna():
        doc = nlp(texto)
        for token in doc:
            if token.pos_ == "NOUN":  # Buscar sustantivos
                adjetivos = [child.text.lower() for child in token.children if child.pos_ == "ADJ"]
                if token.text.lower() not in sustantivos_adjetivos:
                    sustantivos_adjetivos[token.text.lower()] = adjetivos
                else:
                    sustantivos_adjetivos[token.text.lower()].extend(adjetivos)

    # Determinar el sustantivo más frecuente
    sustantivo_mas_relevante = max(sustantivos_adjetivos, key=lambda k: len(sustantivos_adjetivos[k]))
    adjetivos_asociados = sustantivos_adjetivos[sustantivo_mas_relevante]

    # Contar frecuencias de adjetivos
    adjetivos_frecuencias = Counter(adjetivos_asociados).most_common(5)  # Top 5 adjetivos más comunes
    adjetivos, frecuencias = zip(*adjetivos_frecuencias)  # Separar en listas

    total_adjetivos = sum(frecuencias)
    porcentajes = [freq / total_adjetivos * 100 for freq in frecuencias]

    # Crear gráfico de barras con Plotly
    fig = go.Figure(data=[go.Bar(
        x=adjetivos,
        y=frecuencias,
        text=[f"{p:.1f}%" for p in porcentajes],
        textposition='auto',
        marker_color='skyblue' if data.tipo == "praise" else 'salmon'
    )])
    fig.update_layout(
        title=f"{data.tipo.capitalize()} - of {sustantivo_mas_relevante}",
        xaxis_title="associated description",
        yaxis_title="Frecuency",
        xaxis=dict(tickangle=45)
    )
    return fig
    
    # Mostrar gráfico en Streamlit
    #st.plotly_chart(fig)
    ## Mostrar texto explicativo
    #st.write(f"**{data.tipo.capitalize()}**: The most important noun is '{sustantivo_mas_relevante}', "
    #        f"frequently accompanied by description:")
    #st.write(", ".join([f"{adj} ({porc:.1f}%)" for adj, porc in zip(adjetivos, porcentajes)]))