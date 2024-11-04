from math import log
import numpy as np
from scipy.spatial.distance import cosine
from sklearn.feature_extraction.text import CountVectorizer
from itertools import combinations
from transformers import BertTokenizer, BertModel
from bert_score import BERTScorer

from amendments import Amendments
from models import EmbModel
from summarizing import Text
 
class Score:
    
    def __init__(self, pl:str, article:int):
        self.pl = pl
        self.article = article
        self.scorer = BERTScorer(lang='pt')
        self.precision = []
        self.recall = []
        self.f1 = []
    
    def execute(self, groups, route) -> np.array:
        arq_name = f"../arqs_base/emendas_{self.pl}_artigo{self.article}"
        amendments = Amendments(pl=self.pl, article=self.article, arq_name=arq_name)

        for group in groups:
            candidate = group.tema
            if candidate == None:
                print(group)
                continue

            ids = group.ids_emendas
            if len(ids) == 0:
                print(group)
                continue

            precision = []
            recall = []
            F1 = []

            for id in ids:
                reference = amendments.get_amendment(id=int(id), route=route) 
                try: 
                    p, r, f = self.scorer.score([candidate], [reference])
                except Exception as err:
                    print(f"cand: {candidate}")
                    print(f"ref: {reference}")
                    print(f"id: {id}")
                    
                    continue
                precision.append(p.mean())
                recall.append(r.mean())
                F1.append(f.mean())

            self.precision.append(np.array(precision).mean())
            self.recall.append(np.array(recall).mean())
            self.f1.append(np.array(F1).mean())

        print(np.array(self.precision).mean())

        return np.array(self.precision).mean(), np.array(self.recall).mean(), np.array(self.f1).mean()



if __name__ == '__main__':
    pl = "PL-280-2020"
    article = 21
    arq_name = f"../arqs_base/emendas_{pl}_artigo{article}"
    a = Amendments(pl=pl, article=article, arq_name=arq_name)

    x = a.get_amendment(id="28050004", route=2)
    print(x)