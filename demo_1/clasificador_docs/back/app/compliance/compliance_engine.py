# compliance_engine.py
from app.explanation.explanation import explain_with_context, ExplanationResult

class ComplianceEngine:
    """
    Wrapper para centralizar la validación de documentos y reglas legales.
    """

    def validate(self, text: str, category: str) -> ExplanationResult:
        """
        Valida un documento usando explain_with_context.
        Recibe texto y categoría, devuelve ExplanationResult encapsulado.
        """
        # 1️⃣ Llama al motor de explicación
        result = explain_with_context(text, category)

        # 2️⃣ Retorna el objeto ExplanationResult completo
        return result
