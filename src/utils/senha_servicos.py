from werkzeug.security import generate_password_hash, check_password_hash

def encriptar(senha):
    return generate_password_hash(senha, method='pbkdf2:sha256')

def check_senha(hash_db, senha_req):
    if check_password_hash(hash_db, senha_req):
        return True
    else:
        return False