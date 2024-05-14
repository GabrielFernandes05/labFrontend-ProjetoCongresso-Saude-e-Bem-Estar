from flask import Flask, render_template, request, send_from_directory, redirect
from palestrantes import carregarObjetos
import sqlite3
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/img"


@app.route("/")
def home():
    palestrantes_lista, palestras_lista = carregarObjetos()
    return render_template(
        "home.html",
        palestrantes_lista=palestrantes_lista,
        palestras_lista=palestras_lista,
    )


@app.route("/cad_palestra", methods=["GET", "POST"])
def cadastro_palestra():
    if request.method == "POST":
        nome = request.form.get("nome").title()
        local = request.form.get("local")
        dia = request.form.get("dia")
        hora = request.form.get("hora")
        desc = request.form.get("desc")
        # nome = nome.title()
        print(nome)
        hora = f"{dia}-{hora}"
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            """
INSERT INTO palestras (nome, local, hora, desc)
VALUES (?, ?, ?, ?);
""",
            (nome, local, hora, desc),
        )
        conn.commit()
        conn.close()
    return render_template("cadastro_palestra.html")


@app.route("/cad_palestrante", methods=["GET", "POST"])
def cadastro_palestrante():
    if request.method == "POST":
        nome = request.form.get("nome").title()
        bio = request.form.get("bio")
        area = request.form.get("area")
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            """
INSERT INTO palestrantes (nome, bio, area)
VALUES (?, ?, ?);
""",
            (nome, bio, area),
        )
        id = c.lastrowid
        imagem = request.files["imagem"]
        imagem.save(os.path.join(app.config["UPLOAD_FOLDER"], str(id) + ".png"))
        c.execute(
            "UPDATE palestrantes SET imagem = ? WHERE id = ?",
            (os.path.join(app.config["UPLOAD_FOLDER"], str(id) + ".png"), id),
        )
        conn.commit()
        conn.close()
    return render_template("cadastro_palestrante.html")


@app.route("/palestrante/<id>")
def detalhes_palestrante(id):
    palestrantes_lista, palestras_lista = carregarObjetos()
    for palestrante in palestrantes_lista:
        if str(palestrante.id) == str(id):
            return render_template("detalhes_palestrante.html", palestrante=palestrante)


@app.route("/palestra/<id>")
def detalhes_palestra(id):
    palestrantes_lista, palestras_lista = carregarObjetos()
    for palestra in palestras_lista:
        if str(palestra.id) == str(id):
            return render_template("detalhes_palestra.html", palestra=palestra)


@app.route("/del_palestrante/<id>")
def deletar_palestrante(id):
    palestrantes_lista, palestras_lista = carregarObjetos()
    for palestrante in palestrantes_lista:
        if str(palestrante.id) == str(id):
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute(
                """
                DELETE FROM `palestrantes` WHERE id=?
    """,
                (id,),
            )
            conn.commit()
            conn.close()
            print(f"{palestrante.id}:{palestrante.nome} - Deletado com sucesso!")
            return redirect("/")
    return redirect("/")


@app.route("/del_palestra/<id>")
def deletar_palestra(id):
    palestras_lista, palestras_lista = carregarObjetos()
    for palestra in palestras_lista:
        if str(palestra.id) == str(id):
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute(
                """
                DELETE FROM `palestras` WHERE id=?
    """,
                (id,),
            )
            conn.commit()
            conn.close()
            print(f"{palestra.id}:{palestra.nome} - Deletado com sucesso!")
            return redirect("/")
    return redirect("/")


@app.route("/imagens_palestrantes/<id>.png")
def imagem_palestrante(id):
    return send_from_directory(app.config["UPLOAD_FOLDER"], id + ".png")


if __name__ == "__main__":
    app.run(debug=True)
