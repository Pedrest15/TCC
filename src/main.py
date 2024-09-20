from routes import RoutesConfig
from score import CV_Coherence, Score
from files import Files
from chart import create_chart

def choose_route():
    print("################   Agrupamento Semântico de Emendas Parlamentares   ################")
    print()
    print("1- Fluxo de chain com texto proposto das emendas completo.")
    print("2- Fluxo de chain com texto proposto das emendas pre-processado.")
    print("3- Fluxo de chain com texto proposto das emendas resumidas.")
    print("4- Fluxo de chain com texto proposto das emendas resumidas e pre-processadas.")
    print()
    route = int(input("Qual configuração de rota você gostaria de executar? "))

    return route

def choose_model():
    print()
    print("### Qual modelo deseja utilizar? ###")
    print()
    print("1- llama3")
    print("2- llama3.1")
    print("3- gpt4o")
    print("4- gpt-4o-mini")
    print()
    model_id = int(input(""))

    models = ["llama3", "llama3.1", "gpt-4o", "gpt-4o-mini"]

    return models[model_id-1]

def main():
    route = choose_route()
    model = choose_model()   

    PL = "PL-280-2020"
    num_article = 21

    temps = [0,0.25,0.5,0.75,1]
    precision = {}
    recall = {}
    f1 = {}

    for temp in temps:
        groups = RoutesConfig(model=model, pl=PL, article=num_article, route_id=route).execute(temp=temp)
        
        p,r,f = Score(pl=PL, article=num_article).execute(groups=groups, route=route)

        precision[temp] = p
        recall[temp] = r
        f1[temp] = f

    print(precision)

    Files.generate_score_file(model=model, PL=PL, num_article=num_article, route_id=route, 
                              precision=precision, recall=recall, f1=f1)

    create_chart(pl=PL, article=num_article, data=precision, metric_name='Precision', model=model, color='blue', config=route)
    create_chart(pl=PL, article=num_article, data=recall, metric_name='Recall', model=model, color='orange', config=route)
    create_chart(pl=PL, article=num_article, data=f1, metric_name='F1', model=model, color='green', config=route)

if __name__ == '__main__':
    main()