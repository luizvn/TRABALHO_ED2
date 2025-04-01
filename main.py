from flask import Flask, url_for, render_template, request, jsonify, send_file, flash
import json
import sys
import gzip
from io import BytesIO
import arvoreB as ab  # Arvore B
import folium
from igraph import *
import os

# |=======| INICIALIZAÇÃO |=======|
app = Flask(__name__, static_folder='src')
app.secret_key = 'gabi_luiz'

# |=======| IROTA PRINCIPAL(HOME) |=======|
@app.route('/')
def principal():
    return render_template('index.html')

# |=======| ETAPA 01 |=======|
# ======= ROTA ETAPA 01 =======
@app.route('/etapa1')
def sobre1():
    titulo = "Catálogo"

    try:
        with open('catalogo.json', 'r') as file:
            catalogo = json.load(file)
    except Exception as e:
        print(str(e))
    return render_template('etapa1.html', titulo=titulo, catalogo=catalogo)

# ======= CARREGANDO A TABELA DA ETAPA 01 =======
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

# ======= MÉTODO DE INSERIR ELEMENTO =======
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

# ======= MÉTODO DE DELETAR ELEMENTO =======
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

# ======= MÉTODO DE EDITAR ELEMENTO =======
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

# ======= DOWLOAD DO JSON =======
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

# ======= COMPRIMINDO JSON =======
def compress_json(json_data):
    # Comprimindo os dados JSON
    with BytesIO() as compressed_file:
        with gzip.GzipFile(fileobj=compressed_file, mode='wb') as f:
            json_str = json.dumps(json_data)
            f.write(json_str.encode('utf-8'))
        return compressed_file.getvalue()

# |=======| ETAPA 02 |=======|
# ======= CARREGANDO CATÁLOGO NA TABELA =======
@app.route('/etapa2')
def sobre2():
    titulo = "Catálogo"
    try:
        with open('catalogo.json', 'r') as file:
            catalogo = json.load(file)
    except Exception as e:
        print(str(e))
    return render_template('etapa2.html', titulo=titulo, catalogo=catalogo)

# ======= CRIANDO ÁRVORE B POR ID =======
def criarAB_id():
    ap = None
    chave = 1
    return ab.Inserir_id(ap, chave)

# ======= CRIANDO ÁRVORE B POR VALOR =======
def criarAB_valor():
    ap = None
    chave = 1
    return ab.Inserir_chave(ap, chave)

# ======= MÉTODO PARA PESQUISAR NA ÁRVORE B =======
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

# ======= IMPRIMINDO ÁRVORE B EM ORDEM =======
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

# ======= CRIANDO MENOR ELEMENTO DA ÁRVORE B =======
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

# ======= CRIANDO MAIOR ELEMENTO DA ÁRVORE B =======
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

# ======= CRIANDO ENTRE DOIS ELEMENTOS PELA ÁRVORE B =======
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


# |=======| GRAFOS |=======|

# ======= COORDENADAS =======
coordenadas = {
    'Barra': [-13.009615, -38.531981], #0
    'Ondina': [-13.005999, -38.509447], #1
    'Rio Vermelho': [-13.013154, -38.490853], #2
    'Pituba':[-13.005374, -38.458890], #3
    'Itaigara':[-12.996067, -38.467264], #4
    'Boca do Rio':[-12.979125, -38.428300], #5
    'Imbui':[-12.969172, -38.434016], #6
    'Vitória':[-12.995058, -38.526659], #7
    'Comércio':[-12.971356, -38.512657], #8
    'Dique do Tororó':[-12.983893, -38.506903], #9
    'Federação':[-12.999309, -38.499580], #10
    'Vila Laura':[-12.972273, -38.487984], #11
    'Brotas':[-12.989544, -38.491740], #12
    'Liberdade':[-12.951103, -38.495833], #13
    'Uruguai':[-12.932799, -38.496649], #14
    'Ribeira':[-12.912603, -38.496496], #15
    'Pernambués':[-12.967737, -38.461914], #16
    'Cabula':[-12.957054, -38.453342], #17
    'Sussuarana':[-12.932990, -38.445747], #18
    'Canabrava':[-12.919384, -38.426655], #19
    'São Caetano':[-12.937074, -38.476358], #20
    'Lobato':[-12.911165, -38.479429], #21
    'Piatã':[-12.952999, -38.385205], #22
    'Plataforma':[-12.900842, -38.483310], #23
    'Pirajá':[-12.899566, -38.463253], #24
    'São Rafael':[-12.936610, -38.422724], #25
}

# ======= CRIANDO GRAFO ======= 
g = Graph(directed=True)
g.add_vertices(len(coordenadas))
for i, (key, value) in enumerate(coordenadas.items()):
    g.vs[i]["id"] = i
    g.vs[i]["label"] = key

