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


class CV_Coherence:

    def __init__(self, pl:str, article:int, emb_model_name:str="neuralmind/bert-base-portuguese-cased"):
        self.pl = pl
        self.article = article
        self.emb_model = EmbModel(model_name=emb_model_name)
        self.word_vec = {}
        self.word_freq = None
        self.word_pairs = None
        self.co_occurrence_freq = None
        self.total_words = None
        self.npm = {}
        self.scores = {}

    def execute(self, groups):
        arq_name = f"../arqs_base/emendas_{self.pl}_artigo{self.article}"

        amendments = Amendments(pl=self.pl, article=self.article, arq_name=arq_name)
        amendments_text = amendments.get_amendments_text()

        self.__get_word_vec(text=amendments_text)
        self.word_pairs = self.__get_word_pairs(text=amendments_text)
        self.word_freq, matrix, vocab = self.__get_co_occurrence_matrix(text=amendments_text)
        self.co_occurrence_freq = self.__get_co_occurrence_freq(matrix=matrix, vocab=vocab)
        self.__total_words(text=amendments_text)
        self.__calculate_npmis()

        for group in groups:
            topic = group.tema
            topic_words = topic.split(" ")

            score = self.__calculate_topic_coherence(words=topic_words)

            self.scores[group.tema] = score
            break

        return self.scores

    def __get_word_vec(self, text):
        for word in text.split(" "):
            if word not in self.word_vec:
                self.word_vec[word] = self.emb_model.embed(text=word)

    def __get_co_occurrence_matrix(self, text:str):
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform([text])
        word_freq = dict(zip(vectorizer.get_feature_names_out(), X.sum(axis=0).A1))

        X_dense = X.toarray()

        co_occurrence_matrix = (X_dense.T*X_dense)
        vocab = vectorizer.get_feature_names_out()

        return word_freq, co_occurrence_matrix, vocab

    def __get_co_occurrence_freq(self, matrix, vocab):
        co_occurrence_freq = {}

        for i in range(len(vocab)):
            for j in range(i+1, len(vocab)):
                co_occurrence_freq[(vocab[i], vocab[j])] = matrix[i, j]

        return co_occurrence_freq
    
    def __get_word_pairs(self, text):
        words = text.split(" ")

        return list(combinations(words, 2))
    
    def __total_words(self, text):
        self.total_words = len(text.split(" "))

    def __calculate_npmis(self):
        x = 0
        for (wi, wj) in self.word_pairs:
            if x == 3:
                break

            pij = self.co_occurrence_freq.get((wi, wj), 0) / self.total_words
            pi = self.word_freq.get(wi, 0) / self.total_words
            pj = self.word_freq.get(wj, 0) / self.total_words

            if pi > 0 and pj > 0 and pij > 0:
                npmi = log(pij / (pi*pj)) / -log(pij)
                self.npm[(wi, wj)] = npmi
            else:
                self.npm[(wi, wj)] = 0

            x += 1
    
    def __cosine_similarity(self, u, v):
        if np.linalg.norm(u) == 0 or np.linalg.norm(v) == 0:
            return 0
        
        return 1 - cosine(u, v)
    
    def __calculate_topic_coherence(self, words):
        vec = [self.word_vec.get(word, np.zeros(self.emb_model.emb_len())) for word in words]
        topic_vector = np.sum(vec, axis=0)
        similarities = []

        for i in range(len(words)):
            for j in range(i+1, len(words)):
                wi = words[i]
                wj = words[j]
                vec_i = self.word_vec.get(wi, np.zeros(self.emb_model.emb_len()))
                vec_j = self.word_vec.get(wj, np.zeros(self.emb_model.emb_len()))

                cos_sim_i = self.__cosine_similarity(vec_i, topic_vector)
                cos_sim_j = self.__cosine_similarity(vec_j, topic_vector)
                cos_sim = (cos_sim_i + cos_sim_j) / 2

                npmi = self.npm.get((wi, wj), 0)
                pij = self.co_occurrence_freq.get((wi, wj), 0) / self.total_words

                if pij > 0:
                    normalized_npmi = npmi / -log(pij)
                else:
                    normalized_npmi = 0

                similarities.append(cos_sim*normalized_npmi)
        
        return np.mean(similarities)
    
class Score:
    
    def __init__(self, pl:str, article:int):
        self.pl = pl
        self.article = article
        self.scorer = BERTScorer(lang='pt')
        self.precision = []
        self.recall = []
        self.f1 = []
    
    def execute(self, groups, route):
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