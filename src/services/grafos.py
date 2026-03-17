import src.repositories.cursos_db as curso_bd

def criar_node_link(lista_disciplinas):
    # Construir nodes e links sem consultas N+1:
    nodes = []
    links = []

    if not lista_disciplinas:
        return (nodes, links)

    # Mapas auxiliares
    disciplinas_by_id = {d["id"]: d for d in lista_disciplinas}
    ids_disciplinas = list(disciplinas_by_id.keys())

    # Buscar todos os requisitos de uma vez (onde id_disciplina está na lista)
    requisitos = curso_bd.get_id_requisitos(ids_disciplinas)

    # Coletar todos os ids de disciplinas que aparecem como requisito (para obter códigos)
    ids_requisitos_unicos = list({r["id_requisito"] for r in requisitos}) if requisitos else []

    codigo_by_id = {}
    if ids_requisitos_unicos:
        # Buscar de uma vez os códigos das disciplinas que são pré-requisitos
        disciplinas_requisito = curso_bd.get_requisitos(ids_requisitos_unicos)
        for d in disciplinas_requisito:
            codigo_by_id[d["id"]] = d.get("codigo")

    # Construir nodes
    for disciplina in lista_disciplinas:
        # Determina o grupo com if/elif para evitar sobrescrita
        if disciplina.get("obrigatoria"):
            group = "Obrigatória"
        elif disciplina.get("eletiva"):
            group = "Optativa Eletiva"
        elif disciplina.get("livre"):
            group = "Optativa Livre"
        else:
            group = "Outro"

        elemento_node = {
            "id": disciplina.get("codigo"),
            "group": group,
            "nome": disciplina.get("nome"),
            "semestre": disciplina.get("semestre"),
            "credito_aula": disciplina.get("cred_aula"),
            "credito_trabalho": disciplina.get("cred_trabalho"),
            "carga_horaria": disciplina.get("ch"),
            "carga_horaria_estagio": disciplina.get("ce"),
            "carga_horaria_pratica": disciplina.get("cp"),
            "atividades_teoricos": disciplina.get("atpa"),
        }
        nodes.append(elemento_node)

    # Construir links usando os requisitos carregados
    for r in requisitos:
        id_disciplina = r.get("id_disciplina")
        id_requisito = r.get("id_requisito")
        # Código da disciplina que é requisito (origem)
        codigo_origem = codigo_by_id.get(id_requisito)
        # Código da disciplina alvo
        disciplina_alvo = disciplinas_by_id.get(id_disciplina)
        codigo_alvo = disciplina_alvo.get("codigo") if disciplina_alvo else None

        if codigo_origem and codigo_alvo:
            elemento_link = {
                "source": codigo_origem,
                "target": codigo_alvo,
                "value": 3
            }
            links.append(elemento_link)

    return (nodes, links)