# ======= ADICIONANDO ARESTAS =======
g.add_edges([(0, 1), (0, 7),                          # Barra x
              (1, 10), (1, 9), (1, 2),                # Ondina x
              (2, 10), (2, 3), (2, 4),                # Rio Vermelho x
              (3, 4), (3, 5),                         # Pituba x
              (4, 5),                                 # Itaigara x
              (5, 6), (5, 22),                        # Boca do Rio x
              (6, 16), (6, 17), (6, 25),              # Imbui x
              (7, 8), (7, 9),                         # Vitória x
              (8, 9), (8, 11), (8, 13),               # Comércio x
              (9, 10), (9, 11), (9, 12),              # Dique do Tororó x
              (10, 12),                               # Federação x
              (11, 16), (11, 13),                     # Vila Laura x
              (12, 11), (12, 4),                      # Brotas x
              (13, 14), (13, 20),                     # Liberdade x
              (14, 15), (14, 21), (14, 20),           # Uruguai x
                                                      # Ribeira x
              (16, 17), (16, 6),                      # Pernambues x
              (17, 18),                               # Cabula x
              (18, 19), (18, 25),                     # Sussuarana x
                                                      # Canabrava  x
              (20, 14), (20, 18),                     # São Caetano x
              (21, 23), (21, 24),                     # Lobato x
                                                      # Piatã x
                                                      # Plataforma x
                                                      # Pirajá x
              (25, 18), (25, 22),                     # São Rafael x   
              ])                       
#45 conexões, caminhos

# ======= ADICIONANDO DISTÂNCIAS =======
weights = [3.5, 2.8, 4.1, 5.4, 2.7, 3.9, 4.2, 5.4, 2.0, 5.1, 5,0, 3.2, 6.8, 3.9, 3.4, 5.0, 3.7, 4.7, 2.9, 4.5, 4.3, 3.2, 4.7, 4.5, 2.6, 3.8, 3.4, 3.6, 4.8, 4.3, 3.7, 4.0, 7.2, 
           5.1, 5.2, 5.7, 4.4, 4.4, 5.0, 6.0, 3.3, 3.5, 3.7, 7.9]
g.es['weight'] = weights

# ======= CALCULANDO SUBTOTAL =======
def calcular_subtotal(dict):
    subtotal = 0.0
    for codigo, produto in dict.items():
        subtotal = subtotal + float(produto['valor']) * int(produto['quantidade'])
    return round(subtotal, 2)

# ======= GERANDO MENOR CAMINHO ENTRE GRAFOS =======
def get_shortest_path(grafo, origem, destino):
    try:
        origem_idx = [v.index for v in grafo.vs if v['label'] == origem][0]
        destino_idx = [v.index for v in grafo.vs if v['label'] == destino][0]
        
        caminho = grafo.get_shortest_paths(origem_idx, to=destino_idx, weights='weight', output='epath')[0]
        peso_total = sum(grafo.es[e]['weight'] for e in caminho)
        
        caminho_bairros = [grafo.vs[edge.source]['label'] for edge in grafo.es[caminho]] + [destino]
        return caminho_bairros, peso_total, caminho
    except IndexError:
        print('erro no destino')
        return None, float('inf'), None

# |=======| ETAPA 03 |=======|
@app.route('/etapa3')
def sobre3():
    titulo = "Catálogo"
    try:
        with open('catalogo.json', 'r') as file:
            catalogo = json.load(file)
    except Exception as e:
        print(str(e))

    try:
        with open('carrinho.json', 'r') as file:
            carrinho = json.load(file)
            subtotal = calcular_subtotal(carrinho)
    except Exception as e:
        carrinho = {}
        subtotal = 0
        print(str(e))
    titulo_carrinho = 'Carrinho'

    m = folium.Map(location=[-12.9535447,-38.483914], zoom_start=12)
    
    for edge in g.es:
        start = coordenadas[g.vs[edge.source]["label"]]
        end = coordenadas[g.vs[edge.target]["label"]]
        folium.PolyLine([start, end],color='red', weight=2.0, opacity=0.6).add_to(m)

    for vertex in g.vs:
        coords = coordenadas[vertex["label"]]
        if vertex['label'] == 'Barra':
            folium.Marker(location=coords, popup=vertex["label"], icon=folium.Icon(color='red')).add_to(m)
        else:
            folium.Marker(location=coords, popup=vertex["label"], icon=folium.Icon(color='black')).add_to(m)

    mapa_html = m._repr_html_()
    mapa_path = os.path.join('static', 'mapa.html')
    m.save(mapa_path) 

    return render_template('etapa3.html', titulo=titulo, catalogo=catalogo, mapa_html=mapa_html, carrinho=carrinho, titulo_carrinho=titulo_carrinho, subtotal=subtotal)

