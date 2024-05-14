import sqlite3


class Palestra:
    def __init__(self, id, nome, hora, local, desc):
        self.id = id
        self.nome = nome
        self.hora = hora
        self.local = local
        self.desc = desc


class Palestrante:
    def __init__(self, id, nome, bio, area, imagem):
        self.id = id
        self.nome = nome
        self.bio = bio
        self.area = area
        self.imagem = imagem


def carregarObjetos():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM palestras")
    palestras = c.fetchall()
    c.execute("SELECT * FROM palestrantes")
    palestrantes = c.fetchall()

    conn.commit()
    conn.close()

    palestras_lista = []
    palestrantes_lista = []

    for palestra in palestras:
        id, nome, local, hora, desc = palestra
        obj_palestra = Palestra(id, nome, hora, local, desc)
        palestras_lista.append(obj_palestra)

    for palestrante in palestrantes:
        id, nome, bio, area, imagem = palestrante
        imagem = palestrante[4][7:]
        obj_palestrante = Palestrante(id, nome, bio, area, imagem)
        palestrantes_lista.append(obj_palestrante)

    return palestrantes_lista, palestras_lista
