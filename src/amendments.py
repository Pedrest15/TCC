import pandas as pd
from summarizing import Text

class Amendments:

    def __init__(self, pl:int, article:int, arq_name:str):
        self.pl = pl
        self.article = article
        self.df = self.__load_amendments_df(arq_name=arq_name)
        self.text = self.__load_amendments_str()

    def __load_amendments_df(self,arq_name:str) -> pd.DataFrame:
        return pd.read_csv(arq_name + ".csv")
    
    def __load_amendments_str(self) -> str:
        try:
            text = "".join([f"EMENDA ID {numero_emenda}:\n{text_proposto_emenda}\n\n" for numero_emenda, text_proposto_emenda in zip(self.df['NUMEROEMENDA'], self.df['TEXTOPROPOSTOEMENDA'])])
        except MemoryError:
            text = ""

        return text
    
    def count_amendments(self) -> int:
        return self.df.shape[0]
    
    def pre_process_text(self) -> str:
        text_tools = Text()
        pre_amendments = "".join([f"EMENDA ID {numero_emenda}:\n{text_tools.preprocess_text(emenda)}\n" for numero_emenda, emenda in zip(self.df['NUMEROEMENDA'], self.df['TEXTOPROPOSTOEMENDA'])])

        return pre_amendments
    
    def summarize(self, model_name) -> str:
        summarize_text = "".join([f"RESUMO EMENDA ID {numero_emenda}:\n{Text.summarize(text=emenda, model_name=model_name)}\n" for numero_emenda, emenda in zip(self.df['NUMEROEMENDA'], self.df['TEXTOPROPOSTOEMENDA'])])

        return summarize_text
    
    def pre_process_summarized(self) -> str:
        text_tools = Text()
        pre_summarize_text = "".join([f"RESUMO EMENDA ID {numero_emenda}:\n{text_tools.preprocess_text(text_tools.summarize(emenda))}\n" for numero_emenda, emenda in zip(self.df['NUMEROEMENDA'], self.df['TEXTOPROPOSTOEMENDA'])])

        return pre_summarize_text

    def get_amendments_text(self):
        try:
            text_tools = Text()
            text = "".join(f"{text_tools.preprocess_text(text_proposto_emenda)} " for text_proposto_emenda in self.df['TEXTOPROPOSTOEMENDA'])
            #text = "".join(f"{text_proposto_emenda} " for text_proposto_emenda in self.df['TEXTOPROPOSTOEMENDA'])
        except MemoryError:
            text = ""

        return text
    
    def get_amendment(self, id:int, route:int):
        try:
            #text_tools = Text()
            text = self.df.loc[self.df['NUMEROEMENDA'] == id, 'TEXTOPROPOSTOEMENDA'].iloc[0]

            if route == 2:
                text_tools = Text()
                text = text_tools.preprocess_text(text)
            elif route == 3:
                text_tools = Text()
                text = text_tools.summarize(text)
            elif route == 4:
                text_tools = Text()
                text = text_tools.preprocess_text(text_tools.summarize(text))

            return text
        
        except Exception as err:
            print(err)

