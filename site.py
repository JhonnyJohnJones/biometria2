from flask import Flask
from flask import render_template
from flask import request
import os
import json

from biometria import auth, authDirect

app = Flask(__name__, template_folder='template')

@app.route("/")
def homepage():
    return render_template("main.html")

@app.route("/salvar", methods=["GET", "POST"])
def salvar():
    if request.method == "POST":
        nome = request.form.get("nome").strip()
        nivel = int(request.form.get("nivel"))
        digital = request.files["digital"]
        js = open("static/users.json", "r")
        usrs = json.loads(js.read())
        print(usrs)
        js.close()
        for user in usrs["users"]:
            try:
                if user["nome"] == nome:
                    return "Nome já usado"
            except:
                break
        for user in usrs["users"]:
            try:
                if user["digital"] == digital.filename:
                    return "Renomeie o arquivo"
            except:
                break
        digital.save(f"static/temp/{digital.filename}")
        print(f"Auth: {auth(digital.filename)}")
        if not auth(digital.filename):
            js = open("static/users.json", "w")
            usrs["users"].append({"nome": nome, "digital": digital.filename, "nivel": nivel})
            js.write(json.dumps(usrs))
            js.close()
            os.rename(f"static/temp/{digital.filename}", f"static/saved/{digital.filename}")
            return "Salvo"
        else:
            os.remove(f"static/temp/{digital.filename}")
            return "Erro"
    if request.method == "GET":
        return render_template("salvar.html")
        

@app.route("/autenticar", methods=["GET", "POST"])
def autenticar():
    if request.method == "POST":
        nome = request.form.get("nome").strip()
        digital = request.files["digital"]
        digital.save(f"static/temp/{digital.filename}")
        js = open("static/users.json", "r")
        usrs = json.loads(js.read())
        nivel = 1
        js.close()
        if authDirect(digital.filename, nome):
            for user in usrs["users"]:
                if user["nome"] == nome:
                    nivel = user["nivel"]
                    break
            os.remove(f"static/temp/{digital.filename}")
            return render_template("autenticado.html", nome=nome, nivel=nivel, digital=user["digital"])
        else:
            os.remove(f"static/temp/{digital.filename}")
            return "Não te conheço"
    if request.method == "GET":
        return render_template("autenticar.html")



if __name__ == "__main__":
    app.run() # type: ignore