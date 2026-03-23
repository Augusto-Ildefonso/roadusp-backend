from flask import Blueprint, request, jsonify
from src.utils.senha_servicos import encriptar, check_senha
from src.repositories import usuarios_db
from postgrest.exceptions import APIError
from flask_jwt_extended import create_access_token, jwt_required

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
            response = usuarios_db.alterar_senha(email, nova_senha)

            if response.ok:
                return jsonify({"message": "Senha alterada com sucesso"}), 200
            else:
                return jsonify({"error": "Houve um erro ao alterar a senha", "info": response.error}), 500

@conta_bp.route("/upload/historico")
@jwt_required()
def upload_historico():
    