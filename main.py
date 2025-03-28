import pandas as pd
import sqlite3
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime


def buscalink():
    url="https://www.mercadolivre.com.br/console-sony-playstation-5-digital-slim-1tb-branco-jogos-returnal-e-ratchet-clank-controle-sem-fio-dualsense-branco/p/MLB37494438#reco_item_pos=1&reco_backend=item_decorator&reco_backend_type=function&reco_client=home_items-decorator-legacy&reco_id=5570092a-48f1-4881-b488-e4ace576e0b9&reco_model=&c_id=/home/navigation-trends-recommendations/element&c_uid=cc2ed833-602e-40f2-9ab5-602d1705ab42&da_id=navigation_trend&da_position=1&id_origin=/home/dynamic_access&da_sort_algorithm=ranker"
    response=requests.get(url)
    return response.text

def pase_page (html):
    soup=BeautifulSoup(html,'html.parser')
    nome=soup.find('h1',class_='ui-pdp-title').get_text(strip=True)
    price =soup.find('span',class_='andes-money-amount__fraction').get_text(strip=True)

    return {'Nome' : nome,
            'Preço':price,
            'Timestamp': datetime.now().strftime("%Y-%M-D")
            }


def create_db(db_name='price_ps4.db'):
    conn = sqlite3.connect(db_name)
    return conn


def criar_tabela(conn):

    cursor=conn.cursor()
    cursor.execute (

        '''
        CREATE TABLE IF NOT EXISTS PRICE  (
        
        ID PRIMARY KEY, 
        NOME TEXT,
        PRICE INTEGER,
        TIMESTAMP TEXT
        )  
     '''
    ) 
    conn.commit()

def save_to_db(conn,data):
    df = pd.DataFrame([data])
    df.to_sql('prices', conn, if_exists='append', index=False)


if __name__=="__main__":
    
    conn=create_db()
    criar_tabela(conn)


    while True:

        dados=buscalink()
        product_info=pase_page(dados)
        save_to_db(conn,product_info)
        print ('Dados salvos')
        time.sleep(10)

    conn.close
