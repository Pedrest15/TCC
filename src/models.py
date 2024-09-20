from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from transformers import BertTokenizer, BertModel
from torch import no_grad
import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

class EmbModel:

    def __init__(self, model_name:str="neuralmind/bert-base-portuguese-cased"):
        self.tokenizer = BertTokenizer.from_pretrained(model_name, clean_up_tokenization_spaces=True)
        self.model = BertModel.from_pretrained(model_name)

    def embed(self, text: str):
        inputs = self.tokenizer(text, return_tensors='pt', padding=True)
        
        with no_grad():
            outputs = self.model(**inputs)

        emb = outputs.last_hidden_state.mean(dim=1).numpy()[0]

        return emb
    
    def emb_len(self):
        return 768

class Models:
    llama_models = ["llama3","llama3.1"]

    openAI_models = ["gpt-4o","gpt-4-turbo","gpt-3","gpt-4","gpt-3.5-turbo","gpt-4o-mini"]

    def connect(self, model_name, temperature):
        if model_name in self.llama_models:
            model = ChatOllama(model=model_name, temperature=temperature)
        elif model_name in self.openAI_models:
            model = ChatOpenAI(model=model_name, temperature=temperature, openai_api_key=os.getenv("OPEN_AI_KEY",""))

        return model

class Templates:
    SIMPLE_TEMPLATE = """Você é um assistente de IA especializado no setor legislativo e com a tarefa de agrupar de forma semântica as emendas parlamentares fornecidas pelo usuário e gerar os grupos contendo o tópico desse grupo e as emendas contidas nele. 
    <Restrictions> 
    1. SEMPRE gere os grupos em português e enumerados de forma crescente.
    2. Cada emenda deve aparecer SOMENTE em um único grupo.
    3. Gere o tópico de cada grupo de forma sucinta, em no máximo uma frase.
    4. A saída deve SEMPRE escrever SOMENTE conforme o seguinte formato:
        Grupo X1: Tópico de X1.
            Emenda Y1; Emenda Y2; Emenda Y3.
        Grupo X2: Tópico de X2.
            Emenda Y4; Emenda Y5.
    5. Independente do tamanho da entrada, sempre siga estritamente o formato especificado.
    </Restrictions>
    """

    PYDANTIC_TEMPLATE = """Você é um assistente de IA especializado no setor legislativo e com a tarefa de agrupar de forma semântica as emendas parlamentares fornecidas pelo usuário e gerar os grupos contendo o tópico desse grupo e as emendas contidas nele. 
    <Restrictions> 
    1. SEMPRE gere os grupos em português.
    2. Cada emenda deve aparecer SOMENTE em um único grupo. Apenas inclua as emendas, NÃO explique porque ela está no grupo.
    3. NÃO pode haver grupo sem emendas nele.
    4. NÂO invente emendas, use apenas as passadas a você e os respectivos IDs delas.
    5. Gere o tópico de cada grupo de forma sucinta, em no máximo uma frase.
    6. A saída deve seguir EXTRITAMENTE o formato:
    {format_instructions}
    </Restrictions>

    As emendas estão abaixo:
    {amendments}
    """

    SUMMARIZE_TEMPLATE = """Sumarize a emenda parlamentar a seguir. Retorne o sumário em um único parágrafo abrangendo os pontos principais que foram identificados no texto:
    {original_text}
    RESUMO:
    """

    CLUSTER_QUERY = """Faça o agrupamento semântico de:\n"""