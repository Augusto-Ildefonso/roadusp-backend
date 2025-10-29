from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv
import json
import os

# Load enviroment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Create supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/ping")
def ping():
    return jsonify({"status": "ok", "message": "Server is awake"}), 200

@app.route("/listacursos")
def lista_cursos():
    try:
        unidade_escolhida = request.args.get("unidade")
        print(unidade_escolhida)
        
        id_unidade = (supabase.table("unidades").select("id").eq("nome", unidade_escolhida).maybe_single().execute().data)["id"]
        
        cursos_db = (supabase.table("cursos").select("nome").eq("id_unidade", id_unidade).execute().data)

        lista_cursos = [curso["nome"] for curso in cursos_db]

        if cursos_db:
            return jsonify({"cursos": lista_cursos}), 200
        else:
            return jsonify({"error": "não foi encontrado nenhum curso"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
    try:
        requisitos = supabase.table("requisitos").select("id_disciplina, id_requisito").in_("id_disciplina", ids_disciplinas).execute().data
    except Exception:
        # Fallback para evitar quebra caso cliente supabase não suporte in_
        requisitos = []
        for d_id in ids_disciplinas:
            r = supabase.table("requisitos").select("id_disciplina, id_requisito").eq("id_disciplina", d_id).execute().data
            requisitos.extend(r)

    # Coletar todos os ids de disciplinas que aparecem como requisito (para obter códigos)
    ids_requisitos_unicos = list({r["id_requisito"] for r in requisitos}) if requisitos else []

    codigo_by_id = {}
    if ids_requisitos_unicos:
        # Buscar de uma vez os códigos das disciplinas que são pré-requisitos
        disciplinas_requisito = supabase.table("disciplinas").select("id, codigo").in_("id", ids_requisitos_unicos).execute().data
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

@app.route("/disciplinas")
def get_disciplinas():
    try:
        req_unidade = request.args.get("unidade")
        req_curso = request.args.get("curso")
        
        # Id da unidade
        print(f"Unidade a ser buscada: {req_unidade}")
        id_unidade = (supabase.table("unidades").select("id").eq("nome", req_unidade).maybe_single().execute().data)["id"]
        print(f"ID_UNIDADE: {id_unidade}")
        
        # Id do curso
        print(f"Curso a ser buscado: {req_curso}")
        id_curso = (supabase.table("cursos").select("id").eq("id_unidade", id_unidade).eq("nome", req_curso).maybe_single().execute().data)["id"]
        print(f"ID_CURSO: {id_curso}")

        # Lista das disciplinas do curso
        disciplinas_curso = (supabase.table("disciplinas").select("*").eq("id_curso", id_curso).execute().data)
        print(f"Disciplinas:\n{disciplinas_curso}")
        
        nodes, links = criar_node_link(disciplinas_curso)
        
        return jsonify({"nodes": nodes, "links": links}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
