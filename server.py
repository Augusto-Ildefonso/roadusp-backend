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
        return jsonify({"error": str(e)}), 500

def criar_node_link(lista_disciplinas, tipo):
    nodes = []
    links = []
    lista_codigos_disciplinas = []
    group: int
    
    match tipo:
        case "obrigatoria":
            group = 1
        case "eletiva":
            group = 2
        case "livre":
            group = 3
    
    for disciplina in lista_disciplinas:
        lista_codigos_disciplinas.append(disciplina["codigo"])
        elemento_node = {
            "id": disciplina["codigo"],
            "group": group,
            "nome": disciplina["nome"],
            "credito_aula": disciplina["credito_aula"],
            "credito_trabalho": disciplina["credito_trabalho"],
            "carga_horaria": disciplina["carga_horaria"],
            "carga_horaria_estagio": disciplina["carga_horaria_estagio"],
            "carga_horaria_pratica": disciplina["carga_horaria_pratica"],
            "atividades_teoricos": disciplina["atividades_teo"]
        }
        nodes.append(elemento_node)
        
        # Correção: movido o loop de requisitos para dentro do loop de disciplinas
        for requisito in disciplina["requisitos"]:
            if requisito in lista_codigos_disciplinas:
                elemento_link = {
                    "source": requisito,
                    "target": disciplina["codigo"],
                    "value": 3
                }
                links.append(elemento_link)
    
    return (nodes, links)

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
                disciplinas_obrigatorias = criar_node_link(curso["disciplinas_obrigatorias"], "obrigatoria")
                disciplinas_eletivas = criar_node_link(curso["disciplinas_optativas_eletivas"], "eletiva")
                disciplinas_livres = criar_node_link(curso["disciplinas_optativas_livres"], "livre")
                
                nodes.extend(disciplinas_obrigatorias[0])
                nodes.extend(disciplinas_eletivas[0])
                nodes.extend(disciplinas_livres[0])
                
                links.extend(disciplinas_obrigatorias[1])
                links.extend(disciplinas_eletivas[1])
                links.extend(disciplinas_livres[1])
                break
        
        return jsonify({"nodes": nodes, "links": links}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)