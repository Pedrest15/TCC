import matplotlib.pyplot as plt

def create_chart(pl:str, article:str|int, data:dict, metric_name:str):
    labels = list(data.keys())
    print(f"labels {labels}")
    metric = list(data.values())

    plt.clf()
    plt.bar(labels, metric)

    # Adicionar titulo e rotulos
    plt.title(f"{metric_name} {pl} - Art {article}")
    plt.xlabel('Temperatura')
    plt.ylabel(metric_name)

    # Salvar grafico
    plt.savefig(f'../imgs/{pl}_artigo{article}_{metric_name}.png', format='png', dpi=300)
