import time

from amendments import Amendments
from models import Models
from chain import PydanticChain
from summarizing import Text
from files import Files

class RoutesConfig:
    def __init__(self, model:str, pl:str, article:int, route_id:int=1):
        self.pl = pl
        self.article = article
        self.route_id = route_id
        self.model = model
        self.chain = None
        
    def execute(self, temp:float):
        arq_name = f"../arqs_base/emendas_{self.pl}_artigo{self.article}"

        amendments = Amendments(pl=self.pl, article=self.article, arq_name=arq_name)
        num_amendments = amendments.count_amendments()
        text_tools = Text()

        t0 = time.time()

        if self.route_id == 1:
            num_tokens, input_text = self.config1(amendments, text_tools)
        elif self.route_id == 2:
            num_tokens, input_text = self.config2(amendments, text_tools)
        elif self.route_id == 3:
            num_tokens, input_text = self.config3(amendments, text_tools)
        elif self.route_id == 4:
            num_tokens, input_text = self.config4(amendments, text_tools)

        self.chain = self.create_chain(temp=temp)

        self.chain.make()

        response = self.chain.ask(amendments=input_text).Agrupamento
        tf = time.time()
        execution_time = (tf - t0)

        Files.generate_llm_response_file(model=self.model,PL=self.pl, num_article=self.article, num_tokens=num_tokens, execution_time=execution_time,
                    llm_response=response, temperature=temp, num_amendments=num_amendments, chain_name=self.chain.name, route_id=self.route_id)
        
        return response
    
    def create_chain(self, temp=0):
        model = Models().connect(model_name=self.model, temperature=temp)
        chain = PydanticChain(model)

        return chain

    def config1(self, amendments:Amendments, text_tools:Text):
        """
            Config1: Fluxo de chain com travas de Pydantic com texto proposto das emendas completo.
        """        
        num_tokens = text_tools.tokens_calculator(amendments.text)

        return num_tokens, amendments.text
    
    def config2(self, amendments:Amendments, text_tools:Text):
        """
            Config2: Fluxo de chain com travas de Pydantic com texto proposto das emendas pre-processado.
        """
        input_text = amendments.pre_process_text()
        num_tokens = text_tools.tokens_calculator(input_text)

        return num_tokens, input_text
    
    def config3(self, amendments:Amendments, text_tools:Text):
        """
            Config3: Fluxo de chain com travas de Pydantic com texto proposto das emendas resumidas.
        """
        input_text = amendments.summarize(model_name=self.model)
        num_tokens = text_tools.tokens_calculator(input_text)

        return num_tokens, input_text
    
    def config4(self, amendments:Amendments, text_tools:Text):
        """
            Config4: Fluxo de chain com travas de Pydantic com texto proposto das emendas resumidas e pre-processadas.
        """
        input_text = amendments.pre_process_summarized(model_name=self.model)
        num_tokens = text_tools.tokens_calculator(input_text)

        return num_tokens, input_text

            
        