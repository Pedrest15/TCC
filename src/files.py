import gdown


class Files:
    @classmethod
    def download_from_gdrive(url,output_name):
        id = url
        output = output_name
        gdown.download(id=id, output=output, quiet=True)
    
        return

    @classmethod
    def generate_llm_response_file(model,PL, num_article, execution_time_minutes, num_tokens, llm_response, temperature:float, num_amendments:int,chain_name:str):
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