import json

data = []

with open('result.json', 'r',encoding='UTF-8') as f:
    data = json.load(f)

vereadores = data["Vereadores"]
numeros = []
cont = 1
for v in vereadores:
    numeros.append(v["Numero"])
   

unique = { each['Numero'] : each for each in vereadores }.values()

print(unique)

with open('nums.json', 'w',encoding='UTF-8') as f:
    json.dump({"Numeros":numeros}, f)

