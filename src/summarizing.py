import re
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

import tiktoken

from nltk.corpus import stopwords
import spacy
from spacy.lang.pt.stop_words import STOP_WORDS

from models import Templates, Models, EmbModel

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
    
    def embed(self, text):
        return self.nlp(text).vector
    
    def embed_vector_len(self):
        return self.nlp.vocab.vectors_length
    
    def tokens_calculator(self, text:str):
        encoding = tiktoken.get_encoding(self.encoding_name)

        return len(encoding.encode(text))

    def summarize(self, text:str, model_name) -> str:
        model = Models().connect(model_name=model_name,temperature=0)
        parser = StrOutputParser()
        prompt = PromptTemplate(
            template=Templates.SUMMARIZE_TEMPLATE,
            input_variables=['original_text'],
        )
        
        chain = prompt | model | parser
        response = chain.invoke({'original_text': text})

        return response



