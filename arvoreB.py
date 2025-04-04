import pandas as pd #pip install pandas
'''import openpyxl #pip install openpyxl
from openpyxl import load_workbook
from openpyxl.styles import Font
from openpyxl.chart import BarChart, Reference'''
import string
import json

#Declaração das classes e definição do grau da árvore
class Registro:
  def __init__(self):
    self.Chave = None
    self.Elemento = None

class Pagina:
  def __init__(self, ordem):
    self.n = 0
    self.r = [None for i in range(ordem)]
    self.p = [None for i in range(ordem+1)]

#Pesquisa
def Pesquisa(reg, Ap):
  i = 1
  if (Ap == None):
    print("Registro não está presente na árvore\n")
    return None
  while (i < Ap.n and reg.Chave > Ap.r[i - 1].Chave):
    i += 1
  if (reg.Chave == Ap.r[i - 1].Chave):
    reg = Ap.r[i - 1]
    return reg

  if (reg.Chave < Ap.r[i - 1].Chave):
    reg = Pesquisa(reg, Ap.p[i - 1])
  else:
    reg = Pesquisa(reg, Ap.p[i])
  return reg

#Funções de inserção

#Insere o registro na página escolhida
def _InsereNaPagina(Ap, Reg, ApDir):
  k = Ap.n
  NaoAchouPosicao = (k > 0)
  while (NaoAchouPosicao):
    if ( Reg.Chave >= Ap.r[k - 1].Chave ):
      NaoAchouPosicao = False
      break
    Ap.r[k] = Ap.r[k - 1]
    Ap.p[k + 1] = Ap.p[k]
    k-= 1
    if (k < 1):
      NaoAchouPosicao = False

  Ap.r[k] = Reg
  Ap.p[k + 1] = ApDir
  Ap.n += 1

