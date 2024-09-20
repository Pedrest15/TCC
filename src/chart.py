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

if __name__ == '__main__':
    ### gpt-4o
    precision1 = {'0': 0.6474996, '0.25': 0.68858075, '0.5': 0.66569686, '0.75': 0.72508794, '1': 0.7027681}
    #recall = {'0': 0.6042719, '0.25': 0.58929056, '0.5': 0.57272613, '0.75': 0.6066432, '1': 0.5898588}
    #f1 = {'0': 0.62445897, '0.25': 0.6345622, '0.5': 0.61485267, '0.75': 0.66031927, '1': 0.6405766}

    #create_chart(pl='PL-280-2020', article=21, data=precision, metric_name='Precision', model='gpt-4o', color='blue', config=2)
    #create_chart(pl='PL-280-2020', article=21, data=recall, metric_name='Recall', model='gpt-4o', color='orange', config=2)
    #create_chart(pl='PL-280-2020', article=21, data=f1, metric_name='F1', model='gpt-4o', color='green', config=2)

    ### gpt-4o-mini
    precision2 = {'0': '0.6895773', '0.25': '0.7042364', '0.5': '0.6703024', '0.75': '0.67977405', '1': '0.70372677'}
    recall = {'0': '0.5672793', '0.25': '0.57350147', '0.5': '0.56349', '0.75': '0.5742512', '1': '0.5770151'}
    f1 = {'0': '0.6216754', '0.25': '0.6313098', '0.5': '0.6112579', '0.75': '0.6216759', '1': '0.633723'}

    #create_chart(pl='PL-280-2020', article=21, data=precision, metric_name='Precision', model='gpt-4o-mini', color='blue', config=2)
    #create_chart(pl='PL-280-2020', article=21, data=recall, metric_name='Recall', model='gpt-4o-mini', color='orange', config=2)
    #create_chart(pl='PL-280-2020', article=21, data=f1, metric_name='F1', model='gpt-4o-mini', color='green', config=2)

    compare_llms(pl='PL-280-2020', article=21, metric_name='Precision', config=2, models=['gpt-4o','gpt-4o-mini'], data1=precision1,
                 data2=precision2, colors=['blue', 'red'])
