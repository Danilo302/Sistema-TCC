from flask import Flask, redirect
from app.routes.auth import auth_bp
from app.routes.aluno import aluno_bp
from app.routes.secretaria import secretaria_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # Substitua por uma chave segura

    # Registro dos blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(aluno_bp)
    app.register_blueprint(secretaria_bp)
    
    @app.route('/')
    def index():
        return redirect('/auth/login')

    return app
