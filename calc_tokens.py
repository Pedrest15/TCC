from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.chat import SystemMessagePromptTemplate
from langchain_community.chat_models import ChatOllama

import tiktoken
import os
import gdown
import pandas as pd
import time

def limpar_base(base_documentos):
  # remove emendas com texto principal duplicado e também remove emendas com texto principal nulo
  base_documentos_limpa = base_documentos
  base_documentos_limpa.drop_duplicates(subset=['TEXTOPROPOSTOEMENDA'], inplace=True)
  base_documentos_limpa.dropna(subset=['TEXTOPROPOSTOEMENDA'], inplace=True)

  return base_documentos_limpa

def tokens_calculator(text:str):
    encoding_name = "cl100k_base"
    encoding = tiktoken.get_encoding(encoding_name)

    return len(encoding.encode(text))

if __name__ == '__main__':
    emendas_df = pd.read_csv("u4_ordenado_completo.csv")

    clean_emendas = limpar_base(emendas_df)

    num_tokens_full_text:list[int] = []
    for emenda in clean_emendas["TEXTOPROPOSTOEMENDA"]:
        num_tokens_full_text.append(tokens_calculator(text=emenda))

    clean_emendas["TokensTextoPropostoCompleto"] = num_tokens_full_text

    clean_emendas.to_csv('base_limpa.csv', index=False, encoding='utf-8')

