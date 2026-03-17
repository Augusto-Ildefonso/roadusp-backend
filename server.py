from flask import Flask, jsonify
from flask_cors import CORS
from src.api.v1.endpoints.cursos import cursos_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(cursos_bp, url_prefix="/api/v1/cursos")

    @app.route("/ping")
    def ping():
        return jsonify({"status": "ok"}), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
