# Agrupamento Semântico no Contexto de Emendas Legislativas

## Resumo

Este trabalho explora a realização de agrupamento semântico de emendas legislativas brasileiras por meio de Large Language Models. Considerando o número elevado de emendas redigidas anualmente na Câmara dos Deputados Federal e no Senado Federal e a consequente carga horária massiva despendida pelas equipes responsáveis por agrupar tais documentos, o uso de técnicas automatizadas para análise e organização eficientes apresenta-se como uma alternativa benéfica às casas legislativas. A partir dos modelos GPT-4o e GPT-4o-mini da OpenAI, realizaramse experimentos visando agrupar emendas conforme sua similaridade semântica. O estudo comparou abordagens com e sem pré-processamento textual, variando o valor da temperatura do modelo para avaliar o impacto deste parâmetro sobre a qualidade do resultado final. Como forma de validar a eficácia dos grupos formados, as métricas de precisão, recall e F1 foram aplicadas. Constatou-se que o modelo GPT-4o apresentou desempenho superior, sobretudo com temperaturas inferiores. Não obstante, este estudo foi limitado pelos custos de infraestrutura e a propensão dos modelos a alucinarem durante sua execução. Os resultados obtidos indicam potencial dos modelos em auxiliar a tarefa de agrupar emendas, oferecendo subsídios para futuras melhorias no uso de Inteligência Artificial no contexto legislativo brasileiro.

## Estrutura do Código

- amendments.py: contém a classe Amendments, responsável por carregar os dados e manipular.
- chain.py: contém as classes
    - Chain: estrutura padrão da cadeia de conversa com LLM.
    - SimpleChain: cria uma cadeia básica.
    - ClusterContent: BaseModel com os campos que cada cluster deve ter, tema e lista de emendas.
    - Cluster: BaseModel do agrupamento inteiro, é uma lista de clusters.
    - PydanticChain: cria uma cadeia em que a saída gerada pelo LLM deve seguir o formato de Cluster.
- chart.py: contém funções geradoras de gráficos.
- files.py: contém a classe Files, uma junção de funções estáticas que maipulam arquivos, leitura e escrita.
- main.py: arquivo principal, contém os passos do pipeline de execução.
- models.py: contém as classes
    - EmbModel: responsável por transformar texto em embeddings.
    - Models: instancia o modelo LLM.
    - Templates: armazena todas os templetes usados.
- routes.py: contém a classe RoutesConfig, ela direciona a execução conforme a configuração adotada, com pré-processamento ou sem.
- score.py: contém a classe Score, responsável por medir a performence da execução por meio do BERTScore.
summarizing.py: contém a classe Text, responsável por pré-processar o texto, bem como fazer o resumo das emendas.