# ======= MAPA =======
@app.route('/mapa')
def mapa():
    return render_template('mapa.html')

# ======= INSERIR NO CARRINHO =======
@app.route('/inserir_carrinho', methods=['POST'])
def adicionar_carrinho():
    titulo = "Catálogo"
    try:
        with open('catalogo.json', 'r') as file:
            catalogo = json.load(file)
    except Exception as e:
        print(str(e))

    try:
        with open('carrinho.json', 'r') as file:
            carrinho = json.load(file)
            
    except Exception as e:
        carrinho = {}
        subtotal = 0
        print(str(e))

    produto = request.form['chave']
    quantidade = request.form['quantidade']

    titulo_carrinho = 'Carrinho'
    if produto in catalogo:
        detalhes = catalogo[produto]
        carrinho[produto] = {
            'categoria': detalhes['categoria'],
            'tipo': detalhes['tipo'],
            'marca': detalhes['marca'],
            'modelo': detalhes['modelo'],
            'cor': detalhes['cor'],
            'valor': detalhes['valor'],
            'quantidade': quantidade,
            'estoque': detalhes['estoque']    
        }
        
    subtotal = calcular_subtotal(carrinho)

    try:
        with open('carrinho.json', 'w') as file:
            json.dump(carrinho, file)
    except Exception as e:
        print(str(e))    

    m = folium.Map(location=[-12.9535447,-38.483914], zoom_start=12)
    
    for edge in g.es:
        start = coordenadas[g.vs[edge.source]["label"]]
        end = coordenadas[g.vs[edge.target]["label"]]
        folium.PolyLine([start, end],color='red', weight=2.0, opacity=0.6).add_to(m)

    for vertex in g.vs:
        coords = coordenadas[vertex["label"]]
        if vertex['label'] == 'Barra':
            folium.Marker(location=coords, popup=vertex["label"], icon=folium.Icon(color='red')).add_to(m)
        else:
            folium.Marker(location=coords, popup=vertex["label"], icon=folium.Icon(color='black')).add_to(m)

    mapa_html = m._repr_html_()
    mapa_path = os.path.join('static', 'mapa.html')
    m.save(mapa_path)
    return render_template('etapa3.html', titulo=titulo, catalogo=catalogo, mapa_html=mapa_html, carrinho=carrinho, titulo_carrinho=titulo_carrinho, subtotal=subtotal)

# ======= REMOVER DO CARRINHO =======
@app.route('/remover_carrinho', methods=['POST'])
def remover_carrinho():
    titulo = "Catálogo"
    try:
        with open('catalogo.json', 'r') as file:
            catalogo = json.load(file)
    except Exception as e:
        print(str(e))

    try:
        with open('carrinho.json', 'r') as file:
            carrinho = json.load(file)
            
    except Exception as e:
        carrinho = {}
        subtotal = 0
        print(str(e))

    produto = request.form['chave']

    titulo_carrinho = 'Carrinho'
    if produto in carrinho.keys():
        removido = carrinho.pop(produto)

    subtotal = calcular_subtotal(carrinho)

    try:
        with open('carrinho.json', 'w') as file:
            json.dump(carrinho, file)
    except Exception as e:
        print(str(e))    

    m = folium.Map(location=[-12.9535447,-38.483914], zoom_start=12)
    
    for edge in g.es:
        start = coordenadas[g.vs[edge.source]["label"]]
        end = coordenadas[g.vs[edge.target]["label"]]
        folium.PolyLine([start, end],color='red', weight=2.0, opacity=0.6).add_to(m)

    for vertex in g.vs:
        coords = coordenadas[vertex["label"]]
        if vertex['label'] == 'Barra':
            folium.Marker(location=coords, popup=vertex["label"], icon=folium.Icon(color='red')).add_to(m)
        else:
            folium.Marker(location=coords, popup=vertex["label"], icon=folium.Icon(color='black')).add_to(m)

    mapa_html = m._repr_html_()
    mapa_path = os.path.join('static', 'mapa.html')
    m.save(mapa_path)
    return render_template('etapa3.html', titulo=titulo, catalogo=catalogo, mapa_html=mapa_html, carrinho=carrinho, titulo_carrinho=titulo_carrinho, subtotal=subtotal)
    
