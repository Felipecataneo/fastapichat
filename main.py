from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from langchain_community.llms import OpenAI
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from typing import Dict

app = FastAPI()

# Modelo para a requisição de URL
class URLRequest(BaseModel):
    url: str

# Modelo para a requisição de pergunta
class QuestionRequest(BaseModel):
    question: str

# Dicionário para armazenar os vectorstores por usuário
user_vectorstores: Dict[str, Chroma] = {}

# Função para obter a chave API do cabeçalho
def get_api_key(x_api_key: str = Header(...)):
    return x_api_key

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API de processamento de URL e perguntas"}

@app.post("/load_url")
async def load_url(url_request: URLRequest, api_key: str = Depends(get_api_key)):
    try:
        # Carregar o conteúdo da URL
        loader = UnstructuredURLLoader(urls=[url_request.url])
        data = loader.load()
        
        # Dividir o texto
        text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(data)
        
        # Criar embeddings e armazenar no Chroma
        embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        vectorstore = Chroma.from_documents(docs, embeddings)
        
        # Armazenar o vectorstore para este usuário
        user_vectorstores[api_key] = vectorstore
        
        return {"message": "URL loaded and processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing URL: {str(e)}")

@app.post("/ask")
async def ask_question(question_request: QuestionRequest, api_key: str = Depends(get_api_key)):
    if api_key not in user_vectorstores:
        raise HTTPException(status_code=400, detail="No URL has been loaded yet for this user")
    
    try:
        vectorstore = user_vectorstores[api_key]
        
        # Criar uma cadeia de pergunta e resposta
        qa_chain = RetrievalQA.from_chain_type(
            llm=OpenAI(openai_api_key=api_key),
            chain_type="stuff",
            retriever=vectorstore.as_retriever()
        )
        
        # Obter a resposta
        response = qa_chain.invoke(question_request.question)
        
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.post("/clear_data")
async def clear_data(api_key: str = Depends(get_api_key)):
    if api_key in user_vectorstores:
        del user_vectorstores[api_key]
        return {"message": "User data cleared successfully"}
    else:
        return {"message": "No data found for this user"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)