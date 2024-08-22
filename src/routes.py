import time

from amendments import Amendments
from models import ModelsOllama
from chain import SimpleChain, PydanticChain
from summarizing import Text
from files import Files


class RoutesConfig:
    def __init__(self, pl:str, article:int, route_id:int=1, model:str=ModelsOllama.LLAMA3):
        self.pl = pl
        self.article = article
        self.model = model
        self.route_id = route_id
        
    def execute(self):
        arq_name = f"../arqs_base/emendas_{self.pl}_artigo{self.article}"

        amendments = Amendments(pl=self.pl, article=self.article, arq_name=arq_name)
        num_amendments = amendments.count_amendments()
        text_tools = Text()

        for temp in [0,0.25,0.5,0.75,1]:
            if self.route_id == 1:
                chain, num_tokens, input_text = self.config1(amendments, text_tools, temp)
            elif self.route_id == 2:
                chain, num_tokens, input_text = self.config2(amendments, text_tools, temp)
            elif self.route_id == 3:
                chain, num_tokens, input_text = self.config3(amendments, text_tools, temp)
            elif self.route_id == 4:
                chain, num_tokens, input_text = self.config4(amendments, text_tools, temp)
            elif self.route_id == 5:
                chain, num_tokens, input_text = self.config5(amendments, text_tools, temp)
            elif self.route_id == 6:
                chain, num_tokens, input_text = self.config6(amendments, text_tools, temp)
            elif self.route_id == 7:
                chain, num_tokens, input_text = self.config7(amendments, text_tools, temp)

            chain.make()

            t0 = time.time()
            response = chain.ask(amendments=input_text)
            tf = time.time()
            execution_time_minutes = (tf - t0) / 60

            Files.generate_llm_response_file(model=self.model,PL=self.pl, num_article=self.article, num_tokens=num_tokens, execution_time_minutes=execution_time_minutes,
                        llm_response=response, temperature=temp, num_amendments=num_amendments, chain_name=chain.name)
    
    def config1(self, amendments:Amendments, text_tools:Text, temp=0):
        num_tokens = text_tools.tokens_calculator(amendments.text)
        
        model = ModelsOllama.connect(model_name=self.model, temperature=temp)
        chain = SimpleChain(model=model)

        return chain, num_tokens, amendments.text

    def config2(self, amendments:Amendments, text_tools:Text, temp=0):
        model = ModelsOllama.connect(model_name=self.model, temperature=temp)
        chain = SimpleChain(model)

        input_text = Text.preprocess_text(amendments.text)
        num_tokens = text_tools.tokens_calculator(input_text)

        return chain, num_tokens, input_text
    
    def config3(self, amendments:Amendments, text_tools:Text, temp=0):
        num_tokens = text_tools.tokens_calculator(amendments.text)
        
        model = ModelsOllama.connect(model_name=self.model, temperature=temp)
        chain = PydanticChain(model)

        return chain, num_tokens, amendments.text
    
    def config4(self, amendments:Amendments, text_tools:Text, temp=0):
        model = ModelsOllama.connect(model_name=self.model, temperature=temp)
        chain = PydanticChain(model)

        input_text = Text.preprocess_text(amendments.text)
        num_tokens = text_tools.tokens_calculator(input_text)

        return chain, num_tokens, input_text
    
    def config5(self, amendments:Amendments, text_tools:Text, temp=0):
        model = ModelsOllama.connect(model_name=self.model, temperature=temp)
        chain = SimpleChain(model)

        summarize_text = []
        for id, amendment in zip(amendments.df['NUMEROEMENDA'], amendments.df['TEXTOPROPOSTOEMENDA']):
            summarize_text.append([id, text_tools.summarize(amendment)])

        input_text = "Faça o agrupamento semântico de:\n\n".join([f"RESUMO EMENDA ID {numero_emenda}:\n{resumo_emenda}\n\n" for numero_emenda, resumo_emenda in zip(summarize_text)])
        num_tokens = text_tools.tokens_calculator(input_text)

        return chain, num_tokens, input_text
    
    def config6(self, amendments:Amendments, text_tools:Text, temp=0):
        model = ModelsOllama.connect(model_name=self.model, temperature=temp)
        chain = SimpleChain(model)

        summarize_text = []
        for id, amendment in zip(amendments.df['NUMEROEMENDA'], amendments.df['TEXTOPROPOSTOEMENDA']):
            summarize_text.append([id, text_tools.summarize(amendment)])

        text = "Faça o agrupamento semântico de:\n\n".join([f"RESUMO EMENDA ID {numero_emenda}:\n{resumo_emenda}\n\n" for numero_emenda, resumo_emenda in zip(summarize_text)])
        input_text = text_tools.preprocess_text(text)
        num_tokens = text_tools.tokens_calculator(input_text)

        return chain, num_tokens, input_text
    
    def config7(self, amendments:Amendments, text_tools:Text, temp=0):
        model = ModelsOllama.connect(model_name=self.model, temperature=temp)
        chain = PydanticChain(model)

        summarize_text = []
        for id, amendment in zip(amendments.df['NUMEROEMENDA'], amendments.df['TEXTOPROPOSTOEMENDA']):
            summarize_text.append([id, text_tools.summarize(amendment)])

        input_text = "Faça o agrupamento semântico de:\n\n".join([f"RESUMO EMENDA ID {numero_emenda}:\n{resumo_emenda}\n\n" for numero_emenda, resumo_emenda in zip(summarize_text)])
        num_tokens = text_tools.tokens_calculator(input_text)

        return chain, num_tokens, input_text
    
    def config8(self, amendments:Amendments, text_tools:Text, temp=0):
        model = ModelsOllama.connect(model_name=self.model, temperature=temp)
        chain = PydanticChain(model)

        summarize_text = []
        for id, amendment in zip(amendments.df['NUMEROEMENDA'], amendments.df['TEXTOPROPOSTOEMENDA']):
            summarize_text.append([id, text_tools.summarize(amendment)])

        text = "Faça o agrupamento semântico de:\n\n".join([f"RESUMO EMENDA ID {numero_emenda}:\n{resumo_emenda}\n\n" for numero_emenda, resumo_emenda in zip(summarize_text)])
        input_text = text_tools.preprocess_text(text)
        num_tokens = text_tools.tokens_calculator(input_text)

        return chain, num_tokens, input_text

            
        