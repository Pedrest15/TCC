from langchain_community.chat_models import ChatOllama

class ModelsOllama:
    LLAMA3 = "llama3"
    LLAMA3_1 = "llama3.1"

    @classmethod
    def connect(self, model_name, temperature):
        self.model = ChatOllama(model=model_name, temperature=temperature)

        return self.model

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
    3. Gere o tópico de cada grupo de forma sucinta, em no máximo uma frase.
    4. A saída deve seguir EXTRITAMENTE o formato:
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