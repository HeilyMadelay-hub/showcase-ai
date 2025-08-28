# classification.py
import logging
from setfit import SetFitModel
from constants import LEGAL_CATEGORIES

# Cargamos un modelo SetFit preentrenado (rápido y fácil de usar)
try:
    model = SetFitModel.from_pretrained("BAAI/bge-small-en-v1.5") #from_pretrained(...) carga un modelo que ya ha sido entrenado en un corpus grande.
    """
    La mayoría de tareas de NLP usan transfer learning: 
    cargas un modelo ya entrenado y luego lo ajustas a tu problema
    (fine-tuning) o lo usas tal cual (zero-shot).

    Así obtienes resultados decentes con pocos datos y latencia baja.
    
    En este caso, lo que estás haciendo con SetFit es un tipo de fine-tuning muy ligero:

    Cargas un modelo preentrenado de embeddings (BAAI/bge-small-en-v1.5).

    Luego lo ajustas a tu problema de clasificación de documentos legales, usando las categorías definidas en LEGAL_CATEGORIES.

    Esto no es un entrenamiento desde cero, sino transfer learning, donde el modelo ya conoce lenguaje general y solo se especializa en tu tarea específica.

    Por eso obtienes:

    Menor necesidad de datos: con unos pocos ejemplos puedes tener buena precisión.

    Latencia baja: el modelo ya tiene embeddings listos.

    Flexibilidad: puedes cambiar tus categorías sin entrenar un modelo completamente nuevo.
        
    """
    logging.info("Modelo SetFit cargado correctamente")
except Exception as e:
    logging.error("No se pudo cargar el modelo SetFit", exc_info=True)
    model = None

def classify_text(text: str) -> dict:
    """
    Clasifica un texto en categorías legales usando SetFit.

    Args:
        text (str): Texto a clasificar.

    Returns:
        dict: {
            'category': str,          # categoría más probable
            'confidence': float,      # score de confianza de esa categoría
            'all_scores': list        # lista [(categoría, score), ...]
        }
    """
    # Validamos que haya texto suficiente
    if not text or len(text.strip()) < 10:
        logging.warning("Texto demasiado corto para clasificación")
        return {"category": "unknown", "confidence": 0.0, "all_scores": []}

    # Validamos que el modelo esté cargado para no llamarlo si no esta listo 
    if model is None:
        return {"category": "error", "confidence": 0.0, "all_scores": []}



    """
    Aquí usamos la función `predict_proba` del modelo SetFit para obtener la probabilidad de que un texto pertenezca a cada categoría legal definida en `LEGAL_CATEGORIES`. 
    Aunque solo vamos a clasificar un único texto, `predict_proba` espera recibir una lista de textos, por eso pasamos `[text]`. 
    El resultado es una lista de listas: cada sublista contiene los scores de cada categoría para un texto. Como solo tenemos un texto, accedemos al primer elemento con `[0]`. 
    Luego usamos `zip` para emparejar cada categoría con su score correspondiente, generando una lista de tuplas `(categoría, score)` que podemos ordenar o procesar fácilmente para determinar la categoría más probable.

    Ejemplo práctico:
    LEGAL_CATEGORIES = ["contrato", "factura", "demanda"]
    text = "El acuerdo establece los términos de pago entre las partes."

    scores = model.predict_proba([text])[0]
    scores podría ser [0.85, 0.10, 0.05] indicando la probabilidad para cada categoría

    all_scores = list(zip(LEGAL_CATEGORIES, scores))
    all_scores será [('contrato', 0.85), ('factura', 0.10), ('demanda', 0.05)]
    La categoría más probable es 'contrato' con score 0.85
    """
    try:
        # Obtenemos los scores del modelo para cada categoría
        scores = model.predict_proba([text])[0]

        # Creamos una lista combinando categoría + score
        all_scores = list(zip(LEGAL_CATEGORIES, scores))

        # Ordenamos las categorías por score descendente
        all_scores.sort(key=lambda x: x[1], reverse=True)

        # Tomamos la categoría con más confianza
        top_category, top_score = all_scores[0]

        # Si el score es bajo, marcamos como "uncertain"
        if top_score < 0.5:
            logging.warning(f"Confianza baja: {top_category} ({top_score:.2f})")
            top_category = "uncertain"

        # Retornamos resultado
        return {
            "category": top_category,
            "confidence": float(top_score),
            "all_scores": [(cat, float(score)) for cat, score in all_scores]
        }

    except Exception as e:
        logging.error("Error clasificando el texto", exc_info=True)
        return {"category": "error", "confidence": 0.0, "all_scores": []}
