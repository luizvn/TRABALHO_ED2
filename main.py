from flask import Flask, url_for, render_template, request, jsonify, send_file
import json
import sys
import gzip
from io import BytesIO
import arvoreB as ab  # Arvore B
import folium
import igraph
import os

# inicializaçaõ
app = Flask(__name__, static_folder='src')


@app.route('/')
def principal():
    return render_template('index.html')


@app.route('/etapa1')
def sobre1():
    titulo = "Catálogo"

    try:
        with open('catalogo.json', 'r') as file:
            catalogo = json.load(file)
    except Exception as e:
        print(str(e))
    return render_template('etapa1.html', titulo=titulo, catalogo=catalogo)


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

    for produto, detalhes in catalogo.items():
        if (not categoria or detalhes['categoria'] == categoria) and \
           (not marca or detalhes['marca'] == marca) and \
           (not cor or detalhes['cor'] == cor):
            output[produto] = detalhes

    return render_template('etapa1.html', catalogo=output)


@app.route('/inserir', methods=['POST'])
def inserir():
    try:
        with open('catalogo.json', 'r') as file:
            catalogo = json.load(file)
    except Exception as e:
        print(str(e))

    nova_chave = str(max(int(k) for k in catalogo.keys()) + 1)

    categoria = request.form['categoria']
    tipo = request.form['tipo']
    marca = request.form['marca']
    modelo = request.form['modelo']
    cor = request.form['cor']
    valor = request.form['valor']
    estoque = request.form['estoque']
    tamanhos_disponiveis = ['tamanho unico']

    catalogo[nova_chave] = {'categoria': categoria, 'tipo': tipo, 'marca': marca, 'modelo': modelo,
                            'cor': cor, 'valor': valor, 'estoque': estoque, 'tamanhos_disponiveis': tamanhos_disponiveis}

   # output.append(categoria, tipo, marca, modelo, cor, valor, estoque, tamanhos_disponiveis)

    try:
        with open('catalogo.json', 'w', encoding="utf-8") as arquivo:
            json.dump(catalogo, arquivo)
    except Exception as e:
        print(str(e))

    return render_template('etapa1.html', catalogo=catalogo)


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

    return render_template('etapa1.html', catalogo=catalogo)


@app.route('/editar', methods=['POST'])
def editar():
    try:
        with open('catalogo.json', 'r') as file:
            catalogo = json.load(file)
    except Exception as e:
        print(str(e))

    id = request.form['id']
    categoria = request.form['categoria']
    tipo = request.form['tipo']
    marca = request.form['marca']
    modelo = request.form['modelo']
    cor = request.form['cor']
    valor = request.form['valor']
    estoque = request.form['estoque']
    tamanhos_disponiveis = ['tamanho unico']

    if id in catalogo:
        existe = True
    else:
        existe = False

    if existe == True:
        for produto, detalhes in catalogo.items():
            if produto == id:
                if (not categoria):
                    pass
                else:
                    detalhes['categoria'] = categoria

                if (not tipo):
                    pass
                else:
                    detalhes['tipo'] = tipo

                if (not marca):
                    pass
                else:
                    detalhes['marca'] = marca

                if (not modelo):
                    pass
                else:
                    detalhes['modelo'] = modelo

                if (not cor):
                    pass
                else:
                    detalhes['cor'] = cor

                if (not valor):
                    pass
                else:
                    detalhes['valor'] = valor

                if (not estoque):
                    pass
                else:
                    detalhes['estoque'] = estoque

                if (not tamanhos_disponiveis):
                    pass
                else:
                    detalhes['tamanhos_disponiveis'] = tamanhos_disponiveis

    try:
        with open('catalogo.json', 'w', encoding="utf-8") as arquivo:
            json.dump(catalogo, arquivo)
    except Exception as e:
        print(str(e))

    return render_template('etapa1.html', catalogo=catalogo)


