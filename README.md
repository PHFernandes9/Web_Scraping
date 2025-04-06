# Projeto de Web Scraping

## 📋 Descrição

Esse projeto tem como objetivo fazer uma  consulta do preço do Playstation 5, no site mercado livre e posteriormente salvar os dados em um banco de dados.

### 📖 Bibliotecas

- `Requests` : Acessar os aquivos HTML da página.
- `SQLite` : Banco de dados disponível no Python, possui a vantagem de ser leve.
- `BeautifulSoup` : 
- `pandas`: Para organizar e manipular os dados coletados.
- `datetime`: Manipulação de datas.


### Metodologia

&nbsp;

📌 Função que irá buscar as informações da página em HTML

    def buscalink():
        url = "https://lista.mercadolivre.com.br/play5#D[A:play5,L:undefined,MLB1743]"
        response = requests.get(url)
        return response.text

&nbsp;

📌 Essa função servirá para pegar alguns dados esepcíficos do html, como nome e preço. Além de acionar a data com a função datetime.


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
            lista.append({'Nome' : nome.text.strip(),'Valor':int(price.replace('R$','').replace('.','')) ,'Timestamp' : datetime.now().strftime("%Y-%m-%d %H:%M")})
        
        return lista 
        # Criando lista de nomes
