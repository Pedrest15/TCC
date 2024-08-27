import gdown
import time

from amendments import Amendments
from models import ModelsOllama
from chain import SimpleChain, PydanticChain
from routes import RoutesConfig

def main():
    print("################   Agrupamento Semântico de Emendas Parlamentares   ################")
    print()
    print("1- Fluxo de chain padrao com texto proposto das emendas completo.")
    print("2- Fluxo de chain padrao com texto proposto das emendas pre-processado.")
    print("3- Fluxo de chain com travas de Pydantic com texto proposto das emendas completo.")
    print("4- Fluxo de chain com travas de Pydantic com texto proposto das emendas pre-processado.")
    print("5- Fluxo de chain padrão com texto proposto das emendas resumidas.")
    print("6- Fluxo de chain padrão com texto proposto das emendas resumidas e pre-processadas.")
    print("7- Fluxo de chain com travas de Pydantic com texto proposto das emendas resumidas.")
    print("8- Fluxo de chain com travas de Pydantic com texto proposto das emendas resumidas e pre-processadas.")
    print()
    route = int(input("Qual configuração de rota você gostaria de executar? "))

    PL = "PL-280-2020"
    num_article = 21

    RoutesConfig(pl=PL, article=num_article, route_id=route).execute()

if __name__ == '__main__':
    main()