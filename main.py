from flask import Flask, url_for, render_template
import json
import sys

# inicializaçaõ
app = Flask(__name__)


# rotas

@app.route('/')
def principal():
    return render_template('index.html')

@app.route('/etapa1')
def sobre1():
    titulo= "Catalogo"

    try:
        with open('catalogo.json', 'r') as file:
            catalogo = json.load(file)
    except Exception as e:
        print(str(e))
    return render_template('etapa1.html', titulo = titulo, catalogo = catalogo)

@app.route('/etapa2')
def sobre2():
    return render_template('etapa2.html')

@app.route('/etapa3')
def sobre3():
    return render_template('etapa3.html')

#exemplo no navegador
#http://localhost:5000/paginaEDII


#execução
app.run(debug = True)