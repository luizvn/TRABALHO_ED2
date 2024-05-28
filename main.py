from flask import Flask, url_for, render_template, request, jsonify, send_file
import json
import sys
import gzip
from io import BytesIO
import arvoreB # Arvore B

# inicializaçaõ
app = Flask(__name__, static_folder='src')



@app.route('/')
def principal():
    return render_template('index.html')

@app.route('/etapa1')
def sobre1():
    titulo= "Catálogo"

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

    output = {}

    for produto,detalhes in catalogo.items():
        if (not categoria or detalhes['categoria'] == categoria) and \
           (not marca or detalhes['marca'] == marca) and \
           (not cor or detalhes['cor'] == cor):
            output[produto] = detalhes

    return render_template('etapa1.html', catalogo = output)

@app.route('/inserir', methods=['POST'])
def inserir():
    try:
        with open('catalogo.json', 'r') as file:
            catalogo = json.load(file)
    except Exception as e:
        print(str(e))

    nova_chave = str(max(int(k) for k in catalogo.keys()) + 1)
    
    categoria = request.form['categoria']
    tipo      = request.form['tipo']
    marca     = request.form['marca']
    modelo    = request.form['modelo']
    cor       = request.form['cor']
    valor     = request.form['valor']
    estoque   = request.form['estoque']
    tamanhos_disponiveis = ['tamanho unico']

    catalogo[nova_chave] = {'categoria':categoria, 'tipo':tipo, 'marca':marca, 'modelo':modelo, 'cor':cor, 'valor':valor, 'estoque':estoque, 'tamanhos_disponiveis':tamanhos_disponiveis}


   # output.append(categoria, tipo, marca, modelo, cor, valor, estoque, tamanhos_disponiveis)

    try:
        with open('catalogo.json', 'w', encoding="utf-8") as arquivo:
            json.dump(catalogo, arquivo)
    except Exception as e:
        print(str(e))

    return render_template('etapa1.html', catalogo = catalogo)

@app.route('/deletar', methods=['POST'])
def deletar():

    try:
        with open('catalogo.json', 'r') as file:
            catalogo = json.load(file)
    except Exception as e:
        print(str(e))

    id = request.form['id']

    if id in catalogo.keys():
        removido = catalogo.pop(id)
    print(removido)
    try:
        with open('catalogo.json', 'w', encoding="utf-8") as arquivo:
            json.dump(catalogo, arquivo)
    except Exception as e:
        print(str(e))

    return render_template('etapa1.html', catalogo = catalogo)

@app.route('/editar', methods=['POST'])
def editar():
    try:
        with open('catalogo.json', 'r') as file:
            catalogo = json.load(file)
    except Exception as e:
        print(str(e))
    
    id        = request.form['id']
    categoria = request.form['categoria']
    tipo      = request.form['tipo']
    marca     = request.form['marca']
    modelo    = request.form['modelo']
    cor       = request.form['cor']
    valor     = request.form['valor']
    estoque   = request.form['estoque']
    tamanhos_disponiveis = ['tamanho unico']

    if id in catalogo:
        existe = True
    else:
        existe = False

    if existe == True:
        for produto,detalhes in catalogo.items():
            if produto == id:
                if (not categoria):
                    pass
                else:
                    detalhes['categoria'] = categoria

                if(not tipo):
                    pass
                else:
                    detalhes['tipo'] = tipo

                if(not marca):
                    pass
                else:
                    detalhes['marca'] = marca

                if(not modelo):
                    pass
                else:
                    detalhes['modelo'] = modelo

                if(not cor):
                    pass
                else:
                    detalhes['cor'] = cor

                if(not valor):
                    pass
                else:
                    detalhes['valor'] = valor

                if(not estoque):
                    pass
                else:
                    detalhes['estoque'] = estoque

                if(not tamanhos_disponiveis):
                    pass
                else:
                    detalhes['tamanhos_disponiveis'] = tamanhos_disponiveis
            
    try:
        with open('catalogo.json', 'w', encoding="utf-8") as arquivo:
            json.dump(catalogo, arquivo)
    except Exception as e:
        print(str(e))

    return render_template('etapa1.html', catalogo = catalogo)

@app.route('/download', methods=['GET'])
def download():
    try:
        with open('catalogo.json', 'r') as file:
            catalogo = json.load(file)
    except Exception as e:
        print(str(e))
    
    # Comprimindo os dados JSON
    catalogo_comprimido = compress_json(catalogo)

    # Criando um arquivo de memória para armazenar os dados comprimidos
    compressed_file = BytesIO()
    compressed_file.write(catalogo_comprimido)
    compressed_file.seek(0)

    # Enviando o arquivo comprimido para o cliente como uma resposta de download
    return send_file(compressed_file, as_attachment=True, download_name='catalogo.json.gz')

def compress_json(json_data):
    # Comprimindo os dados JSON
    with BytesIO() as compressed_file:
        with gzip.GzipFile(fileobj=compressed_file, mode='wb') as f:
            json_str = json.dumps(json_data)
            f.write(json_str.encode('utf-8'))
        return compressed_file.getvalue()


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