'''def compress_rle(data):
    if not data:
        return ""

    compressed = []
    count = 1
    prev_char = data[0]

    for char in data[1:]:
        if char == prev_char:
            count += 1
        else:
            compressed.append(prev_char + str(count))
            prev_char = char
            count = 1

    compressed.append(prev_char + str(count))
    return ''.join(compressed)

@app.route('/download', methods=['GET'])
def compress_and_download():
    try:
        with open('catalogo.json', 'r') as file:
            catalogo = json.load(file)
    except Exception as e:
        print(str(e))
    json_string = json.dumps(catalogo)
    compressed_data = compress_rle(json_string)
    with open('compressed.json', 'w') as f:
        f.write(compressed_data)
    return send_file('compressed.json', as_attachment=True)'''


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
    titulo = "Catálogo"
    try:
        with open('catalogo.json', 'r') as file:
            catalogo = json.load(file)
    except Exception as e:
        print(str(e))
    return render_template('etapa2.html', titulo=titulo, catalogo=catalogo)


def criarAB_id():
    ap = None
    chave = 1
    return ab.Inserir_id(ap, chave)


def criarAB_valor():
    ap = None
    chave = 1
    return ab.Inserir_chave(ap, chave)


@app.route('/pesquisa', methods=['POST'])
def pesquisa():
    radio = request.form.get('radio')
    if radio == 'id':
        (ap2, chave2, df) = criarAB_id()
        reg = ab.Registro()
        reg.Chave = int(request.form['chave'])
        encontrou = ab.Pesquisa(reg, ap2)
        try:
            with open('catalogo.json', 'r') as file:
                catalogo = json.load(file)
        except Exception as e:
            print(str(e))
            catalogo = {}
        output = {}
        if encontrou is not None:
            chave_encontrada = str(encontrou.Chave)
            if chave_encontrada in catalogo:
                detalhes = catalogo[chave_encontrada]
                output[chave_encontrada] = {
                    'categoria': detalhes['categoria'],
                    'tipo': detalhes['tipo'],
                    'marca': detalhes['marca'],
                    'modelo': detalhes['modelo'],
                    'cor': detalhes['cor'],
                    'valor': detalhes['valor'],
                    'estoque': detalhes['estoque'],
                    'tamanhos_disponiveis': detalhes.get('tamanhos_disponiveis', ['tamanho unico'])
                }
    else:
        (ap2, chave2, df) = criarAB_valor()
        reg = ab.Registro()
        reg.Chave = float(request.form['chave'])
        encontrou = ab.Pesquisa(reg, ap2)
        try:
            with open('catalogo.json', 'r') as file:
                catalogo = json.load(file)
        except Exception as e:
            print(str(e))
            catalogo = {}
        output = {}
        if encontrou is not None:
            elemento_encontrado = str(encontrou.Elemento)
            if elemento_encontrado in catalogo:
                detalhes = catalogo[elemento_encontrado]
                output[elemento_encontrado] = {
                    'categoria': detalhes['categoria'],
                    'tipo': detalhes['tipo'],
                    'marca': detalhes['marca'],
                    'modelo': detalhes['modelo'],
                    'cor': detalhes['cor'],
                    'valor': detalhes['valor'],
                    'estoque': detalhes['estoque'],
                    'tamanhos_disponiveis': detalhes.get('tamanhos_disponiveis', ['tamanho unico'])
                }

    return render_template('etapa2.html', titulo='Catálogo', catalogo=output)


'''@app.route('/pesquisa', methods=['POST'])
def pesquisa():
    (ap2, chave2, df) = criarAB()
    reg = ab.Registro()
    reg.Chave = int(request.form['chave']) 
    reg.Elemento = float(reg.Chave)

    radio = request.form.get('radio')
    encontrou = ab.Pesquisa(reg, ap2, radio)
    
    try:
        with open('catalogo.json', 'r') as file:
            catalogo = json.load(file)
    except Exception as e:
        print(str(e))
        catalogo = {}
    output = {}
    if encontrou is not None:
        elemento_encontrado = str(encontrou.Elemento)
        chave_encontrada = str(encontrou.Chave)
        print(chave_encontrada)
        print(elemento_encontrado)
        if radio == 'id':           
            if chave_encontrada in catalogo:
                detalhes = catalogo[chave_encontrada]
                output[chave_encontrada] = {
                    'categoria': detalhes['categoria'],
                    'tipo': detalhes['tipo'],
                    'marca': detalhes['marca'],
                    'modelo': detalhes['modelo'],
                    'cor': detalhes['cor'],
                    'valor': detalhes['valor'],
                    'estoque': detalhes['estoque'],
                    'tamanhos_disponiveis': detalhes.get('tamanhos_disponiveis', ['tamanho unico'])
                }
        else:
            if chave_encontrada in catalogo:
                detalhes = catalogo[chave_encontrada]
                output[chave_encontrada] = {
                    'categoria': detalhes['categoria'],
                    'tipo': detalhes['tipo'],
                    'marca': detalhes['marca'],
                    'modelo': detalhes['modelo'],
                    'cor': detalhes['cor'],
                    'valor': detalhes['valor'],
                    'estoque': detalhes['estoque'],
                    'tamanhos_disponiveis': detalhes.get('tamanhos_disponiveis', ['tamanho unico'])
                }
        
    else:
        print('oi')

    return render_template('etapa2.html', titulo='Catálogo', catalogo=output)'''


