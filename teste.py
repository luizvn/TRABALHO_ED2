import arvoreB2 as ab
import arvoreB3 as ab3
import json
import pandas as pd

arvoreB = ab3.BTree(2)

with open('catalogo.json', 'r') as file:
        data = json.load(file) 

'''arq = 'catalogo2.json'
if arq.lower().endswith(".json"):
    dataframe = pd.read_json(arq)'''

arvoreB.load_from_json(data)

arvoreB.traverse(data)
a = input()
result = arvoreB.search(5)
if result:
    print(f"Encontrado:  - {result}")
else:
    print(f"Não encontrado: {3}")

result = arvoreB.search(6)
if result:
    print(f"Encontrado:  - {result}")
else:
    print(f"Não encontrado: {6}")
result = arvoreB.search(7)
if result:
    print(f"Encontrado:  - {result}")
else:
    print(f"Não encontrado: {6}")


