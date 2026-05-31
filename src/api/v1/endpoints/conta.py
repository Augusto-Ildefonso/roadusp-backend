from flask import Blueprint, request, jsonify
from src.utils.senha_servicos import encriptar, check_senha
from src.repositories import usuarios_db, processamento_db, preferencias_db, historico_db
from src.services import processamento
from postgrest.exceptions import APIError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

conta_bp = Blueprint("conta", __name__)

@conta_bp.route("/criar", methods=["POST"])
def criar_conta():
    payload = request.get_json(silent=True) or {}
    email = payload.get("email")
    senha = payload.get("senha")

    if not email or not senha:
        return jsonify({"message": "Erro: email ou senha não foram recebidos"}), 400

    hash = encriptar(senha)

    try:
        response = usuarios_db.criar(email, hash)
    except APIError as e: # Já existe essa conta
        print(e)
        return jsonify({"code": e.code, "details": "Já existe essa usuário com esse email."}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": "Houve um erro na base de dados."}), 400
    
    print(response.data)
    
    if not response:
        return jsonify({"message": "Erro ao criar conta"}), 400

    return jsonify({"message": "Conta criada com sucesso"}), 201

@conta_bp.route("/login", methods=["POST"])
def login_conta():
    payload = request.get_json(silent=True) or {}
    email = payload.get("email")
    senha = payload.get("senha")

    if not email or not senha:
        return jsonify({"message": "Erro: email ou senha não foram recebidos"}), 400

    user_db = usuarios_db.busca_user(email)
    user_db_senha = user_db["senha"]
    user_db_id = user_db["id"]
    
    if check_senha(user_db_senha, senha):
        return jsonify({"message": "Login efetuado com sucesso", "token": create_access_token(identity=str(user_db_id))}), 200
    else:
        return jsonify({"error": "O email ou senha estão incorretors"}), 400

@conta_bp.route("/deletar", methods=["DELETE"])
@jwt_required()
def deletar_conta():
    payload = request.get_json()
    email = payload.get("email")

    if not email:
        return jsonify({"message": "Erro: email ou senha não foram recebidos"}), 400

    response = usuarios_db.deletar_user(email)


    if response.ok:
        return({"message": "Usuário deletado com sucesso"}), 200
    else:
        return({"error": "Houve um erro ao deletar o usuário", "info": response.error}), 500

@conta_bp.route("/alterar", methods=["UPDATE"])
@jwt_required()
def alterar_senha():
    payload = request.get_json()
    email = payload.get("email")
    senha_antiga = payload.get("senha_antiga")
    nova_senha = payload.get("nova_senha")

    if not email or not senha_antiga or not nova_senha:
        return jsonify({"message": "Erro: email ou senha não foram recebidos"}), 400

    user_db_response = usuarios_db.busca_user(email)

    if user_db_response.ok:
        user_db_senha = user_db_response["senha"]
        user_db_id = user_db_response["id"]
        
        if check_senha(user_db_senha, senha_antiga):
            hash = encriptar(nova_senha)
            response = usuarios_db.alterar_senha(email, hash)

            if response.ok:
                return jsonify({"message": "Senha alterada com sucesso"}), 200
            else:
                return jsonify({"error": "Houve um erro ao alterar a senha", "info": response.error}), 500

@conta_bp.route("/upload/historico", methods=["POST"])
@jwt_required()
def upload_historico():
    user_id = get_jwt_identity()

    if "arquivo" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado."}), 400

    arquivo = request.files["arquivo"]

    if arquivo.filename == "":
        return jsonify({"error": "Nenhum arquivo selecionado."}), 400

    arquivo_bytes = arquivo.read()
    processamento_id = processamento.iniciar_processamento(user_id, arquivo_bytes)

    return jsonify({
        "processamento_id": processamento_id,
        "status": "processando",
    }), 202


@conta_bp.route("/processamento/<processamento_id>", methods=["GET"])
@jwt_required()
def status_processamento(processamento_id):
    user_id = get_jwt_identity()
    dados = processamento_db.buscar(processamento_id)

    if not dados:
        return jsonify({"error": "Processamento não encontrado."}), 404

    if dados["id_usuario"] != user_id:
        return jsonify({"error": "Acesso negado."}), 403

    return jsonify({
        "processamento_id": dados["id"],
        "status": dados["status"],
        "resultado": dados.get("resultado"),
        "erro": dados.get("erro"),
    }), 200


@conta_bp.route("/historico", methods=["GET"])
@jwt_required()
def get_historico():
    user_id = get_jwt_identity()
    disciplinas = historico_db.buscar_historico(user_id)
    aprovadas = [d["codigo_disciplina"] for d in disciplinas if d["status"] == "aprovada"]
    cursando = [d["codigo_disciplina"] for d in disciplinas if d["status"] == "cursando"]
    return jsonify({"aprovadas": aprovadas, "cursando": cursando}), 200


@conta_bp.route("/preferencias", methods=["GET"])
@jwt_required()
def get_preferencias():
    user_id = get_jwt_identity()
    prefs = preferencias_db.buscar(user_id)
    if prefs:
        return jsonify({"unidade": prefs.get("unidade"), "curso": prefs.get("curso")}), 200
    return jsonify({"unidade": None, "curso": None}), 200


@conta_bp.route("/preferencias", methods=["PATCH"])
@jwt_required()
def set_preferencias():
    user_id = get_jwt_identity()
    payload = request.get_json(silent=True) or {}
    unidade = payload.get("unidade")
    curso = payload.get("curso")

    preferencias_db.salvar(user_id, unidade, curso)
    return jsonify({"message": "Preferências salvas com sucesso"}), 200