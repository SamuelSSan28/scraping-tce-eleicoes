import json
import pandas as pd

data = []

with open('result.json', 'r',encoding='UTF-8') as f:
    data = json.load(f)

vereadores = data["Vereadores"]
numeros = []

for v in vereadores:
    v["Imagem"] = v["Numero"]+".jpeg"

data["Vereadores"] = vereadores

with open('vereadores.json', 'w',encoding='UTF-8') as f:
    json.dump(data, f)

