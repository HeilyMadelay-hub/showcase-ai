# demo_dataset.py

class DemoDataset:
    def __init__(self):
        self.documents = []

    def load_demo_data(self):
        """Cargar datos de demostración estáticos con info completa."""
        self.documents = [
            {
                "title": "Contrato de arrendamiento",
                "text": "Este contrato establece las condiciones de alquiler de la vivienda entre el arrendador y el arrendatario.",
                "category": "contrato",
                "confidence": 0.95,
                "compliance": "✅",
                "hash_integrity": "a1b2c3d4e5f67890123456789abcdef1234567890abcdef1234567890abcdef",
                "explanation": "Contiene partes, objeto del contrato y firmas. Cumple todas las reglas mínimas.",
                "cited_articles": ["art. 1", "art. 2"],
                "hits": ["partes", "objeto del contrato", "firmas"],
                "misses": []
            },
            {
                "title": "Sentencia judicial 001",
                "text": "El tribunal ha decidido en favor del demandante en el caso de incumplimiento de contrato.",
                "category": "sentencia",
                "confidence": 0.92,
                "compliance": "✅",
                "hash_integrity": "b1c2d3e4f567890123456789abcdef1234567890abcdef1234567890abcd",
                "explanation": "Contiene hechos probados, fallo y condena/absuelve. Cumple todas las reglas mínimas.",
                "cited_articles": ["art. 45 CP"],
                "hits": ["hechos probados", "fallo", "condena/absuelve"],
                "misses": []
            },
            {
                "title": "Licencia de software",
                "text": "Se concede una licencia no exclusiva para el uso del software según los términos indicados.",
                "category": "otros",
                "confidence": 0.85,
                "compliance": "⚠️",
                "hash_integrity": "c1d2e3f4567890123456789abcdef1234567890abcdef1234567890abcde",
                "explanation": "No cumple todas las reglas mínimas, algunas partes faltan.",
                "cited_articles": [],
                "hits": [],
                "misses": ["partes", "objeto del contrato", "firmas"]
            },
            {
                "title": "Reglamento interno",
                "text": "El presente reglamento establece las normas de convivencia dentro de la empresa.",
                "category": "normativa",
                "confidence": 0.9,
                "compliance": "✅",
                "hash_integrity": "d1e2f34567890123456789abcdef1234567890abcdef1234567890abcdef",
                "explanation": "Incluye ámbito y artículos citados. Cumple reglas mínimas.",
                "cited_articles": ["art. 3", "art. 4"],
                "hits": ["ámbito", "artículos citados"],
                "misses": []
            },
            {
                "title": "Contrato de prestación de servicios",
                "text": "El proveedor se compromete a entregar los servicios acordados bajo los términos del contrato.",
                "category": "contrato",
                "confidence": 0.93,
                "compliance": "✅",
                "hash_integrity": "e1f234567890123456789abcdef1234567890abcdef1234567890abcdef1",
                "explanation": "Contiene partes, objeto del contrato y firmas. Cumple todas las reglas mínimas.",
                "cited_articles": ["art. 5"],
                "hits": ["partes", "objeto del contrato", "firmas"],
                "misses": []
            },
            {
                "title": "Sentencia judicial 002",
                "text": "Se desestima la demanda por falta de pruebas suficientes para probar el incumplimiento.",
                "category": "sentencia",
                "confidence": 0.91,
                "compliance": "⚠️",
                "hash_integrity": "f1234567890123456789abcdef1234567890abcdef1234567890abcdef12",
                "explanation": "Faltan algunos elementos de la sentencia completa, revisión parcial.",
                "cited_articles": ["art. 46 CP"],
                "hits": ["fallo"],
                "misses": ["hechos probados", "condena/absuelve"]
            },
            {
                "title": "Licencia de uso de imagen",
                "text": "Se otorga permiso para utilizar la imagen en campañas publicitarias durante un año.",
                "category": "otros",
                "confidence": 0.87,
                "compliance": "⚠️",
                "hash_integrity": "0123456789abcdef1234567890abcdef1234567890abcdef1234567890ab",
                "explanation": "Algunas reglas mínimas no cumplidas.",
                "cited_articles": [],
                "hits": [],
                "misses": ["partes", "objeto del contrato", "firmas"]
            },
            {
                "title": "Normativa de seguridad",
                "text": "Todos los empleados deben cumplir las normas de seguridad establecidas en el manual.",
                "category": "normativa",
                "confidence": 0.92,
                "compliance": "✅",
                "hash_integrity": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcd",
                "explanation": "Incluye ámbito y artículos citados. Cumple reglas mínimas.",
                "cited_articles": ["art. 6"],
                "hits": ["ámbito", "artículos citados"],
                "misses": []
            },
            {
                "title": "Contrato de confidencialidad",
                "text": "El firmante se compromete a mantener la información confidencial de la empresa en secreto.",
                "category": "contrato",
                "confidence": 0.94,
                "compliance": "✅",
                "hash_integrity": "234567890abcdef1234567890abcdef1234567890abcdef1234567890abc",
                "explanation": "Contiene partes, objeto del contrato y firmas. Cumple todas las reglas mínimas.",
                "cited_articles": ["art. 7"],
                "hits": ["partes", "objeto del contrato", "firmas"],
                "misses": []
            },
            {
                "title": "Documento varios",
                "text": "Este es un documento de prueba que no encaja en las categorías anteriores.",
                "category": "otros",
                "confidence": 0.8,
                "compliance": "❌",
                "hash_integrity": "34567890abcdef1234567890abcdef1234567890abcdef1234567890abcd",
                "explanation": "No cumple ninguna regla mínima.",
                "cited_articles": [],
                "hits": [],
                "misses": ["partes", "objeto del contrato", "firmas"]
            }
        ]

    def get_documents(self):
        return self.documents

