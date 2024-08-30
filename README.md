API de Processamento de URL e Perguntas

Essa API é uma implementação de um sistema que processa URLs e perguntas utilizando tecnologias como FastAPI, OpenAI e LangChain. O sistema permite carregar URLs, processar as perguntas com base nos dados carregados e fornecer respostas.

Funcionalidades

Carregar URLs e criar embeddings.
Dividir o texto da URL.
Realizar pesquisas baseadas no conteúdo da URL.
Responder perguntas baseadas no conteúdo da URL.
Requisitos

Python 3.9 ou superior
FastAPI 0.70.0 ou superior
LangChain Community
OpenAI API Key
Instalação

Para instalar a API, você precisará ter Python 3.9 ou superior instalado na sua máquina. Em seguida, você pode executar os seguintes comandos no terminal:

pip install fastapi uvicorn langchain langchain-community llms pydantic

Executar a API

Para executar a API, execute o comando uvicorn app:app --host 0.0.0.0 --port 8000 no diretório raiz do projeto. A API estará disponível em http://localhost:8000.

Endpoints

A API tem os seguintes endpoints:

/
Método: GET
Descrição: Retorna uma mensagem de boas-vindas.
/load_url
Método: POST
Descrição: Carrega o conteúdo de uma URL e processa-o.
Requisitos:
url: A URL a ser carregada.
api_key: A chave API para autenticar a requisição.
Resposta:
message: Uma mensagem de sucesso se a URL for carregada com sucesso.
/ask
Método: POST
Descrição: Responde a uma pergunta baseada no conteúdo da URL carregada anteriormente.
Requisitos:
question: A pergunta a ser respondida.
api_key: A chave API para autenticar a requisição.
Resposta:
answer: A resposta à pergunta.
/clear_data
Método: POST
Descrição: Remove os dados do usuário.
Requisitos:
api_key: A chave API para autenticar a requisição.
Resposta:
message: Uma mensagem de sucesso se os dados forem removidos com sucesso.
Observações

A API utiliza a chave API para autenticar as requisições. Você precisará fornecer uma chave API válida para acessar os endpoints.
A API armazena os dados do usuário em memória. Se você precisar armazenar os dados em um banco de dados, você precisará implementar uma solução adicional.
A API utiliza a biblioteca LangChain e OpenAI para processar as URLs e responder às perguntas. Você pode encontrar mais informações sobre a biblioteca em https://langchain.readthedocs.io.
Modelos de Requisição

A API utiliza dois modelos de requisição:

URLRequest: Modelo para a requisição de URL
url: A URL a ser carregada
QuestionRequest: Modelo para a requisição de pergunta
question: A pergunta a ser respondida
Exemplos de Uso

Incluir a URL https://www.example.com na requisição /load_url
Fazer a pergunta O que é Python? na requisição /ask
Excluir os dados do usuário com a chave API abc123 na requisição /clear_data
