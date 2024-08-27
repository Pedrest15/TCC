import gdown


class Files:
    @staticmethod
    def download_from_gdrive(url,output_name):
        id = url
        output = output_name
        gdown.download(id=id, output=output, quiet=True)
    
        return

    @staticmethod
    def generate_llm_response_file(model:str,PL:str, num_article:int, execution_time_minutes:float, num_tokens:int, llm_response:str,
                                   temperature:float, num_amendments:int, chain_name:str, route_id:int):
        with open(f'../agrupamentos/config{route_id}/temp{temperature}/{model}/{PL}_art_{num_article}.txt','w', encoding='utf-8') as f:
            f.write(f"###############   Agrupamento Semântico   ###############\n")
            f.write(f"==>PL: {PL}.\n")
            f.write(f"==>Artigo: {num_article}.\n")
            f.write(f"==>LLM: {model}.\n")
            f.write(f"==>Total de emendas: {num_amendments}.\n")
            f.write(f"==>Número de tokens: {num_tokens}.\n")
            f.write(f"==>Chain: {chain_name}.\n")
            f.write(f"==>Tempo de execução: {execution_time_minutes:.2f} min.\n")
            f.write(f"#########################################################\n\n")
            f.write(llm_response)

        return