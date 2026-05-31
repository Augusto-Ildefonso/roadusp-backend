import io
import re
import pdfplumber

CODIGO_RE = re.compile(r'^[A-Z]{3}\d{4}$|^\d{7}$')
UNIDADE_RE = re.compile(r'Unidade:\s*(.+)')
CURSO_RE = re.compile(r'Curso:\s*(?:\d+/\d+\s*-\s*)?(.+)')
STATUS_APROVADO = "A"
STATUS_CURSANDO = "MA"


def extracao_materias(arquivo: io.IOBase) -> dict:
    aprovadas = []
    cursando = []
    unidade = None
    curso = None

    with pdfplumber.open(arquivo) as pdf:
        for i, pagina in enumerate(pdf.pages):
            texto = pagina.extract_text()
            if i == 0 and texto:
                if not unidade:
                    m = UNIDADE_RE.search(texto)
                    if m:
                        unidade = m.group(1).strip()
                if not curso:
                    m = CURSO_RE.search(texto)
                    if m:
                        curso = m.group(1).strip()

            tabela = pagina.extract_table()
            if not tabela:
                continue

            for linha in tabela:
                linha_limpa = [
                    celula.replace("\n", " ").strip() if celula else ""
                    for celula in linha
                ]

                codigo = linha_limpa[0]
                if not CODIGO_RE.match(codigo):
                    continue

                status = _extrair_status(linha_limpa)
                if not status:
                    continue

                if status == STATUS_APROVADO:
                    aprovadas.append(codigo)
                elif status == STATUS_CURSANDO:
                    cursando.append(codigo)

    return {
        "aprovadas": aprovadas,
        "cursando": cursando,
        "unidade": unidade,
        "curso": curso,
    }


def _extrair_status(linha: list) -> str | None:
    ultimo = linha[-1]
    if not ultimo:
        return None
    palavras = ultimo.split()
    status = palavras[-1]
    if status in (STATUS_APROVADO, STATUS_CURSANDO):
        return status
    return None
