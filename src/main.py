import gdown
import time

from amendments import Amendments
from models import ModelsOllama
from chain import SimpleChain, PydanticChain

def download_from_gdrive(url,output_name):
    id = url
    output = output_name
    gdown.download(id=id, output=output, quiet=True)
    
    return

def generate_file(model,PL, num_article, execution_time_minutes, num_tokens, llm_response, temperature:float, num_amendments:int,chain_name:str):
    with open(f'../agrupamentos/{model}/{chain_name}/temp{temperature}_{PL}_art_{num_article}.txt','w', encoding='utf-8') as f:
        f.write(f"###############\tAgrupamento Semântico\t###############\n")
        f.write(f"==>PL: {PL}.\n")
        f.write(f"==>Artigo: {num_article}.\n")
        f.write(f"==>LLM: {model}.\n")
        f.write(f"==>Total de emendas: {num_amendments}.\n")
        f.write(f"==>Número de tokens: {num_tokens}.\n")
        f.write(f"==>Chain: {chain_name}.\n")
        f.write(f"==>Tempo de execução: {execution_time_minutes} min.\n\n")
        f.write(llm_response)

    return

if __name__ == '__main__':
    PL = "PL-280-2020"
    num_article = 21
    arq_name = f"../arqs_base/emendas_{PL}_artigo{num_article}"

    amendments = Amendments(pl=PL,article=num_article,arq_name=arq_name)
    num_tokens = amendments.tokens_calculator()
    num_amendments = amendments.count_amendments()

    for temp in [0]:#,0.25,0.5,0.75,1]:
        model = ModelsOllama.connect(model_name=ModelsOllama.LLAMA3,temperature=temp)
        #chain = SimpleChain(model=model)
        chain = PydanticChain(model)
        chain.make()

        t0 = time.time()
        response = chain.ask(amendments=amendments.text)
        tf = time.time()
        execution_time_minutes = (tf - t0) / 60

        generate_file(model=model,PL=PL, num_article=num_article, num_tokens=num_tokens, execution_time_minutes=execution_time_minutes,
                      llm_response=response, temperature=temp, num_amendments=num_amendments, chain_name=chain.name)



