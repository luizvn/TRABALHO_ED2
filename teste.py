'''import arvoreB2 as ab
import arvoreB3 as ab3
import json
import pandas as pd'''
import arvoreB as ab

ap = None
chave = 1

(ap2, chave2, df) = ab.Inserir(ap, chave)

ab.Imprime(ap2)

print('======================')

reg = ab.Registro()
reg.Chave = 4
ab.ImprimeMaior(reg, ap2)

print('======================')

reg = ab.Registro()
reg.Chave = 4
ab.ImprimeMenor(reg, ap2)

print('======================')

reg = ab.Registro()
reg.Chave = 4
reg = ab.Pesquisa(reg, ap2)
if reg != None:
    print('entrou')
    print(f'{reg.Chave} - {reg.Elemento}')
else:
    print('erro!')

