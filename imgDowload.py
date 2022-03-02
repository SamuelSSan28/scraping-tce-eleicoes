import urllib.request
import json
import os.path

data = []

with open('result.json', 'r',encoding='UTF-8') as f:
    data = json.load(f)

vereadores = data["Vereadores"]
for v in vereadores:
    if os.path.exists("vereadores_20_10/"+v["Numero"]+".jpeg"):
        continue
    urllib.request.urlretrieve(v["Imagem"], "vereadores_20_10/"+v["Numero"]+".jpeg")



    