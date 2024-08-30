# Usar uma imagem base do Python
FROM python:3.12-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos de dependências e instalá-las
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do projeto para o container
COPY . .

# Expôr a porta 8000 para o FastAPI
EXPOSE 8000

# Comando para rodar a aplicação FastAPI, já que o main.py está na raiz
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]