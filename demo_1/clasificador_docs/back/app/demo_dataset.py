# demo_dataset.py

class DemoDataset:
    def __init__(self):
        self.documents = []

    def load_demo_data(self):
        """Cargar datos de demostración en la lista de documentos."""
        self.documents = [
            {
                "title": "Contrato de arrendamiento",
                "text": "Este contrato establece las condiciones de alquiler de la vivienda entre el arrendador y el arrendatario.",
                "category": "Contratos"
            },
            {
                "title": "Sentencia judicial 001",
                "text": "El tribunal ha decidido en favor del demandante en el caso de incumplimiento de contrato.",
                "category": "Sentencias"
            },
            {
                "title": "Licencia de software",
                "text": "Se concede una licencia no exclusiva para el uso del software según los términos indicados.",
                "category": "Licencias"
            },
            {
                "title": "Reglamento interno",
                "text": "El presente reglamento establece las normas de convivencia dentro de la empresa.",
                "category": "Normativas"
            },
            {
                "title": "Contrato de prestación de servicios",
                "text": "El proveedor se compromete a entregar los servicios acordados bajo los términos del contrato.",
                "category": "Contratos"
            },
            {
                "title": "Sentencia judicial 002",
                "text": "Se desestima la demanda por falta de pruebas suficientes para probar el incumplimiento.",
                "category": "Sentencias"
            },
            {
                "title": "Licencia de uso de imagen",
                "text": "Se otorga permiso para utilizar la imagen en campañas publicitarias durante un año.",
                "category": "Licencias"
            },
            {
                "title": "Normativa de seguridad",
                "text": "Todos los empleados deben cumplir las normas de seguridad establecidas en el manual.",
                "category": "Normativas"
            },
            {
                "title": "Contrato de confidencialidad",
                "text": "El firmante se compromete a mantener la información confidencial de la empresa en secreto.",
                "category": "Contratos"
            },
            {
                "title": "Documento varios",
                "text": "Este es un documento de prueba que no encaja en las categorías anteriores.",
                "category": "Otros"
            }
        ]

    def get_documents(self):
        return self.documents


# Prueba rápida
if __name__ == "__main__":
    demo = DemoDataset()
    demo.load_demo_data()
    for doc in demo.get_documents():
        print(f"{doc['title']} ({doc['category']}): {doc['text'][:60]}...")
