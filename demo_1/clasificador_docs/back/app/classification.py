# classification.py
import logging
from typing import List

CATEGORY_KEYWORDS = {

    "contrato": [
        "contrato", "partes", "cláusula", "firmas", "objeto del contrato",
        "duración", "resolución", "obligaciones", "acuerdo", "vigencia",
        "condiciones contractuales", "incumplimiento", "firma de aceptación",
        "modificación", "terminación anticipada", "renuncia", "responsabilidad",
        "anexo", "sujeto a", "ejecución", "penalización", "cláusula penal",
        "pactos", "manifiestan", "reunidos", "precio", "transmisión",
        "contraprestación", "cumplimiento", "garantías", "indemnización"
    ],
    
    "contrato_traspaso": [  # Nueva categoría específica
        "traspaso", "negocio en funcionamiento", "fondo de comercio",
        "local de negocio", "transmisión de bienes", "precio del traspaso",
        "actividad económica", "explotación económica", "titular de actividad",
        "carta de pago", "bienes transmitidos", "metros cuadrados"
    ],
    
    "contrato_arrendamiento": [  # Nueva categoría
        "arrendamiento", "arrendador", "arrendatario", "renta mensual",
        "fianza", "duración del arrendamiento", "uso de vivienda",
        "gastos de comunidad", "suministros", "prórroga", "desahucio",
        "actualización de renta", "obras", "conservación"
    ],
    
    "contrato_compraventa": [  # Nueva categoría
        "compraventa", "vendedor", "comprador", "precio de venta",
        "cosa vendida", "entrega", "saneamiento", "vicios ocultos",
        "escritura de compraventa", "posesión", "tradición",
        "reserva de dominio", "pacto de retro"
    ],
    
    "escritura_publica": [  # Renombrada para mayor claridad
        "escritura pública", "notario", "protocolo", "fe pública",
        "comparecencia", "otorgamiento", "testimonio", "matriz",
        "número de protocolo", "libro de protocolo", "legitimación",
        "apostilla", "legalización", "copia autorizada", "inscripción registral",
        "registro de la propiedad", "folio", "tomo"
    ],
    
    "factura": [
        "factura", "importe", "folio", "RFC emisor", "RFC receptor",
        "total", "IVA", "concepto", "fecha de emisión", "forma de pago",
        "detalle de productos", "descuento", "subtotal", "base gravable",
        "retenciones", "comprobante", "número de serie", "fecha de recepción",
        "pago parcial", "condiciones de pago", "CFDI", "UUID",
        "sello digital", "cadena original", "certificado SAT"
    ],
    
    "acta": [
        "acta", "asistentes", "orden del día", "acuerdos",
        "aprobación", "firma", "constancia", "sesión", "reunión",
        "presidencia", "votación", "decisiones", "participantes", "lectura",
        "firmas de conformidad", "resoluciones adoptadas", "verificación de quorum",
        "convocatoria", "moción", "deliberación", "unanimidad", "mayoría"
    ],

   "poder_notarial": [
        # Términos esenciales
        "poder notarial",      # Indica el tipo de documento
        "apoderado",           # Persona que recibe el poder
        "facultades",          # Capacidades conferidas
        "representación",      # Acción de actuar en nombre del poderdante
        "actuar en mi nombre", # Frase típica de poderes
        "revocación",          # Posibilidad de revocar el poder
        "ratificación",        # Aceptación formal de los poderes otorgados
        "vigencia",            # Duración del poder
        "firma",               # Firma del poderdante
        "aceptación",          # Aceptación del apoderado
        "limitaciones",        # Límites de los poderes conferidos
        "documentos",          # Lo que puede firmar o presentar
        "contratos",           # Tipo de actos permitidos
        "actos administrativos" # Ámbito de actuación más común
    ],
    
    "estado_financiero": [
        "activo", "pasivo", "patrimonio", "ejercicio fiscal",
        "balance general", "estado de resultados", "flujo de efectivo",
        "ingresos", "gastos", "capital contable", "cuentas por cobrar",
        "cuentas por pagar", "reservas", "depreciación", "amortización",
        "utilidad neta", "EBITDA", "razones financieras", "notas a los estados"
    ],
    
    "declaracion_fiscal": [  # Sin tilde para evitar problemas de encoding
        "RFC", "ejercicio fiscal", "ingresos acumulables", "declaración",
        "deducciones autorizadas", "impuesto causado", "presentación", 
        "pago provisional", "saldo a favor", "compensación",
        "retenciones", "IVA", "ISR", "comprobantes fiscales", 
        "declaración anual", "declaración mensual", "DIOT", "DIM"
    ],
    
    "dictamen_fiscal": [  # Nueva categoría
        "dictamen fiscal", "contador público", "opinión", "estados financieros dictaminados",
        "carta de presentación", "informe sobre la situación fiscal",
        "anexos del dictamen", "contribuciones", "cumplimiento de obligaciones",
        "salvedades", "abstención de opinión", "opinión negativa"
    ],
    
    "resolucion_administrativa": [  # Categoría más específica
        "resolución", "autoridad administrativa", "fundamentos legales", 
        "considerandos", "resuelve", "notifíquese", "recurso administrativo",
        "plazo para impugnar", "acto administrativo", "competencia",
        "motivación", "fundamentación", "puntos resolutivos"
    ],
    
    "sentencia_judicial": [
        "sentencia", "tribunal", "fallo", "juez", "demandante",
        "demandado", "resuelve", "juzgado", "autos", "parte actora",
        "parte demandada", "resolución judicial", "apelación", "Sala", 
        "casación", "STC", "Audiencia Provincial", "considerando",
        "resultando", "vistos", "antecedentes de hecho", "fundamentos de derecho"
    ],

    "sentencia_TC": [
        "sentencia", "STC", "Sala", "considerando", "resultando", "vistos",
        "antecedentes de hecho", "fundamentos de derecho", 
        "vulneración del derecho", "recurrente", "órgano emisor",
        "referencias a STC", "auto de admisión", "fallo constitucional"
    ],
    "auto_resolucion": [
        "auto", "resolución", "notificación", "plazo", "competencia", 
        "motivación", "fundamentación", "puntos resolutivos"
    ],
    
    "informe_auditoria": [  # Sin tilde
        "informe de auditoría", "alcance", "hallazgos", "opinión del auditor",
        "revisión", "control interno", "observaciones", "recomendaciones",
        "riesgos identificados", "materialidad", "evidencia de auditoría",
        "procedimientos aplicados", "limitaciones al alcance", "carta de gerencia"
    ],
    "certificado": [
        "certificado", "emisor", "destinatario", "validez", "autenticidad",
        "vigencia", "sello", "documento oficial", "constancia",
        "certificación oficial", "registro de validez", "autorización"
    ],
    "comprobante fiscal": [
        "RFC emisor", "importe", "folio", "comprobante fiscal",
        "detalle de impuestos", "concepto", "total", "fecha de emisión",
        "forma de pago", "certificado digital", "sellos electrónicos"
    ],

    "sanción": [
        "sanción", "autoridad", "infracción", "multa",
        "penalización", "cumplimiento", "reglamento", "incumplimiento",
        "advertencia", "responsabilidad", "sanción económica"
    ],
    "denuncia": [
        "denuncia", "denunciante", "denunciado", "hechos",
        "reclamación", "presentación formal", "investigación", "expediente",
        "acusación", "procedimiento legal", "informe de hechos"
    ],
    "fiscal": [
        "ingresos", "deducciones", "ejercicio fiscal",
        "obligaciones fiscales", "impuesto", "declaración", "cumplimiento",
        "retenciones", "pagos provisionales", "ajustes fiscales", "revisión"
    ],
    
    "laboral": [
        "acuerdo laboral",
        "beneficios",
        "colaborador",
        "condiciones laborales",
        "contrato laboral",
        "contrato de trabajo",
        "despido",
        "empleado",
        "empleador",
        "fin de contrato",
        "huelga",
        "horario",
        "jornada",
        "licencia",
        "modificación de contrato",
        "pacto laboral",
        "prestaciones",
        "reglamento interno",
        "remuneración",
        "salario",
        "sueldo",
        "seguridad social",
        "terminación de contrato",
        "vacaciones",
        "trabajador"
    ],
    "mercantil": [
        "sociedad", "objeto social", "capital", "accionistas",
        "asamblea", "estatutos", "participaciones", "acciones",
        "fusiones", "disolución", "liquidación", "capital social",
        "contratos mercantiles", "representante legal", "comercio"
    ],
    "cumplimiento normativo": [
        "norma aplicable", "controles", "responsable de cumplimiento",
        "auditoría", "procedimientos", "reglamento", "políticas internas",
        "evaluación de riesgos", "reportes de cumplimiento",
        "monitoreo", "verificación", "informes de cumplimiento"
    ],
}

def classify_text(text: str) -> dict:
    """
    Clasificación heurística basada en keywords.
    No usa modelo de ML, útil para demo rápida.
    """
    if not text or len(text.strip()) < 10:
        logging.warning("Texto demasiado corto para clasificación")
        return {"category": "unknown", "confidence": 0.0, "all_scores": []}

    scores = {}
    text_lower = text.lower()

    # Contar keywords encontradas por categoría
    for category, keywords in CATEGORY_KEYWORDS.items():
        match_count = sum(1 for kw in keywords if kw.lower() in text_lower)
        scores[category] = match_count / len(keywords)  # porcentaje de coincidencias

    # Ordenar por score descendente
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Categoría con mayor score
    top_category, top_score = sorted_scores[0]

    if top_score == 0:
        top_category = "sin clasificar"

    return {
        "category": top_category,
        "confidence": float(top_score),
        "all_scores": [(cat, float(score)) for cat, score in sorted_scores]
    }