# ======= CONFIRMAR CARRINHO =======
@app.route('/confirmar_carrinho', methods=['POST'])
def confirmar_carrinho():
    titulo = "Catálogo"
    try:
        with open('catalogo.json', 'r') as file:
            catalogo = json.load(file)
    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Erro ao carregar o catálogo.'}), 500

    try:
        with open('carrinho.json', 'r') as file:
            carrinho = json.load(file)
            subtotal = calcular_subtotal(carrinho)
    except Exception as e:
        carrinho = {}
        subtotal = 0
        print(str(e))
        return jsonify({'error': 'ERRO AO MANDAR O CARRINHO'}), 500

    destino = str(request.form['chave'])
    origem = 'Barra'

    caminho, peso, caminho_arestas = get_shortest_path(g, origem, destino)
    if caminho:
        print(f"Caminho mais curto de {origem} para {destino}: {' -> '.join(caminho)}")
        print(f"Peso total do caminho: {peso}")
        subtotal = subtotal + (peso * 2.2)
        subtotal = round(subtotal, 2)
    else:
        print('[erro] - Destino errado')  # mandar retorno pro js para exibir um alert
        return jsonify({'error': 'DESTINO MANDADO FOI ERRADO'}), 400

    titulo_carrinho = 'Carrinho'

    m = folium.Map(location=[-12.9535447, -38.483914], zoom_start=12)

    for edge_index in caminho_arestas:
        edge = g.es[edge_index]
        start = coordenadas[g.vs[edge.source]["label"]]
        end = coordenadas[g.vs[edge.target]["label"]]
        folium.PolyLine([start, end], color='red', weight=2.0, opacity=0.6).add_to(m)

    for vertex in g.vs:
        coords = coordenadas[vertex["label"]]
        if vertex['label'] == 'Barra':
            folium.Marker(location=coords, popup=vertex["label"], icon=folium.Icon(color='red')).add_to(m)
        else:
            folium.Marker(location=coords, popup=vertex["label"], icon=folium.Icon(color='black')).add_to(m)

    mapa_html = m._repr_html_()
    mapa_path = os.path.join('static', 'mapa.html')
    m.save(mapa_path)
    return render_template('etapa3.html', titulo=titulo, catalogo=catalogo, mapa_html=mapa_html, carrinho=carrinho, titulo_carrinho=titulo_carrinho, subtotal=subtotal)

def remover_estoque(catalogo, carrinho):
    for codigo, produto in catalogo.items():
        if codigo in carrinho:
            quantidade_carrinho = int(carrinho[codigo]['quantidade'])
            if int(produto['estoque']) < quantidade_carrinho:
                return False, f"Estoque insuficiente para o produto de ID {codigo}. Quantidade em estoque: {produto['estoque']}."
            produto['estoque'] -= quantidade_carrinho
    return True, "Estoque atualizado com sucesso."

@app.route('/finalizar_pedido', methods=['POST'])
def finalizar_pedido():
    titulo = "Catálogo"
    titulo_carrinho = 'Carrinho'
    try:
        with open('catalogo.json', 'r') as file:
            catalogo = json.load(file)
    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Erro ao carregar o catálogo.'}), 500

    try:
        with open('carrinho.json', 'r') as file:
            carrinho = json.load(file)
            subtotal = calcular_subtotal(carrinho)
    except Exception as e:
        carrinho = {}
        subtotal = 0
        print(str(e))
        return jsonify({'error': 'ERRO AO MANDAR O CARRINHO'}), 500
    
    m = folium.Map(location=[-12.9535447,-38.483914], zoom_start=12)
    
    for edge in g.es:
        start = coordenadas[g.vs[edge.source]["label"]]
        end = coordenadas[g.vs[edge.target]["label"]]
        folium.PolyLine([start, end],color='red', weight=2.0, opacity=0.6).add_to(m)

    for vertex in g.vs:
        coords = coordenadas[vertex["label"]]
        if vertex['label'] == 'Barra':
            folium.Marker(location=coords, popup=vertex["label"], icon=folium.Icon(color='red')).add_to(m)
        else:
            folium.Marker(location=coords, popup=vertex["label"], icon=folium.Icon(color='black')).add_to(m)

    mapa_html = m._repr_html_()
    mapa_path = os.path.join('static', 'mapa.html')
    m.save(mapa_path)
    
    # Diminuindo do estoque
    sucesso, mensagem_estoque = remover_estoque(catalogo, carrinho)
    if not sucesso:
        flash(mensagem_estoque, 'error')
        return render_template('etapa3.html', titulo=titulo, catalogo=catalogo, carrinho=carrinho, titulo_carrinho=titulo_carrinho, subtotal=subtotal, mapa_html=mapa_html)

    
    subtotal = 0
    carrinho = {}
    try:
        with open('carrinho.json', 'w') as file:
            json.dump(carrinho, file)
    except Exception as e:
        print(str(e))  

    try:
        with open('catalogo.json', 'w', encoding="utf-8") as arquivo:
            json.dump(catalogo, arquivo)
    except Exception as e:
        print(str(e))

    flash('Pedido finalizado com sucesso!', 'success')
    return render_template('etapa3.html', titulo=titulo, catalogo=catalogo, mapa_html=mapa_html, carrinho=carrinho, titulo_carrinho=titulo_carrinho, subtotal=subtotal)


# execução
app.run(debug=True)
