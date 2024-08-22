import re
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

import tiktoken

from nltk.corpus import stopwords
import spacy
from spacy.lang.pt.stop_words import STOP_WORDS

from models import Templates, ModelsOllama

#import nltk
#nltk.download('punkt')
#nltk.download('stopwords')

class Text:
    def __init__(self, encoding_name:str="cl100k_base"):
        self.nlp = spacy.load('pt_core_news_sm', disable=['ner', 'parser'])
        self.nlp.max = 50000
        self.global_sw = list(set(stopwords.words('portuguese') + list(STOP_WORDS)))
        self.encoding_name = encoding_name

    def preprocess_text(self, text:str):
        text = text.replace('\n', ' ').strip() # remove quebras de linha
        text = re.sub(r'\s+', ' ', text, flags=re.I)  # Substituindo múltiplos espaços por um único espaço
        text = re.sub(r'\.{2,}', '.', text) # removendo excesso de . na string
        text = re.sub(r'\_{2,}', '.', text) # removendo excesso de _ na string
        text = re.sub(r' \. ', '', text) # remove pontos . soltos em uma string
        text = re.sub(r'\^[a-zA-Z]\s+', ' ', text)  # Removendo palavras isoladas do início

        text = re.sub(r'\b\d{6,}\b', '', text) # Removendo termos numéricos com tamanho maior que 6 (ex, números de protocolo)
        text = re.sub(r'\bº\b', '', text) # remove caractere isolado em frase
        text = re.sub(r'¿', '', text)

        text = re.sub(' {2,}', ' ', text) # remove espaços em branco desnecessários

        doc = self.nlp(text)
        tokens = [token.text for token in doc if not token.is_punct and token.text not in self.global_sw]
        preprocessed_text = ' '.join(tokens)

        return preprocessed_text
    
    def tokens_calculator(self, text:str):
        encoding = tiktoken.get_encoding(self.encoding_name)

        return len(encoding.encode(text))

    def summarize(self, text:str) -> str:
        model = ModelsOllama.connect(ModelsOllama.LLAMA3,0)
        parser = StrOutputParser()
        prompt = PromptTemplate(
            template=Templates.SUMMARIZE_TEMPLATE,
            input_variables=['original_text'],
        )
        
        chain = prompt | model | parser
        response = chain.invoke({'original_text': text})

        return response

if __name__ == '__main__':
    from amendments import Amendments
    PL = "PL-280-2020"
    num_article = 21
    arq_name = f"../arqs_base/emendas_{PL}_artigo{num_article}"

    amendments = Amendments(pl=PL,article=num_article,arq_name=arq_name)
    text_tools = Text()

    text = []
    for id, amendment in zip(amendments.df['NUMEROEMENDA'], amendments.df['TEXTOPROPOSTOEMENDA']):
        text.append([id, amendment])
        break

    #print(Templates.CLUSTER_QUERY + amendments.text)
    #print(text)
    pre_text = "".join([f"EMENDA ID {numero_emenda}:\n{text_tools.preprocess_text(emenda)}\n" for numero_emenda, emenda in text])
    #summarize_text = "".join([f"RESUMO EMENDA ID {numero_emenda}:\n{text_tools.summarize(emenda)}\n" for numero_emenda, emenda in text])

    pre_summarize_text = ""
    for numero_emenda, emenda in text:
        pre_summarize_text = text_tools.summarize(pre_summarize_text)
        pre_summarize_text = text_tools.preprocess_text(emenda)
        print(pre_summarize_text)
        exit()
    pre_summarize_text = "".join([f"RESUMO EMENDA ID {numero_emenda}:\n{text_tools.summarize(text_tools.preprocess_text(emenda))}\n" for numero_emenda, emenda in text])



    num_tokens_complete_text = text_tools.tokens_calculator(amendments.text)
    num_tokens_pre_text = text_tools.tokens_calculator(pre_text)
    #num_tokens_summarize_text = text_tools.tokens_calculator(summarize_text)
    num_tokens_pre_summarize_text = text_tools.tokens_calculator(pre_summarize_text)
    
    print(f"=>Tokens texto todo: {num_tokens_complete_text}")
    print(f"=>Tokens texto pré processado: {num_tokens_pre_text}")
    #print(f"=>Tokens resumo: {num_tokens_summarize_text}")
    print(f"=>Tokens resumo pré processado: {num_tokens_pre_summarize_text}")

    #print(f"=>pré: {Templates.CLUSTER_QUERY+pre_text}\n\n")
    #print(f"=>resumo: {Templates.CLUSTER_QUERY+summarize_text}\n\n")
    print(f"=>resumo pré: {Templates.CLUSTER_QUERY+pre_summarize_text}")

