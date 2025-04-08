# 🕸️ Projeto de Web Scraping

## 📋 Descrição

Esse projeto tem como objetivo fazer uma  consulta do preço do Playstation 5, no site mercado livre e posteriormente salvar os dados em um banco de dados.

### 📖 Bibliotecas

- `Requests` : Acessar os aquivos HTML da página.
- `SQLite` : Banco de dados disponível no Python, possui a vantagem de ser leve.
- `BeautifulSoup` : 
- `pandas`: Para organizar e manipular os dados coletados.
- `datetime`: Manipulação de datas.


#### Aquisição dos dados do HTML

- Função que irá buscar as informações da página em HTML

        def buscalink():
            url = "https://lista.mercadolivre.com.br/play5#D[A:play5,L:undefined,MLB1743]"
            response = requests.get(url)
            return response.text

##### Esta função acessa a página de listagem de "Playstation 5" no Mercado Livre e retorna o conteúdo HTML para ser processado.

&nbsp;
### 🧠 Função para processar e extrair os dados
        def parse_page(html):
            soup = BeautifulSoup(html, 'html.parser')
        
            # Encontrando todos os nomes dos produtos
            produtos = soup.find_all('div', class_='ui-search-result__wrapper')
            lista = []
            # Criando lista de nomes
            for produto in produtos:
        
                nome = produto.find('h3',class_='poly-component__title-wrapper')
                price = produto.find('span',class_='andes-money-amount andes-money-amount--cents-superscript')
                price=price.text.strip()
                lista.append({'Nome' : nome.text.strip(),'Valor':int(price.replace('R$','').replace('.','')),
                'Timestamp' : datetime.now().strftime("%Y-%m-%d %H:%M")})
            
        return lista 
        # Criando lista de nomes
        
##### Esta função pega os elementos HTML que contêm o nome e o valor de cada produto e cria um dicionário com esses dados, incluindo a data e hora da coleta. Todos os resultados são adicionados a uma lista que é retornada ao final.

&nbsp;

### 🗃️  Banco de dados
### 🔧 Função para criar ou conectar ao banco de dados

- Cria um banco de dados ou então conecta se ele já existir.

            def cria_banco(db='PS4.db'):
                conn = sqlite3.connect(db)
                return conn
##### Essa função cria (ou se conecta, caso já exista) a um banco de dados SQLite com o nome especificado (por padrão, PS4.db).

### 🏗️- Cria a tabela dentro do banco de dados SQlite. 
        
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
##### Esta função garante que a tabela chamada tes exista no banco de dados, com os campos necessários para armazenar as informações dos produtos.
