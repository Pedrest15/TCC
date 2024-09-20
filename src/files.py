import gdown

class Files:
    @staticmethod
    def download_from_gdrive(url,output_name):
        id = url
        output = output_name
        gdown.download(id=id, output=output, quiet=True)
    
        return

    @staticmethod
    def generate_llm_response_file(model:str,PL:str, num_article:int, execution_time:float, num_tokens:int, llm_response:str,
                                   temperature:float, num_amendments:int, chain_name:str, route_id:int):
        with open(f'../agrupamentos/config{route_id}/temp{temperature}/{model}/{PL}_art_{num_article}.txt','w', encoding='utf-8') as f:
            minutes = execution_time // 60
            seconds = int(execution_time % 60)
            
            f.write(f"###############   Agrupamento Semântico   ###############\n")
            f.write(f"==>PL: {PL}.\n")
            f.write(f"==>Artigo: {num_article}.\n")
            f.write(f"==>LLM: {model}.\n")
            f.write(f"==>Total de emendas: {num_amendments}.\n")
            f.write(f"==>Número de tokens: {num_tokens}.\n")
            f.write(f"==>Chain: {chain_name}.\n")
            f.write(f"==>Tempo de execução: {minutes} min {seconds} seg.\n")
            f.write(f"#########################################################\n\n")

            for group in llm_response:
                f.write(f"Grupo: {group.tema}\n")
                f.write(f"\tEmenda ID {'; Emenda ID '.join(group.ids_emendas)}\n\n")

        return
    
    @staticmethod
    def generate_score_file(model:str,PL:str, num_article:int, route_id:int,
                            precision:dict, recall:dict, f1:dict):
        with open(f'../agrupamentos/config{route_id}/score/{model}/{PL}_art_{num_article}.txt','w', encoding='utf-8') as f:
            f.write(f"###############   Scores   ###############\n")
            f.write(f"==> PL: {PL}.\n")
            f.write(f"==> Artigo: {num_article}.\n")
            f.write(f"==> LLM: {model}.\n")
            f.write(f"==> Config: {route_id}.\n")
            f.write(f"#########################################################\n\n")

            f.write(f"Precisão:\n")
            f.write(str(precision))
            f.write("\n\n")

            f.write(f"Recall:\n")
            f.write(str(recall))
            f.write("\n\n")

            f.write(f"F1:\n")
            f.write(str(f1))

        return
    


