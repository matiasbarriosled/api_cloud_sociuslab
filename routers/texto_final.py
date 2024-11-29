import spacy
from collections import Counter
nlp = spacy.load("en_core_web_sm")

def generar_texto_final(reseñas_negativas):
    textos = reseñas_negativas['frase']
    sustantivos_adjetivos = {}

    # Extraer sustantivos y adjetivos de las reseñas negativas
    for texto in textos.dropna():
        doc = nlp(texto)
        for token in doc:
            if token.pos_ == "NOUN":  # Buscar sustantivos
                adjetivos = [child.text.lower() for child in token.children if child.pos_ == "ADJ"]
                if token.text.lower() not in sustantivos_adjetivos:
                    sustantivos_adjetivos[token.text.lower()] = adjetivos
                else:
                    sustantivos_adjetivos[token.text.lower()].extend(adjetivos)

    # Identificar el sustantivo más relevante y sus adjetivos asociados
    if not sustantivos_adjetivos:
        return "No se encontraron suficientes datos para generar un resumen de las quejas."

    sustantivo_mas_relevante = max(sustantivos_adjetivos, key=lambda k: len(sustantivos_adjetivos[k]))
    adjetivos_asociados = sustantivos_adjetivos[sustantivo_mas_relevante]

    # Determinar el adjetivo más frecuente
    if not adjetivos_asociados:
        adjetivo_mas_relevante = "no descriptions"
    else:
        adjetivo_mas_relevante = Counter(adjetivos_asociados).most_common(1)[0][0]

    # Crear el texto final
    texto_final = (
        f"Complaints are usually caused by {sustantivo_mas_relevante},"
        f" which is usually described as {adjetivo_mas_relevante}."
    )

    return texto_final