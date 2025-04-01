# Sistema E-Commerce de Produtos Esportivos

Este projeto é um sistema de e-commerce desenvolvido para a venda de produtos esportivos, utilizando tecnologias como HTML, CSS, Python, JSON e Flask. Além disso, implementa estruturas de dados avançadas, como tabela de hashing e árvore B, para otimizar o desempenho e a eficiência na manipulação dos dados.

## Funcionalidades
- __Catálogo de Produtos:__ Exibição de uma lista de produtos esportivos disponíveis para compra, com detalhes como categoria, tipo, marca, modelo, cor, valor e estoque.​
- __Carrinho de Compras:__ Permite aos usuários adicionar produtos ao carrinho, especificar quantidades, visualizar os itens selecionados e calcular o subtotal da compra.​
- __Gerenciamento de Estoque:__ Atualização dinâmica do estoque disponível conforme os produtos são adicionados ou removidos do carrinho.​
- __Cálculo de Frete:__ Funcionalidade para estimar o custo de entrega com base no local fornecido pelo usuário.​
- __Finalização de Pedido:__ Processo simplificado para concluir a compra e registrar o pedido.​
- __Mapeamento de Localização:__ Integração com mapas para exibir a localização da entrega ou da loja.

## Tecnologias Utilizadas

- FrontEnd: HTML, CSS, JS e Leaflet
- Backend: Python com Flask e Json para persistir os dados
- Estrutura de Dados: Tabela hashing, árvore B e Graphos

## Estrutura do Projeto

- templates/ : Contêm os arquivos HTML que compõem a página
- static/ : Contêm o arquivo CSS + Mapa.html (leaflet)
- src/ : imagens e instrução do trabalho
- main.py : Arquivo principal que define as rotas e lógica usando flask
- ArvoreB.py : Arquivo que gera árvore B, para maior eficiência na busca.
- catalogo.json : Onde fica armazenado os produtos
- carrinho: Json que exibe os produtos no carrinho

## Como Executar

1. Faça clone do projeto
2. Baixe as dependências necessárias, como o flask
3. execute o arquivo __'main.py'__
4. acesse o __'http://localhost:5000'__

## Contato:

Gabriel Rodrigues:
- Email: gabrielcsro@gmail.com
- Linkedin: https://www.linkedin.com/in/gabriel-rodrigues-a551012a2/

Luiz Vinícius:
- Email: luizvinicius128@gmail.com
- Linkedin: https://www.linkedin.com/in/luizvn/