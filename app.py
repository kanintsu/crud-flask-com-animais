import sqlite3
from flask import Flask, render_template, redirect, request


app = Flask(__name__)

def criar_tabela():
    conexao = sqlite3.connect("animal.db")
    cursor = conexao.cursor()

    cursor.execute("""
CREATE TABLE IF NOT EXISTS animais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    raca TEXT,
    habilidade TEXT) """)

    conexao.commit()
    conexao.close()

criar_tabela()

@app.route("/", methods=["POST", "GET"])
def index():
    conexao = sqlite3.connect("animal.db")
    cursor = conexao.cursor()
    if "nome" in request.form:
        nome = request.form["nome"]
        raca = request.form["raca"]
        habilidade = request.form["habilidade"]
        cursor.execute("INSERT INTO animais (nome, raca, habilidade) VALUES (?, ?, ?)", (nome, raca, habilidade))
        conexao.commit()

    cursor.execute("SELECT * FROM animais")
    dados = cursor.fetchall()
    animais = dados
    return render_template("index.html", animais=animais)

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    conexao = sqlite3.connect("animal.db")
    cursor = conexao.cursor()

    novo_nome = request.form["nome"]
    nova_raca = request.form["raca"]
    nova_habilidade = request.form["habilidade"]
    
    cursor.execute("UPDATE animais SET nome = ?, raca = ?, habilidade = ? WHERE id = ?", (novo_nome, nova_raca, nova_habilidade))
    conexao.commit()
    conexao.close()
    return redirect("/")

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conexao = sqlite3.connect("animal.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM animais WHERE id = ?", (id, ))
    conexao.commit()
    conexao.close()
    return redirect("/")

app.run(debug=True)

