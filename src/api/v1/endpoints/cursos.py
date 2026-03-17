from flask import Blueprint, request, jsonify
import src.repositories.cursos_db as curso_db
import src.services.grafos as grafo

cursos_bp = Blueprint("cursos", __name__, url_prefix="/cursos")

@cursos_bp.route("/lista")
def lista_cursos():
    try:
        unidade_escolhida = request.args.get("unidade")
        print(unidade_escolhida)

        id_unidade = curso_db.get_id_unidade(unidade_escolhida)
        
        lista_cursos = curso_db.get_cursos(id_unidade)

        if lista_cursos:
            return jsonify({"cursos": lista_cursos}), 200
        else:
            return jsonify({"error": "não foi encontrado nenhum curso"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@cursos_bp.route("/disciplinas")
def get_disciplinas():
    try:
        req_unidade = request.args.get("unidade")
        req_curso = request.args.get("curso")
        
        # Id da unidade
        print(f"Unidade a ser buscada: {req_unidade}")
        id_unidade = curso_db.get_id_unidade(req_unidade)
        print(f"ID_UNIDADE: {id_unidade}")
        
        # Id do curso
        print(f"Curso a ser buscado: {req_curso}")
        id_curso = curso_db.get_id_curso(id_unidade, req_curso)
        print(f"ID_CURSO: {id_curso}")

        # Lista das disciplinas do curso
        disciplinas_curso = curso_db.get_disciplinas(id_curso)
        print(f"Disciplinas:\n{disciplinas_curso}")
        
        nodes, links = grafo.criar_node_link(disciplinas_curso)
        
        return jsonify({"nodes": nodes, "links": links}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500