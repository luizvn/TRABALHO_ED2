'''import arvoreB2 as ab
import arvoreB3 as ab3
import json'''
import pandas as pd
import arvoreB as ab
import json

ap = None
chave = 1

(ap2, chave2, df) = ab.Inserir(ap, chave)
lista = {}
lista = ab.Imprime(ap2, lista)

print('======================')

reg = ab.Registro()
reg.Chave = 4
lista = {}
lista = ab.ImprimeMenor(reg, ap2, lista)

print('======================')

reg = ab.Registro()
reg.Chave = 4
lista = {}
lista = ab.ImprimeMaior(reg, ap2, lista)

print('======================')

print('======================')

try:
    with open('catalogo.json', 'r') as file:
        data = json.load(file)
except Exception as e:
    print(str(e))


ab.ImprimirOrdemArvore(ap2, data)



reg = ab.Registro()
reg.Chave = 10
reg = ab.Pesquisa(reg, ap2)
if reg != None:
    print('entrou')
    print(f'{reg.Chave} - {reg.Elemento}')
else:
    print('erro!')

print('======================')

'''arq = 'catalogo.json'
if arq.lower().endswith(".json"):
    dataframe = pd.read_json(arq)
else:
    print ("Arquivo incompatível.")

reg = ab.Registro()
reg.Chave = 4
ab.ImprimeMaiorDataFrame(reg, ap2, dataframe) # TALVEZ NECESSITE ADAPTACAO

print('======================')

reg = ab.Registro()
reg.Chave = 4
ab.ImprimeMenorDataFrame(reg, ap2, dataframe) # TALVEZ NECESSITE ADAPTACAO

print('======================')'''

regMenor = ab.Registro()
regMenor.Chave = 7
regMaior = ab.Registro()
regMaior.Chave = 10
ab.ImprimirEntreRegistro(regMenor, regMaior, ap2)


