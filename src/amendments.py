import pandas as pd
from summarizing import Text

class Amendments:

    def __init__(self, pl:int, article:int, arq_name:str):
        self.pl = pl
        self.article = article
        self.df = self.__load_amendments_df(arq_name=arq_name)
        self.text = self.__load_amendments_str()
        self.summarized = None

    def __load_amendments_df(self,arq_name:str):
        return pd.read_csv(arq_name+".csv")
    
    def __load_amendments_str(self):
        try:
            text = "".join([f"EMENDA ID {numero_emenda}:\n{text_proposto_emenda}\n\n" for numero_emenda, text_proposto_emenda in zip(self.df['NUMEROEMENDA'], self.df['TEXTOPROPOSTOEMENDA'])])
        except MemoryError:
            text = ""

        return text
    
    def count_amendments(self):
        return self.df.shape[0]
    
    def summarize(self):
        self.summarized = Text().summarize(self.text)
    
    
    
