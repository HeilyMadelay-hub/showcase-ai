# constants.py
LEGAL_CATEGORIES = [
    "contrato",
    "factura", 
    "demanda",
    "escritura",
    "testamento",
    "poder notarial",
    "certificado",
    "acta",
    "resolución",
    "sentencia"
]

# Configuración del modelo
MODEL_NAME = "facebook/bart-large-mnli"
CONFIDENCE_THRESHOLD = 0.4

"""

### 1️⃣ `LEGAL_CATEGORIES`

```python
LEGAL_CATEGORIES = [
    "contrato",
    "factura", 
    "demanda",
    "escritura",
    "testamento",
    "poder notarial",
    "certificado",
    "acta",
    "resolución",
    "sentencia"
]
```

* **Qué es:** una **lista de cadenas** (strings) que contiene las **categorías de documentos legales** que quieres clasificar.
* **Propósito:** cuando procesas un documento, el modelo va a intentar decir a cuál de estas categorías pertenece.
* Ejemplo de uso:

```python
for category in LEGAL_CATEGORIES:
    print(f"Comprobando si el documento es: {category}")
```

---

### 2️⃣ `MODEL_NAME`

```python
MODEL_NAME = "facebook/bart-large-mnli"
```

* **Qué es:** un **string con el nombre del modelo** que usarás para la clasificación de textos.
* **Propósito:** indica qué modelo de **Machine Learning/NLP** se va a cargar desde Hugging Face.
* En este caso: `bart-large-mnli` es un modelo de **inferencia de lenguaje natural** (NLI) que puede decidir si un texto “entra” dentro de una categoría o no.

---

### 3️⃣ `CONFIDENCE_THRESHOLD`

```python
CONFIDENCE_THRESHOLD = 0.5
```

* **Qué es:** un **número entre 0 y 1** que indica el **umbral mínimo de confianza**.
* **Propósito:** decide si la predicción del modelo es suficientemente segura para considerarla válida.
* Ejemplo práctico:

```python
confidence = 0.7
if confidence >= CONFIDENCE_THRESHOLD:
    print("Etiqueta aceptada")
else:
    print("Etiqueta rechazada")
```

* **Significado de 0.5:** si el modelo está **50% o más seguro**, la predicción se acepta; si está por debajo, se descarta.
"""