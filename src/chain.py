from typing import List

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.chat import SystemMessagePromptTemplate

from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator

from models import Templates

class Chain:
    def __init__(self, model:str):
        self.chain = None
        self.model = model
        self.name:str = None

    def clear(self):
        self.model = None
        self.chain = None

class SimpleChain(Chain):
    def __init__(self, model):
        super().__init__(model)
        self.name = 'simple_chain'

    def make(self):
        output_parser = StrOutputParser()
        system_prompt = SystemMessagePromptTemplate.from_template(template=Templates.SIMPLE_TEMPLATE)
        prompt = ChatPromptTemplate.from_messages(
            [
                system_prompt,
                ("user", "{amendments}"),
            ]
        )

        self.chain = {"amendments": RunnablePassthrough()} | prompt | self.model | output_parser

    def ask(self, amendments: str):
        return self.chain.invoke(Templates.CLUSTER_QUERY + amendments)

class ClusterContent(BaseModel):
    tema: str = Field(description='Tema do agrupamento de emendas legislativas.')
    ids_emendas: List[str] = Field(description='IDS das emendas que fazem parte do agrupamento.', unique_items=True)
    
    class Config:
        #extra = 'allow'  # Permite campos adicionais
        extra = 'ignore' #Ignora campos adicionais

class Cluster(BaseModel):
    Agrupamento: List[ClusterContent]

class PydanticChain(Chain):
    def __init__(self, model: str):
        super().__init__(model)
        self.name = 'pydantic_chain'

    def make(self):
        parser = PydanticOutputParser(pydantic_object=Cluster)
        prompt = PromptTemplate(
            template=Templates.PYDANTIC_TEMPLATE,
            input_variables=['amendments'],
            partial_variables={'format_instructions': parser.get_format_instructions()},
        )
        
        self.chain = prompt | self.model | parser

    def ask(self, amendments: str):
        return self.chain.invoke({'amendments': Templates.CLUSTER_QUERY+amendments})