#Busca a página onde o registro será inserido e controla a divisão de páginas por Overflow
def _Ins( Reg, Ap, Cresceu, RegRetorno, ApRetorno, Ordem ):
  #float(Reg.Chave)
  i = 1
  J = None
  if (Ap == None):
    Cresceu = True
    RegRetorno = Reg
    ApRetorno = None
    return Cresceu, RegRetorno, ApRetorno

  while ( i < Ap.n and Reg.Chave > Ap.r[i - 1].Chave ):
    i+= 1

  if(Reg.Chave == Ap.r[i - 1].Chave):
    print(" Erro: Registro já está presente\n")
    Cresceu = False
    return Cresceu, RegRetorno, ApRetorno

  if(Reg.Chave < Ap.r[i - 1].Chave ):
    i-= 1

  Cresceu, RegRetorno, ApRetorno = _Ins(Reg, Ap.p[i], Cresceu, RegRetorno, ApRetorno, Ordem)

  if(not Cresceu):
    return Cresceu, RegRetorno, ApRetorno
  if (Ap.n < Ordem): # Página tem espaco
    _InsereNaPagina(Ap, RegRetorno, ApRetorno)
    Cresceu = False
    return Cresceu, RegRetorno, ApRetorno

  # Overflow: Página tem que ser dividida /
  ApTemp = Pagina(Ordem)
  ApTemp.n = 0
  ApTemp.p[0] = None
  if (i < (Ordem//2) + 1):
    _InsereNaPagina(ApTemp, Ap.r[Ordem - 1], Ap.p[Ordem])
    Ap.n-= 1
    _InsereNaPagina(Ap, RegRetorno, ApRetorno)
  else:
    _InsereNaPagina(ApTemp, RegRetorno, ApRetorno)
  for J in range((Ordem//2) + 2, Ordem + 1):
    _InsereNaPagina(ApTemp, Ap.r[J - 1], Ap.p[J])
  Ap.n = (Ordem//2)
  ApTemp.p[0] = Ap.p[(Ordem//2) + 1]
  RegRetorno = Ap.r[(Ordem//2)]
  ApRetorno = ApTemp
  return Cresceu, RegRetorno, ApRetorno

#Cria página da nova raiz caso a árvore cresça em altura
def _Insere(Reg, Ap, Ordem):
  Cresceu = False
  RegRetorno = Registro()
  ApRetorno = Pagina(Ordem)
  Cresceu, RegRetorno, ApRetorno = _Ins(Reg, Ap, Cresceu, RegRetorno, ApRetorno, Ordem)
  if (Cresceu):
    ApTemp = Pagina(Ordem)
    ApTemp.n = 1
    ApTemp.r[0] = RegRetorno
    ApTemp.p[1] = ApRetorno
    ApTemp.p[0] = Ap
    Ap = ApTemp
  return Ap
  
#Insere elementos do arquivo
def _InserirElementos_id(Ap, ordem, dataframe, chave):
  tam_lin, tam_col = dataframe.shape
  Lista_id = list(dataframe.columns)
  for i in range(tam_col):
      reg = Registro()
      reg.Chave    = Lista_id[i]
      reg.Elemento = float(dataframe.iloc[5, i])
      Ap = _Insere(reg, Ap, ordem)
      chave += 1
  return Ap, chave

#Define os registros a serem inseridos
def Inserir_id(Ap, chave):
  ordem = 4
  arq = 'catalogo.json'
  if arq.lower().endswith(".json"):
    dataframe = pd.read_json(arq)
  else:
    print ("Arquivo incompatível.")

  '''if arq.lower().endswith(".csv"):
    dataframe = pd.read_csv(arq, header=None)      
  elif arq.lower().endswith((".xls", ".xlsx")):
    dataframe = pd.read_excel(arq, header=None)'''
  
  #imprimindo dataframe criado do arquivo
  print("\nDataframe")
  print(dataframe)

  print("------------------------------------")
  '''tam_lin, tam_col = dataframe.shape
  print(tam_lin)
  print(tam_col)'''
  #a = input("Digite um carater para continuar")
  Ap, chave = _InserirElementos_id(Ap, ordem, dataframe, chave)
  return Ap, chave, dataframe

def _InserirElementos_chave(Ap, ordem, dataframe, chave):
  tam_lin, tam_col = dataframe.shape
  Lista_id = list(dataframe.columns)
  for i in range(tam_col):
      reg = Registro()
      reg.Chave    = float(dataframe.iloc[5, i])
      reg.Elemento = Lista_id[i]
      Ap = _Insere(reg, Ap, ordem)
      chave += 1
  return Ap, chave

#Define os registros a serem inseridos
def Inserir_chave(Ap, chave):
  ordem = 4
  arq = 'catalogo.json'
  if arq.lower().endswith(".json"):
    dataframe = pd.read_json(arq)
  else:
    print ("Arquivo incompatível.")

  '''if arq.lower().endswith(".csv"):
    dataframe = pd.read_csv(arq, header=None)      
  elif arq.lower().endswith((".xls", ".xlsx")):
    dataframe = pd.read_excel(arq, header=None)'''
  
  #imprimindo dataframe criado do arquivo
  print("\nDataframe")
  print(dataframe)

  print("------------------------------------")
  '''tam_lin, tam_col = dataframe.shape
  print(tam_lin)
  print(tam_col)'''
  #a = input("Digite um carater para continuar")
  Ap, chave = _InserirElementos_chave(Ap, ordem, dataframe, chave)
  return Ap, chave, dataframe
# =======| FUNÇÕES DE IMPRESSÃO |=======

def Imprime(Ap, lista, string):
  try:
    with open('catalogo.json', 'r') as file:
      catalogo = json.load(file)
  except Exception as e:
    print(str(e))
  if string == 'id':
    if (Ap != None):
      i = 0
      while i < Ap.n:
        Imprime(Ap.p[i], lista, string)
        detalhes = catalogo[str(Ap.r[i].Chave)]
        lista[str(Ap.r[i].Chave)] = {
                  'categoria': detalhes['categoria'],
                  'tipo': detalhes['tipo'],
                  'marca': detalhes['marca'],
                  'modelo': detalhes['modelo'],
                  'cor': detalhes['cor'],
                  'valor': detalhes['valor'],
                  'estoque': detalhes['estoque'],
                  'tamanhos_disponiveis': detalhes.get('tamanhos_disponiveis', ['tamanho unico'])
              }
        print(Ap.r[i].Chave, "-", Ap.r[i].Elemento)
        i += 1
      Imprime(Ap.p[i], lista, string)
      return lista
  else:
    if (Ap != None):
      i = 0
      while i < Ap.n:
        Imprime(Ap.p[i], lista, string)
        detalhes = catalogo[str(Ap.r[i].Elemento)]
        lista[str(Ap.r[i].Elemento)] = {
                  'categoria': detalhes['categoria'],
                  'tipo': detalhes['tipo'],
                  'marca': detalhes['marca'],
                  'modelo': detalhes['modelo'],
                  'cor': detalhes['cor'],
                  'valor': detalhes['valor'],
                  'estoque': detalhes['estoque'],
                  'tamanhos_disponiveis': detalhes.get('tamanhos_disponiveis', ['tamanho unico'])
              }
        print(Ap.r[i].Chave, "-", Ap.r[i].Elemento)
        i += 1
      Imprime(Ap.p[i], lista, string)
      return lista

def ImprimeMenor(reg, Ap, lista, radio): # Imprime valores menores doq informado
  try:
    with open('catalogo.json', 'r') as file:
      catalogo = json.load(file)
  except Exception as e:
    print(str(e))
  if radio == 'id':
    if (Ap != None):
      i = 0
      while i < Ap.n:
        ImprimeMenor(reg, Ap.p[i], lista, radio)
        if (Ap.r[i].Chave < reg.Chave):
          detalhes = catalogo[str(Ap.r[i].Chave)]
          lista[str(Ap.r[i].Chave)] = {
                  'categoria': detalhes['categoria'],
                  'tipo': detalhes['tipo'],
                  'marca': detalhes['marca'],
                  'modelo': detalhes['modelo'],
                  'cor': detalhes['cor'],
                  'valor': detalhes['valor'],
                  'estoque': detalhes['estoque'],
                  'tamanhos_disponiveis': detalhes.get('tamanhos_disponiveis', ['tamanho unico'])
              }
          print(Ap.r[i].Chave, "-", Ap.r[i].Elemento)
        i += 1
      ImprimeMenor(reg, Ap.p[i], lista, radio)
    return lista
  else:
    if (Ap != None):
      i = 0
      while i < Ap.n:
        ImprimeMenor(reg, Ap.p[i], lista, radio)
        if (Ap.r[i].Chave < reg.Chave):
          detalhes = catalogo[str(Ap.r[i].Elemento)]
          lista[str(Ap.r[i].Elemento)] = {
                  'categoria': detalhes['categoria'],
                  'tipo': detalhes['tipo'],
                  'marca': detalhes['marca'],
                  'modelo': detalhes['modelo'],
                  'cor': detalhes['cor'],
                  'valor': detalhes['valor'],
                  'estoque': detalhes['estoque'],
                  'tamanhos_disponiveis': detalhes.get('tamanhos_disponiveis', ['tamanho unico'])
              }
          print(Ap.r[i].Chave, "-", Ap.r[i].Elemento)
        i += 1
      ImprimeMenor(reg, Ap.p[i], lista, radio)
    return lista

def ImprimeMaior(reg, Ap, lista, radio):
  try:
    with open('catalogo.json', 'r') as file:
      catalogo = json.load(file)
  except Exception as e:
    print(str(e))
  if radio == 'id':
    if (Ap != None):
      i = 0
      while i < Ap.n:
        ImprimeMaior(reg, Ap.p[i], lista, radio)
        if (Ap.r[i].Chave > reg.Chave):
          detalhes = catalogo[str(Ap.r[i].Chave)]
          lista[str(Ap.r[i].Chave)] = {
                  'categoria': detalhes['categoria'],
                  'tipo': detalhes['tipo'],
                  'marca': detalhes['marca'],
                  'modelo': detalhes['modelo'],
                  'cor': detalhes['cor'],
                  'valor': detalhes['valor'],
                  'estoque': detalhes['estoque'],
                  'tamanhos_disponiveis': detalhes.get('tamanhos_disponiveis', ['tamanho unico'])
              }
          print(Ap.r[i].Chave, "-", Ap.r[i].Elemento)
        i += 1
      ImprimeMaior(reg, Ap.p[i], lista, radio)
    return lista
  else:
    if (Ap != None):
      i = 0
      while i < Ap.n:
        ImprimeMaior(reg, Ap.p[i], lista, radio)
        if (Ap.r[i].Chave > reg.Chave):
          detalhes = catalogo[str(Ap.r[i].Elemento)]
          lista[str(Ap.r[i].Elemento)] = {
                  'categoria': detalhes['categoria'],
                  'tipo': detalhes['tipo'],
                  'marca': detalhes['marca'],
                  'modelo': detalhes['modelo'],
                  'cor': detalhes['cor'],
                  'valor': detalhes['valor'],
                  'estoque': detalhes['estoque'],
                  'tamanhos_disponiveis': detalhes.get('tamanhos_disponiveis', ['tamanho unico'])
              }
          print(Ap.r[i].Chave, "-", Ap.r[i].Elemento)
        i += 1
      ImprimeMaior(reg, Ap.p[i], lista, radio)
    return lista
    
#Impressão Arquivo Completo
#obtenção da chave na árvoreB e restante dos dados do DataFrame
def ImprimeMenorDataFrame(x, Ap, df):
  if (Ap != None):
    i = 0
    while i < Ap.n:
      ImprimeMenorDataFrame(x, Ap.p[i],df)
      if (Ap.r[i].Chave < x.Chave):
        print(df.iloc[Ap.r[i].Elemento])
      i += 1
    ImprimeMenorDataFrame(x, Ap.p[i], df)

def ImprimeMaiorDataFrame(x, Ap, df):
  if (Ap != None):
    i = 0
    while i < Ap.n:
      ImprimeMaiorDataFrame(x, Ap.p[i],df)
      if (Ap.r[i].Chave > x.Chave):
        print(df.iloc[ Ap.r[i].Elemento])
      i += 1
    ImprimeMaiorDataFrame(x, Ap.p[i],df)

def ImprimirEntreRegistro(regMenor, regMaior, Ap, lista, radio):
  try:
    with open('catalogo.json', 'r') as file:
      catalogo = json.load(file)
  except Exception as e:
    print(str(e))
  if radio == 'id':
    if Ap != None:
      i = 0
      while(i < Ap.n):
        ImprimirEntreRegistro(regMenor, regMaior, Ap.p[i], lista, radio) # Vai para a esquerda
        if((Ap.r[i].Chave > regMenor.Chave) and (Ap.r[i].Chave < regMaior.Chave)):
          detalhes = catalogo[str(Ap.r[i].Chave)]
          lista[str(Ap.r[i].Chave)] = {
                  'categoria': detalhes['categoria'],
                  'tipo': detalhes['tipo'],
                  'marca': detalhes['marca'],
                  'modelo': detalhes['modelo'],
                  'cor': detalhes['cor'],
                  'valor': detalhes['valor'],
                  'estoque': detalhes['estoque'],
                  'tamanhos_disponiveis': detalhes.get('tamanhos_disponiveis', ['tamanho unico'])
              }
          print(f'{Ap.r[i].Chave} - {Ap.r[i].Elemento}')
        i += 1
      ImprimirEntreRegistro(regMenor, regMaior, Ap.p[i], lista, radio) # Vai para a direita
      return lista
  else:
    if Ap != None:
      i = 0
      while(i < Ap.n):
        ImprimirEntreRegistro(regMenor, regMaior, Ap.p[i], lista, radio) # Vai para a esquerda
        if((Ap.r[i].Chave > regMenor.Chave) and (Ap.r[i].Chave < regMaior.Chave)):
          detalhes = catalogo[str(Ap.r[i].Elemento)]
          lista[str(Ap.r[i].Elemento)] = {
                  'categoria': detalhes['categoria'],
                  'tipo': detalhes['tipo'],
                  'marca': detalhes['marca'],
                  'modelo': detalhes['modelo'],
                  'cor': detalhes['cor'],
                  'valor': detalhes['valor'],
                  'estoque': detalhes['estoque'],
                  'tamanhos_disponiveis': detalhes.get('tamanhos_disponiveis', ['tamanho unico'])
              }
          print(f'{Ap.r[i].Chave} - {Ap.r[i].Elemento}')
        i += 1
      ImprimirEntreRegistro(regMenor, regMaior, Ap.p[i], lista, radio) # Vai para a direita
      return lista

'''def ImprimirOrdemArvore(Ap):
  if Ap != None:
    i = 0
    while i < Ap.n:
      ImprimirOrdemArvore(Ap.p[i])
      for j in range(len(Ap.p) - 1):
        ImprimirOrdemArvore(Ap.p[j + 1])
      print(f'{Ap.r[i].Chave} - {Ap.r[i].Elemento}')
      i += 1
'''

def ImprimirOrdemArvore(Ap, data):
    if Ap is not None:
        i = 0
        while i < Ap.n:
            if Ap.p[0] is not None:
                ImprimirOrdemArvore(Ap.p[i], data)
            print(f'{Ap.r[i].Chave} - {data[str(Ap.r[i].Chave)]}')
            i += 1
        if Ap.p[0] is not None:
            ImprimirOrdemArvore(Ap.p[i], data)
