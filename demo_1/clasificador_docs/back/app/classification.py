# Módulo de clasificación de documentos

class DocumentClassifier:

    LEGAL_CATEGORIES = ["Contratos", "Sentencias", "Normativas", "Licencias", "Otros"]

    def __init__(self):
        self.model = None
    
    def train_model(self, training_data):
        # Entrenar modelo de clasificación
        pass
    
    def classify_document(self, document):
        # Clasificar documento
        pass
    
    def predict_category(self, text):
        # Predecir categoría del texto
        pass
