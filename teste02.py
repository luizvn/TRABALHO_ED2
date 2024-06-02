import pandas as pd

arq = 'catalogo.json'
if arq.lower().endswith(".json"):
    dataframe = pd.read_json(arq)
else:
    print ("Arquivo incompatível.")

Lista_id = list(dataframe.columns)

print(Lista_id)