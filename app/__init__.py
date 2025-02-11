from flask import Flask, redirect
from app.routes.auth import auth_bp
from app.routes.aluno import aluno_bp
from app.routes.secretaria import secretaria_bp
from app.routes.gerador_documento import document_bp
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY')

    app.register_blueprint(auth_bp)
    app.register_blueprint(aluno_bp)
    app.register_blueprint(secretaria_bp)
    app.register_blueprint(document_bp)
    
    @app.route('/')
    def index():
        return redirect('/auth/login')

    return app
