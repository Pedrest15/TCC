from routes import RoutesConfig
from score import Score
from files import Files
from chart import create_chart

def choose_route():
    print("################   Agrupamento Semântico de Emendas Parlamentares   ################")
    print()
    print("1- Fluxo com texto proposto das emendas completo.")
    print("2- Fluxo com texto proposto das emendas pre-processado.")
    print("3- Fluxo com texto proposto das emendas resumidas.")
    print("4- Fluxo com texto proposto das emendas resumidas e pre-processadas.")
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

    mean_precision = {0:0.0, 0.25:0.0, 0.5:0.0, 0.75:0.0, 1:0.0}
    mean_recall = {0:0.0, 0.25:0.0, 0.5:0.0, 0.75:0.0, 1:0.0}
    mean_f1 = {0:0.0, 0.25:0.0, 0.5:0.0, 0.75:0.0, 1:0.0}

    Files.create_score_file(model=model, PL=PL, num_article=num_article, route_id=route)

    for i in range(5):
        precision = {0:0.0, 0.25:0.0, 0.5:0.0, 0.75:0.0, 1:0.0}
        recall = {0:0.0, 0.25:0.0, 0.5:0.0, 0.75:0.0, 1:0.0}
        f1 = {0:0.0, 0.25:0.0, 0.5:0.0, 0.75:0.0, 1:0.0}
    
        for temp in temps:
            groups = RoutesConfig(model=model, pl=PL, article=num_article, route_id=route).execute(temp=temp)
            
            p,r,f = Score(pl=PL, article=num_article).execute(groups=groups, route=route)

            precision[temp] = p
            recall[temp] = r
            f1[temp] = f

            mean_precision[temp] += p
            mean_recall[temp] += r
            mean_f1[temp] += f

        Files.generate_score_file(model=model, PL=PL, num_article=num_article, route_id=route, 
                                precision=precision, recall=recall, f1=f1, i=i)
    for temp in temps:
        mean_precision[temp] /= 5
        mean_recall[temp] /= 5
        mean_f1[temp] /= 5


    create_chart(pl=PL, article=num_article, data=mean_precision, metric_name='Precision', model=model, color='blue', config=route)
    create_chart(pl=PL, article=num_article, data=mean_recall, metric_name='Recall', model=model, color='orange', config=route)
    create_chart(pl=PL, article=num_article, data=mean_f1, metric_name='F1', model=model, color='green', config=route)

if __name__ == '__main__':
    main()