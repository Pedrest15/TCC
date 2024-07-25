from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain.vectorstores.utils import filter_complex_metadata
from langchain.prompts.chat import (
  ChatPromptTemplate,
  SystemMessagePromptTemplate,
  AIMessagePromptTemplate,
  HumanMessagePromptTemplate,
)
import os
import gdown
import pandas as pd

def download_from_gdrive(url,output_name):
    id = url
    output = output_name
    gdown.download(id=id, output=output, quiet=True)
    
    return

def get_template():
    template="""Responda em português.
    Tarefa: Agrupamento Semântico de Emendas Parlamentares
    Você foi designado para realizar um agrupamento semântico das emendas parlamentares. As emendas podem abordar uma variedade de tópicos, mas cada emenda deve aparecer em apenas um grupo, conforme seu tópico principal. Seu modelo deve atribuir cada emenda a um grupo semântico com base em seus tópicos principais. Todas as emendas são referentes ao mesmo projeto de lei, PL. Certifique-se de que cada emenda seja atribuída a um único grupo e que todas as emendas sejam atribuídas a um grupo.
    Texto do PL: {context}
    Pergunta: {input}"""

    return template

def get_query(emendas):
    return f"""Faça o agrupamento semântico das seguintes emendas: {emendas}"""

class MyChat:

    def __init__(self,model:str,template:str):
        self.vector_store = None
        self.retriever = None
        self.chain = None
        self.model = ChatOllama(model=model)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
        self.prompt = PromptTemplate.from_template(template)


    def ingest(self, pdf_file_path: str):
        docs = PyPDFLoader(file_path=pdf_file_path).load()
        chunks = self.text_splitter.split_documents(docs)
        return filter_complex_metadata(chunks)

    def make_vector_store(self, pdf_file_path:str):
        chunks = self.ingest(pdf_file_path)
        embedding_fn = FastEmbedEmbeddings()

        self.vector_store = Chroma.from_documents(documents=chunks, embedding=embedding_fn)

    def make_chain(self):
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 3,
                "score_threshold": 0.5,
            },
        )

        self.chain = ({"context": lambda x: self.retriever,"input":RunnablePassthrough()}
                        | self.prompt
                        | self.model
                        | StrOutputParser())

    def ask(self, query: str):

        return self.chain.invoke(query)

    def clear(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None

if __name__ == '__main__':
    PL = "PL-280-2020.pdf"
    nome_emendas = "emendas_PL-280-2020_artigo21.csv"
    num_artigo = 21
    model = "llama3"

    if not os.path.isfile(PL):
        download_from_gdrive("1MlHznaj9HV-Sz-OdHbc3528ASnL55YN2",PL)
    if not os.path.isfile(nome_emendas):
        download_from_gdrive("1IwHU_Z0oNr6ex1Bj2m0A8n1bglctQeD0",nome_emendas)

    emendas_df = pd.read_csv(nome_emendas)
    try:
        emendas = "".join([f"AQUI SE INICIA A EMENDA ID {numero_emenda}:{text_proposto_emenda} " for numero_emenda, text_proposto_emenda in zip(emendas_df['NUMEROEMENDA'], emendas_df['TEXTOPROPOSTOEMENDA'])])
    except MemoryError:
        print("Erro de memória.")

    template = get_template()
    chat = MyChat(model,template)
    chat.make_vector_store(PL)
    chat.make_chain()

    query = get_query(emendas)

    response = chat.ask(query)

    with open('agrupamento.txt','w') as f:
        f.write("==>Agrupamento feito pelo LLM Llama3-7B para as emendas referentes ao artigo 52 do PL476/2018.<==\n")
        f.write(response)



