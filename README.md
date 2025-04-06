# Projeto de Web Scraping

## 📋 Descrição

Esse projeto tem como objetivo fazer uma  consulta do preço do Playstation 5, no site mercado livre e posteriormente salvar os dados em um banco de dados.

### Bibliotecas

- `Requests` : Acessar os aquivos HTML da página.
- `SQLite` : Banco de dados disponível no Python, possui a vantagem de ser leve.
- `BeautifulSoup` : 
- `pandas`: Para organizar e manipular os dados coletados.



# Função para buscar o HTML da página de produtos do Mercado Livre
def buscalink():
    url = "https://lista.mercadolivre.com.br/play5#D[A:play5,L:undefined,MLB1743]"
    response = requests.get(url)
    return response.text  # Retorna o conteúdo HTML da página

# Função para extrair os dados relevantes (nome e preço) do HTML
def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')  # Faz o parser do HTML com BeautifulSoup

    produtos = soup.find_all('div', class_='ui-search-result__wrapper')  # Encontra todos os produtos listados
    lista = []

    # Loop pelos produtos encontrados
    for produto in produtos:
        nome = produto.find('h3', class_='poly-component__title-wrapper')  # Encontra o nome do produto
        price = produto.find('span', class_='andes-money-amount andes-money-amount--cents-superscript')  # Encontra o preço
        
        price = price.text.strip()  # Remove espaços em branco
        lista.append({
            'Nome': nome.text.strip(),
            'Valor': int(price.replace('R$', '').replace('.', '')),  # Remove símbolos e formata como inteiro
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")  # Adiciona a hora atual
        })

    return lista  # Retorna a lista de dicionários com os dados dos produtos

# Função que cria ou conecta ao banco de dados SQLite
def cria_banco(db='PS4.db'):
    conn = sqlite3.connect(db)
    return conn

# Função que cria a tabela no banco, caso não exista
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

# Função que insere os dados extraídos no banco de dados
def save_to_datetme(conn, data):
    df = pd.DataFrame(data)  # Converte a lista de dicionários em DataFrame
    df.to_sql('tes', conn, if_exists='append', index=False)  # Insere os dados na tabela 'tes'

# Função que consulta todos os dados da tabela e retorna como DataFrame
def consulta(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tes ORDER BY Nome')  # Seleciona todos os dados ordenados por nome
    executar = cursor.fetchall()
    df = pd.DataFrame(executar)  # Converte o resultado para DataFrame
    return df

if __name__ == "__main__":
    # Cria ou conecta ao banco de dados
    banco_de_dados = cria_banco()
    
    # Cria a tabela se ela não existir
    Tabela = cria_tabela(banco_de_dados)

    # Mostra os dados já existentes no banco
    print(consulta(banco_de_dados))

    # Código comentado para execução contínua (scraping a cada intervalo de tempo)
    # while True:
    #     html = buscalink()  # Busca o HTML da página
    #     dados = parse_page(html)  # Extrai os dados
    #     save_to_datetme(banco_de_dados, dados)  # Salva os dados no banco
    #     print('dados inseridos')
    #     time.sleep(3600)  # Espera 1 hora antes de repetir (se quiser ativar)

    # Fecha a conexão com o banco de dados (está comentado também)
    # banco_de_dados.close()
