from flask import Flask, jsonify
from flask_cors import CORS
from src.api.v1.endpoints.cursos import cursos_bp
from src.api.v1.endpoints.conta import conta_bp
from src.core.config import settings
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = settings.JWT_SECRET_KEY
    CORS(app)

    app.register_blueprint(cursos_bp, url_prefix="/api/v1/cursos")
    app.register_blueprint(conta_bp, url_prefix="/api/v1/conta")

    @app.route("/ping")
    def ping():
        return jsonify({"status": "ok"}), 200
    
    jwt.init_app(app)

    return app

app = create_app()


# Expose WSGI application for Gunicorn (`server:app`).
app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
