from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Exemplo de modelo para alunos
class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nome = db.Column(db.String(120), nullable=False)
