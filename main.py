import pandas as pd
import sqlite3
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import sqlite3


def buscalink():
    url = "https://lista.mercadolivre.com.br/games/consoles/sony/playstation-5/play5_NoIndex_True"
    response = requests.get(url)
    return response.text

def proximo(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    for link in soup.find_all('a',class_='andes-pagination__link'):
        if link.text.strip()=='Seguinte':
            url= (link.get('href')) 
    response = requests.get(url)
    return response.text

def seguinte(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    for link in soup.find_all('a',class_='andes-pagination__link'):
        if link.text.strip()=='Seguinte':
            url= (link.get('href')) 
    # response = requests.get(url)
    return url


def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    #Encontrando todos os nomes dos produtos
    produtos = soup.find_all('div', class_='ui-search-result__wrapper')
    lista = []
    # Criando lista de nomes
    for produto in produtos:

        nome = produto.find('h3',class_='poly-component__title-wrapper')
        price = produto.find('span',class_='andes-money-amount andes-money-amount--cents-superscript')
        price=price.text.strip()
        lista.append({'Nome' : nome.text.strip(),'Valor':int(price.replace('R$','').replace('.','')),'Timestamp' : datetime.now().strftime("%Y-%m-%d %H:%M")})
    return lista 
    #Criando lista de nomes


# cria/ connecta o banco de dados e retorna a conxao
def cria_banco(db='PS4.db'):
    conn = sqlite3.connect(db)
    return conn


def cria_tabela(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT,
            Valor REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()

def save_to_datetme(conn,data):
    df = pd.DataFrame(data)
    df.to_sql('tes',conn ,if_exists= 'append',index=False)



def consulta(conn):
    cursor=conn.cursor()
    cursor.execute ('SELECT * FROM  tes  ')

    executar=cursor.fetchall()
    print(executar)




if __name__=="__main__":


    banco_de_dados = cria_banco()
    Tabela = cria_tabela(banco_de_dados)
    html = buscalink()
    aux=html
    contador=1
    while True:
        try:    

            # print(seguinte(aux))
 
            dados=parse_page(aux)
            # print(dados)
            aux = proximo(aux)
            save_to_datetme(banco_de_dados,dados)
            time.sleep(5)
            contador+=1

        except Exception as e:
            print(f"Erro ao buscar dados: {e}")
            break
    banco_de_dados.close()
print(contador)
    # Obtendo o HTML da página
    # banco_de_dados = cria_banco()
    # Tabela = cria_tabela(banco_de_dados)

    # print(consulta(banco_de_dados))

    # while True:
    #Extraindo os nomes dos produtos
        # html = buscalink()
        # dados = parse_page(html)
        
        # save_to_datetme(banco_de_dados,dados)
        # print('dados inseridos')


    #Criando um DataFrame com os resultados

    # banco_de_dados.close()

    #Exibindo os dados

