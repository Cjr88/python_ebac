import csv
from sys import argv
import pandas as pd
import seaborn as sns
import os
import time
import json
from random import random
from datetime import datetime
import requests

def extrair_dados_cdi():
    # Extraindo as colunas hora e taxa
    df = pd.read_csv('./taxa-cdi.csv')

    # Criando o gráfico
    grafico = sns.lineplot(x=df.index, y=df['taxa'])
    grafico.set_xticks(df.index)
    _ = grafico.set_xticklabels(labels=df['hora'], rotation=90)
    grafico.get_figure().savefig(f"{argv[1]}.png")

def capturar_taxa_cdi():
    URL = 'https://www2.cetip.com.br/ConsultarTaxaDi/ConsultarTaxaDICetip.aspx'

    for _ in range(0, 10):
        # Criando a variável data e hora
        data_e_hora = datetime.now()
        data = datetime.strftime(data_e_hora, '%Y/%m/%d')
        hora = datetime.strftime(data_e_hora, '%H:%M:%S')

        # Captando a taxa CDI do site da B3
        try:
            response = requests.get(URL)
            response.raise_for_status()
        except requests.HTTPError as exc:
            print("Dado não encontrado, continuando.")
            cdi = None
        except Exception as exc:
            print("Erro, parando a execução.")
            raise exc
        else:
            dado = json.loads(response.text)
            cdi = float(dado['taxa'].replace(',', '.')) + (random() - 0.5)

        # Verificando se o arquivo "taxa-cdi.csv" existe
        if not os.path.exists('./taxa-cdi.csv'):
            with open(file='./taxa-cdi.csv', mode='w', encoding='utf8') as fp:
                fp.write('data,hora,taxa\n')

        # Salvando dados no arquivo "taxa-cdi.csv"
        with open(file='./taxa-cdi.csv', mode='a', encoding='utf8') as fp:
            fp.write(f'{data},{hora},{cdi}\n')

        time.sleep(2 + (random() - 0.5))

    print("Sucesso")

if __name__ == "__main__":
    if len(argv) != 2:
        print("Uso: python analise.py <nome-do-grafico>")
    else:
        capturar_taxa_cdi()
        extrair_dados_cdi()
