from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# ---------- CONFIGURAÇÃO INICIAL ----------
import os

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(base_dir, "templates"),
    static_folder=os.path.join(base_dir, "static")
)

# ---------- CONFIGURAÇÃO DO BANCO ----------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///biolink.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------- MODELOS ----------
class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    local = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(20), nullable=False)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(150), nullable=False)
    data_nascimento = db.Column(db.String(20), nullable=False)
    tipo_sanguineo = db.Column(db.String(10), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(50), nullable=False)


# ---------- ROTAS DE PÁGINAS ----------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


@app.route("/locais")
def locais():
    return render_template("locais.html")


@app.route("/contato")
def contato():
    return render_template("contato.html")


# ---------- CRUD DE AGENDAMENTOS ----------
@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        local = request.form["local"]
        data = request.form["data"]

        if not nome or not email or not local or not data:
            flash("Preencha todos os campos.")
            return redirect(url_for("agendar"))

        novo = Agendamento(nome=nome, email=email, local=local, data=data)
        db.session.add(novo)
        db.session.commit()
        flash("Agendamento realizado com sucesso!")
        return redirect(url_for("agendamentos"))

    return render_template("agendar.html")


@app.route("/agendamentos")
def agendamentos():
    registros = Agendamento.query.all()
    return render_template("agendamentos.html", agendamentos=registros)


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    agendamento = Agendamento.query.get_or_404(id)

    if request.method == "POST":
        agendamento.nome = request.form["nome"]
        agendamento.email = request.form["email"]
        agendamento.local = request.form["local"]
        agendamento.data = request.form["data"]

        db.session.commit()
        flash("Agendamento atualizado com sucesso!")
        return redirect(url_for("agendamentos"))

    return render_template("editar.html", agendamento=agendamento)


@app.route("/deletar/<int:id>")
def deletar(id):
    agendamento = Agendamento.query.get_or_404(id)
    db.session.delete(agendamento)
    db.session.commit()
    flash("Agendamento excluído com sucesso!")
    return redirect(url_for("agendamentos"))


# ---------- CRUD DE USUÁRIOS ----------
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nome = request.form['nomeForm']
        telefone = request.form['telefoneForm']
        email = request.form['emailForm']
        endereco = request.form['enderecoForm']
        data_nascimento = request.form['dataDeNascimentoForm']
        tipo_sanguineo = request.form['tiposanguineoform']
        senha = request.form['senhaForm']
        cidade = request.form['cidade']

        if not nome or not email:
            flash("Preencha todos os campos obrigatórios.")
            return redirect(url_for('registrar'))

        novo_usuario = Usuario(
            nome=nome,
            telefone=telefone,
            email=email,
            endereco=endereco,
            data_nascimento=data_nascimento,
            tipo_sanguineo=tipo_sanguineo,
            senha=senha,
            cidade=cidade
        )

        db.session.add(novo_usuario)
        db.session.commit()
        flash("Usuário registrado com sucesso!")
        return redirect(url_for('usuarios'))

    return render_template('registrar.html')


@app.route('/usuarios')
def usuarios():
    lista = Usuario.query.all()
    return render_template('usuarios.html', usuarios=lista)


@app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.telefone = request.form['telefone']
        usuario.email = request.form['email']
        usuario.cidade = request.form['cidade']
        usuario.tipo_sanguineo = request.form['tipo_sanguineo']
        db.session.commit()
        flash("Usuário atualizado com sucesso!")
        return redirect(url_for('usuarios'))

    return render_template('editar_usuario.html', usuario=usuario)


@app.route('/deletar_usuario/<int:id>')
def deletar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash("Usuário excluído com sucesso!")
    return redirect(url_for('usuarios'))


# ---------- EXECUÇÃO ----------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
