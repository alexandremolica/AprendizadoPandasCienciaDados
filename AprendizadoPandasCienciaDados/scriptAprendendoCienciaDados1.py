## Objetivo do script - aprendizado utilizando pandas com ciencias de dados 

## Imports
import pandas as pd
import numpy as np


print('\n--- Carrega dados do arquivo dados_compras.json ---')
## Carrega o arquivo
load_file = "dados_compras.json"
purchase_file = pd.read_json(load_file, orient = "records")
print(purchase_file.head())


print('\n--- Informações Sobre os Consumidores -------------')
## Informações Sobre os Consumidores
# Número total de consumidores
demo = purchase_file.loc[:, ["Login","Idade","Sexo"]]
print(demo.head())

# Limpeza e remocao de dados duplicados
demo = demo.drop_duplicates()
contPes = demo.count()[0]
print('\n')

# Converte saida para DataFrame para uso posterior em analise
contPessoa = pd.DataFrame({"Total de Compradores": [contPes]})
print(contPessoa)


print('\n--- Analise Geral de Compras ---------------------')
## Analise Geral de Compras 
# Número de itens exclusivos
itExc = len(purchase_file["Item ID"].unique())

# Preço médio de compra
prMedio = purchase_file["Valor"].mean()

# Número total de compras
numComp = purchase_file["Valor"].count()

# Rendimento total
renTotal = purchase_file["Valor"].sum()

# Passando resultado para DataFrame
sumarioCalculos = pd.DataFrame({"Numeros de itens unicos": itExc,
                                "Numeros de compras": numComp,
                                "Total de vendas": renTotal,
                                "Preco medio": [prMedio]})

# Data Munging
sumarioCalculos = sumarioCalculos.round(2)
sumarioCalculos ["Preco medio"] = sumarioCalculos["Preco medio"].map("${:,.2f}".format)
sumarioCalculos ["Total de vendas"] = sumarioCalculos["Total de vendas"].map("${:,.2f}".format)
sumarioCalculos = sumarioCalculos.loc[:, ["Numeros de itens unicos", "Preco medio", "Numeros de compras", "Total de vendas"]]
print(sumarioCalculos)


print('\n--- Informacoes Demografica ---------------------')
## Informações Demográfica
# Contagem por genero
contGenero = demo["Sexo"].value_counts()

# percentual por genero
percGenero = (contGenero/ int(contPessoa['Total de Compradores'])) * 100

# Passando resultado para DataFrame
generoDemo = pd.DataFrame({"Sexo": contGenero,
                          "Perc":percGenero })

# Data Munging
generoDemo = generoDemo.round(2)
generoDemo ["Perc"] = generoDemo["Perc"].map("{:,.1f}%".format)
print(generoDemo)


print('\n--- Analise de Compras Por Genero ---------------')
## Analise de Compras Por Genero
#Número de compras
numCompGen =  purchase_file.groupby(["Sexo"]).count()["Valor"].rename("Numero de compras")

#Preço médio de compra
mediaCompGen =  purchase_file.groupby(["Sexo"]).mean()["Valor"].rename("Media de preco")

#Valor Total de Compra
totVendGen =  purchase_file.groupby(["Sexo"]).sum()["Valor"].rename("Total venda")

# total normalizado
totNorm = totVendGen / generoDemo["Sexo"]

# DataFrame
analiseCompGenero = pd.DataFrame({"Numero de compras": numCompGen,
                                 "Valor medio por item":mediaCompGen,
                                 "Total de vendas": totVendGen,
                                 "Total normalizado": totNorm})

# Data Munging
analiseCompGenero = analiseCompGenero.round(2)
analiseCompGenero ["Valor medio por item"] = analiseCompGenero["Valor medio por item"].map("${:,.2f}".format)
analiseCompGenero ["Total de vendas"] = analiseCompGenero["Total de vendas"].map("${:,.2f}".format)
analiseCompGenero ["Total normalizado"] = analiseCompGenero["Total normalizado"].map("${:,.2f}".format)
print(analiseCompGenero)


print('\n--- Analise Demografica ----------------------')
## Analise Demografica
# Cálculos básicos
caixaIdade = [0, 9.99, 14.99, 19.99, 24.99, 29.99, 34.99, 39.99, 999]
faixaIdade = ["Menos de 10", "10 a 14", "15 a 19", "20 a 24", "25 a 29", "30 a 34", "35 a 39", "Mais de 40"]

