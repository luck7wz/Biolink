from db import db


class Contato(db.Model):
    tablename = 'contatos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)  # ← alterado para String
    email = db.Column(db.String(100))
    tiposanguineo = db.Column(db.String(5))
    endereco = db.Column(db.String(200))
    data_de_nascimento = db.Column(db.Date)
    senha = db.Column(db.String(100))


def repr(self):
    return f"<Contato {self.nome}>"