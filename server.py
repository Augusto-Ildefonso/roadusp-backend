from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)

CORS(app)

@app.route("/listacursos")
def lista_cursos():
    try:
        unidade_http = request.args.get("unidade")

        file = open("dados.json", 'r', encoding='utf-8')
        data = json.load(file)
        file.close()

        unidade = data[unidade_http]

        cursos = [curso["nome"] for curso in unidade["cursos"]]

        if unidade:
            return jsonify({"cursos": cursos}), 200
        else:
            return jsonify({"error": "não foi encontrado nenhum curso"}), 500
    except Exception as e:
        return jsonify({"error": e}), 500

@app.route("/disciplinas")
def get_disciplinas():
    try:
        unidade_http = request.args.get("unidade")
        curso_http = request.args.get("curso")

        print(f"Unidade a ser buscada: {unidade_http}")
        print(f"Curso a ser buscado: {curso_http}")

        file = open("dados.json", 'r', encoding='utf-8')
        data = json.load(file)
        file.close()

        nodes = []        
        links = []

        unidade = data[unidade_http]
        lista_cursos = unidade["cursos"]

        for curso in lista_cursos:
            if curso["nome"] == curso_http:
                lista_disciplinas = curso["disciplinas_obrigatorias"] + curso["disciplinas_optativas_eletivas"] + curso["disciplinas_optativas_livres"]
                lista_codigos_disciplinas = []

                for disciplina in lista_disciplinas:
                    lista_codigos_disciplinas.append(disciplina["codigo"])
                    elemento_node = {
                        "id": disciplina["codigo"],
                        "group": 1 if not disciplina["requisitos"] else 2,
                        "nome": disciplina["nome"],
                        "credito_aula": disciplina["credito_aula"],
                        "credito_trabalho": disciplina["credito_trabalho"],
                        "carga_horaria": disciplina["carga_horaria"],
                        "carga_horaria_estagio": disciplina["carga_horaria_estagio"],
                        "carga_horaria_pratica": disciplina["carga_horaria_pratica"],
                        "atividades_teoricos": disciplina["atividades_teo"]
                    }
                    nodes.append(elemento_node)

                    for requisito in disciplina["requisitos"]:
                        if requisito in lista_codigos_disciplinas:
                            elemento_link = {}
                            elemento_link["source"] = requisito
                            elemento_link["target"] = disciplina["codigo"]
                            elemento_link["value"] = 3

                        links.append(elemento_link)

                break

        return jsonify({"nodes": nodes, "links": links}), 200

    except Exception as e:
        return jsonify({"error": e}), 500
    
    """
    nodes: [
            { id: 'SCC0956', group: 1 },
            { id: 'SSC1234', group: 3 },
            { id: 'SMA7452', group: 2 }
        ],
        links: [
            { source: 'SCC0956', target: 'SSC1234', value: 1 },
            { source: 'SSC1234', target: 'SMA7452', value: 2 },
            { source: 'SMA7452', target: 'SCC0956', value: 3}
        ]
    """