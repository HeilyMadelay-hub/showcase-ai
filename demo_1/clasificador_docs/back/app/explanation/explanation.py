# explanation.py
from dataclasses import dataclass
from app.classification import CATEGORY_KEYWORDS
from typing import List
import re

@dataclass
class ExplanationResult:
    summary: str
    cited_articles: List[str]
    compliance_status: str  # "✅", "⚠️", "❌"
    hits: List[str]
    misses: List[str]
    confidence: float  # confianza de 0 a 1

patterns = [
    # Artículos, apartados y cláusulas
    r"\bart\.?\s*\d+\b",
    r"\bartículo\s+\d+\b",
    r"\binciso\s+[a-zA-Z0-9]+\b",
    r"\bapartado\s+\d+[a-zA-Z]?\b",
    r"\bcláusula\s+\d+[a-zA-Z]?\b",
    r"\bsección\s+\d+[a-zA-Z]?\b",

    # Referencias a partes y firmas
    r"\bpartes\b",
    r"\bobjeto\b",
    r"\bfirmado\b",
    r"\bfirma\b",
    r"\botorgante\b",
    r"\brepresentante\b",
    r"\bapoderado\b",
    
    # Información administrativa
    r"\bimporte\b",
    r"\bfolio\b",
    r"\bRFC\b",
    r"\basistentes\b",
    r"\borden del día\b",
    r"\bacuerdos\b",
    r"\bemisor\b",
    r"\bdestinatario\b",
    r"\bvalidez\b",
    r"\bactivo\b",
    r"\bpasivo\b",
    r"\bpatrimonio\b",
    r"\bfallo\b",
    r"\bautoridad\b",
    r"\binfracción\b",
    r"\bmulta\b",

    # Conceptos legales de contrato
    r"\brelación laboral\b",
    r"\bcontratación\b",
    r"\bperíodo de prueba\b",
    r"\bfinalización de contrato\b",
    r"\bterminación de contrato\b",
    r"\bbeneficios\b",
    r"\bprestaciones\b",
    r"\bsueldo\b",
    r"\bsalario\b",
    r"\bremuneración\b",
    r"\bjornada\b",
    r"\bhorario\b",
    r"\bvacaciones\b",
    r"\blesión\b",
    r"\bmodificación de contrato\b",
    r"\bacuerdo laboral\b",
    r"\bpacto laboral\b",
    
    # Seguridad social y compensaciones
    r"\bseguridad social\b",
    r"\bsubsidio\b",
    r"\bprestación por desempleo\b",

    # Otros términos legales frecuentes
    r"\breglamento interno\b",
    r"\bhuelga\b",
    r"\blicencia\b",
    r"\bpermiso\b",
    r"\breestructuración\b",
    r"\bdespido\b",
    
    # Expresiones más largas que suelen aparecer en contratos
    r"\btrabajador\/a\b",
    r"\bempleado\/a\b",
    r"\bempleador\/a\b",
    r"\bpersona con discapacidad\b",
    r"\btiempo completo\b",
    r"\btiempo parcial\b",
    r"\bfijo-discontinuo\b"
]


def split_into_sentences(text: str) -> List[str]:
    sentences = re.split(r'(?<=[\.\n;])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def detect_patterns(sentence: str, patterns: List[str]) -> List[str]:
    return [pat for pat in patterns if re.search(pat, sentence, re.IGNORECASE)]


def explain_with_context(text: str, category: str) -> ExplanationResult:
    rules_for_category = CATEGORY_KEYWORDS.get(category, [])
    hits, misses, sentence_scores, cited_articles = [], [], [], []

    sentences = split_into_sentences(text)

    buffer = ""
    buffer_patterns = set()

    for sentence in sentences:
        sentence_patterns = set(detect_patterns(sentence, patterns))
        sentence_lower = sentence.lower()
        matched_keywords = [kw for kw in rules_for_category if kw.lower() in sentence_lower]

        if buffer and (buffer_patterns & sentence_patterns):
            buffer += " " + sentence
            buffer_patterns.update(sentence_patterns)
        else:
            if buffer:
                cited_articles.append(buffer)
                buffer_lower = buffer.lower()
                buffer_matched_keywords = [kw for kw in rules_for_category if kw.lower() in buffer_lower]
                if buffer_matched_keywords or buffer_patterns:
                    hits.append(f"{buffer} (keywords: {buffer_matched_keywords}, patterns: {list(buffer_patterns)})")
                    score = len(buffer_matched_keywords) / len(rules_for_category) if rules_for_category else 0
                    sentence_scores.append(score)
                else:
                    sentence_scores.append(0)
            buffer = sentence
            buffer_patterns = sentence_patterns

    if buffer:
        cited_articles.append(buffer)
        buffer_lower = buffer.lower()
        buffer_matched_keywords = [kw for kw in rules_for_category if kw.lower() in buffer_lower]
        if buffer_matched_keywords or buffer_patterns:
            hits.append(f"{buffer} (keywords: {buffer_matched_keywords}, patterns: {list(buffer_patterns)})")
            score = len(buffer_matched_keywords) / len(rules_for_category) if rules_for_category else 0
            sentence_scores.append(score)
        else:
            sentence_scores.append(0)

    for kw in rules_for_category:
        if not any(kw.lower() in s.lower() for s in cited_articles):
            misses.append(kw)

    # NUEVO: cálculo basado en porcentaje de keywords encontradas
    total_keywords = len(rules_for_category)
    found_keywords = total_keywords - len(misses)
    percent = (found_keywords / total_keywords) * 100 if total_keywords > 0 else 0

    if percent >= 60:
        compliance_status = "✅"
    elif 30 <= percent < 60:
        compliance_status = "⚠️"
    else:
        compliance_status = "❌"

    confidence = percent / 100
    summary = (
        f"Resumen para '{category}': {len(hits)} fragmentos con coincidencias, "
        f"{len(misses)} palabras clave faltantes ({misses}), "
        f"cumplimiento: {percent:.1f}%."
    )

    return ExplanationResult(
        summary=summary,
        cited_articles=cited_articles,
        compliance_status=compliance_status,
        hits=hits,
        misses=misses,
        confidence=confidence
    )