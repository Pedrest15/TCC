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
    Você foi designado para realizar um agrupamento semântico das emendas parlamentares. As emendas podem abordar uma variedade de tópicos, mas cada emenda deve aparecer em apenas um grupo, conforme seu tópico principal. Todas as emendas são referentes ao mesmo projeto de lei, PL. Certifique-se de que cada emenda seja atribuída a um único grupo e que todas as emendas sejam atribuídas a um grupo.
    Exemplo de Emenda:
    AQUI SE INICIA A EMENDA ID 000001 TEXTO
    Pergunta: {input}"""

    return template

def get_query(emendas):
    return f"""Realize o agrupamento semântico das emendas parlamentares fornecidas, atribuindo cada emenda a um grupo com base em seus tópicos principais. Segue as emendas: {emendas}"""

class MyChat:

    def __init__(self,model:str,template:str):
        self.chain = None
        self.model = ChatOllama(model=model)
        self.prompt = PromptTemplate.from_template(template)

    def make_chain(self):

        self.chain = ({"input":RunnablePassthrough()}
                        | self.prompt
                        | self.model
                        | StrOutputParser())

    def ask(self, query: str):

        return self.chain.invoke(query)

if __name__ == '__main__':
    nome_emendas = "emendas_PL-280-2020_artigo21.csv"
    num_artigo = 21
    model = "llama3"

    if not os.path.isfile(nome_emendas):
        download_from_gdrive("1IwHU_Z0oNr6ex1Bj2m0A8n1bglctQeD0",nome_emendas)

    emendas_df = pd.read_csv(nome_emendas)
    try:
        emendas = "".join([f"AQUI SE INICIA A EMENDA ID {numero_emenda}:{text_proposto_emenda} " for numero_emenda, text_proposto_emenda in zip(emendas_df['NUMEROEMENDA'], emendas_df['TEXTOPROPOSTOEMENDA'])])
    except MemoryError:
        print("Erro de memória.")

    template = get_template()
    chat = MyChat(model,template)
    chat.make_chain()

    query = get_query(emendas)
    response = chat.ask(query)

    with open('agrupamentoSemRAG.txt','w') as f:
        f.write("==>Agrupamento feito pelo LLM Llama3-7B para as emendas referentes ao artigo 52 do PL476/2018.<==\n")
        f.write(response)



