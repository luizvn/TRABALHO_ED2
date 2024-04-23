from flask import Flask, url_for, render_template, request, jsonify
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

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        with open('catalogo.json', 'r') as file:
            catalogo = json.load(file)
    except Exception as e:
        print(str(e))
    
    categoria = request.form['categoria']
    marca = request.form['marca']
    cor = request.form['cor']

    output = []

    for produto in catalogo:
        if categoria in produto['categoria']:
            if marca in produto['marca']:
                if cor in produto['cor']:
                    output.append(produto)
                elif cor == '':
                    output.append(produto)
            elif marca == '':
                if cor in produto['cor']:
                    output.append(produto)
        else:
            if categoria == '':
                if marca in produto['marca']:
                    if cor in produto['cor']:
                        output.append(produto)
                    elif cor == '':
                        output.append(produto)
                elif marca == '':
                    if cor in produto['cor']:
                        output.append(produto)

    return render_template('etapa1.html', catalogo = output)



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