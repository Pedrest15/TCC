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

class MyChat:

    def __init__(self,model:str):
        self.vector_store = None
        self.retriever = None
        self.chain = None
        self.model = ChatOllama(model=model)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)

    def ingest(self, pdf_file_path: str):
        docs = PyPDFLoader(file_path=pdf_file_path).load()
        chunks = self.text_splitter.split_documents(docs)
        return filter_complex_metadata(chunks)

    def make_vector_store(self, pdf_file_path:str):
        chunks = self.ingest(pdf_file_path)
        embedding_fn = FastEmbedEmbeddings()

        self.vector_store = Chroma.from_documents(documents=chunks, embedding=embedding_fn)

    def make_chain(self,template:str):
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 3,
                "score_threshold": 0.5,
            },
        )

        sys_message_prompt= SystemMessagePromptTemplate.from_template(template)
        example_human_history = HumanMessagePromptTemplate.from_template("Olá!")
        example_ai_history = AIMessagePromptTemplate.from_template("Oi, como você está hoje?")

        human_template="{input}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        chat_prompt = ChatPromptTemplate.from_messages([sys_message_prompt, example_human_history, example_ai_history, human_message_prompt])

        self.chain = chat_prompt | self.model

    def ask(self, query:str,emendas:str):
        return self.chain.invoke({"context": self.retriever,"emendas":emendas,"input":query})

    def clear(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None