@app.route('/imprime_ordem', methods=['POST'])
def imprime_ordem():
    radio = request.form.get('radio')
    print(radio)
    lista = {}
    if radio == 'id':
        (ap2, chave2, df) = criarAB_id()
        lista = ab.Imprime(ap2, lista, radio)
    else:
        (ap2, chave2, df) = criarAB_valor()
        lista = ab.Imprime(ap2, lista, radio)
    return render_template('etapa2.html', titulo='Catálogo', catalogo=lista)


@app.route('/imprime_menor', methods=['POST'])
def imprime_menor():
    radio = request.form.get('radio')
    print(radio)
    lista = {}
    if radio == 'id':
        (ap2, chave2, df) = criarAB_id()
        reg = ab.Registro()
        reg.Chave = int(request.form['id'])
        lista = ab.ImprimeMenor(reg, ap2, lista, radio)
    else:
        (ap2, chave2, df) = criarAB_valor()
        reg = ab.Registro()
        reg.Chave = float(request.form['id'])
        lista = ab.ImprimeMenor(reg, ap2, lista, radio)
    return render_template('etapa2.html', titulo='Catálogo', catalogo=lista)


@app.route('/imprime_maior', methods=['POST'])
def imprime_maior():
    radio = request.form.get('radio')
    print(radio)
    lista = {}
    if radio == 'id':
        (ap2, chave2, df) = criarAB_id()
        reg = ab.Registro()
        reg.Chave = int(request.form['id'])
        lista = ab.ImprimeMaior(reg, ap2, lista, radio)
    else:
        (ap2, chave2, df) = criarAB_valor()
        reg = ab.Registro()
        reg.Chave = float(request.form['id'])
        lista = ab.ImprimeMaior(reg, ap2, lista, radio)
    return render_template('etapa2.html', titulo='Catálogo', catalogo=lista)


@app.route('/imprime_entre', methods=['POST'])
def imprime_entre():
    radio = request.form.get('radio')
    print(radio)
    lista = {}
    if radio == 'id':
        (ap2, chave2, df) = criarAB_id()

        regmaior = ab.Registro()
        regmaior.Chave = int(request.form['idmaior'])

        regmenor = ab.Registro()
        regmenor.Chave = int(request.form['idmenor'])

        lista = ab.ImprimirEntreRegistro(regmenor, regmaior, ap2, lista, radio)
    else:
        (ap2, chave2, df) = criarAB_valor()

        regmaior = ab.Registro()
        regmaior.Chave = float(request.form['idmaior'])

        regmenor = ab.Registro()
        regmenor.Chave = float(request.form['idmenor'])

        lista = ab.ImprimirEntreRegistro(regmenor, regmaior, ap2, lista, radio)
    return render_template('etapa2.html', titulo='Catálogo', catalogo=lista)


@app.route('/etapa3')
def sobre3():
    titulo = "Catálogo"
    try:
        with open('catalogo.json', 'r') as file:
            catalogo = json.load(file)
    except Exception as e:
        print(str(e))

    m = folium.Map(location=[-12.9714, -38.5014], zoom_start=13)
    mapa_html = m._repr_html_()

    mapa_path = os.path.join('static', 'mapa.html')
    m.save(mapa_path) 

    return render_template('etapa3.html', titulo=titulo, catalogo=catalogo, mapa_html=mapa_html)

@app.route('/mapa')
def mapa():
    return render_template('mapa.html')
    

# exemplo no navegador
# http://localhost:5000/paginaEDII


# execução
app.run(debug=True)
