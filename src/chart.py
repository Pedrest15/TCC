import matplotlib.pyplot as plt

def create_chart(pl:str, article:str|int, model:str, config:str|int, data:dict, metric_name:str, color:str='blue'):
    labels = list(data.keys())
    metric = [float(value) for value in data.values()]

    plt.clf()
    plt.plot(labels, metric, marker='o', linewidth=0.5, color=color)
    plt.ylim(0, 1)
    plt.yticks([i/10 for i in range(0, 11)])

    # Adicionar titulo e rotulos
    plt.title(f"Config{config}: {pl} - Art {article} p/ {model}")
    plt.xlabel('Temperatura')
    plt.ylabel(metric_name)

    for x, y in zip(labels, metric):
        plt.text(x, y, f'{round(y, 2)}', ha='center', va='bottom')

    # Salvar grafico
    #plt.show()
    plt.savefig(f'../imgs/{model}/{model}_config{config}_{metric_name}_{pl}_art{article}.png', format='png', dpi=300)

def compare_llms(pl:str, article:str|int, config:str|int, models:list[str], data1:dict, data2:dict, metric_name:str, colors:list[str]):
    labels = list(data1.keys())
    
    metric1 = [float(value) for value in data1.values()]
    metric2 = [float(value) for value in data2.values()]

    plt.clf()
    plt.plot(labels, metric1, marker='o', linewidth=0.5, color=colors[0])
    plt.plot(labels, metric2, marker='o', linewidth=0.5, color=colors[1])
    plt.ylim(0, 1)
    plt.yticks([i/10 for i in range(0, 11)])

    plt.show()