# Cria coluna com range de idades
purchase_file["Range de Idades"] = pd.cut(purchase_file["Idade"], caixaIdade, labels=faixaIdade)

# Cálculos básicos
contIdadeDemo = purchase_file["Range de Idades"].value_counts()
mediaItemValorIdadeDemo = purchase_file.groupby(["Range de Idades"]).mean()["Valor"]
totalItemValorIdadeDemo = purchase_file.groupby(["Range de Idades"]).sum()["Valor"]
percIdadeDemo = (contIdadeDemo / int(contPessoa['Total de Compradores'])) * 100

# Dataframe para os resultados
idadeDemo = pd.DataFrame({"Contagem": contIdadeDemo, "%": percIdadeDemo, "Valor Unitario": mediaItemValorIdadeDemo, "Valor Total de Compra": totalItemValorIdadeDemo})

# Data Munging
idadeDemo ["Valor Unitario"] = idadeDemo["Valor Unitario"].map("${:,.2f}".format)
idadeDemo ["Valor Total de Compra"] = idadeDemo["Valor Total de Compra"].map("${:,.2f}".format)
idadeDemo ["%"] = idadeDemo["%"].map("{:,.2f}%".format)

# Ordenacao
idadeDemo = idadeDemo.sort_index()
print(idadeDemo)


print('\n--- Consumidores Mais Populares (Top5) ----------------------')
## Consumidores Mais Populares (Top 5)
# Cálculos básicos
totUsu = purchase_file.groupby(["Login"]).sum()["Valor"].rename("Valor total de compra")
mediaUsu = purchase_file.groupby(["Login"]).mean()["Valor"].rename("Valor medio de compra")
contUsu = purchase_file.groupby(["Login"]).count()["Valor"].rename("Numero de compras")

# Dataframe para os resultados
dadoUsu = pd.DataFrame({"Valor total de compra": totUsu, "Valor medio de compra": mediaUsu, "Numero de compras": contUsu})

# Data Munging
dadoUsu ["Valor total de compra"] = dadoUsu["Valor total de compra"].map("${:,.2f}".format)
dadoUsu ["Valor medio de compra"] = dadoUsu["Valor medio de compra"].map("${:,.2f}".format)
print(dadoUsu.sort_values("Valor total de compra", ascending=False).head(5))


print('\n--- Itens Mais Populares (Top5) ---------------------------')
## Itens Mais Populares
# Cálculos básicos
totUsu = purchase_file.groupby(["Nome do Item"]).sum()["Valor"].rename("Valor total de compra")
mediaUsu = purchase_file.groupby(["Nome do Item"]).mean()["Valor"].rename("Valor medio de compra")
contUsu = purchase_file.groupby(["Nome do Item"]).count()["Valor"].rename("Numero de compras")

# Dataframe para os resultados
dadoUsu = pd.DataFrame({"Valor total de compra": totUsu, "Valor medio de compra": mediaUsu, "Numero de compras": contUsu})

# Data Munging
dadoUsu ["Valor total de compra"] = dadoUsu["Valor total de compra"].map("${:,.2f}".format)
dadoUsu ["Valor medio de compra"] = dadoUsu["Valor medio de compra"].map("${:,.2f}".format)
print(dadoUsu.sort_values("Numero de compras", ascending=False).head(5))


print('\n--- Itens Mais Lucrativos (Top5) -------------------------')
## Itens Mais Lucrativos
totUsu = purchase_file.groupby(["Nome do Item"]).sum()["Valor"].rename("Valor total de compra")
mediaUsu = purchase_file.groupby(["Nome do Item"]).mean()["Valor"].rename("Valor medio de compra")
contUsu = purchase_file.groupby(["Nome do Item"]).count()["Valor"].rename("Numero de compras")

# Dataframe para os resultados
dadoUsu = pd.DataFrame({"Valor total de compra": totUsu, "Valor medio de compra": mediaUsu, "Numero de compras": contUsu})

# Data Munging
dadoUsu ["Valor total de compra"] = dadoUsu["Valor total de compra"].map("${:,.2f}".format)
dadoUsu ["Valor medio de compra"] = dadoUsu["Valor medio de compra"].map("${:,.2f}".format)
dadoUsu.sort_values("Numero de compras", ascending=False).head(5)
print(dadoUsu.sort_values("Valor total de compra", ascending=False).head(5)[['Valor total de compra','Valor medio de compra','Numero de compras']])
