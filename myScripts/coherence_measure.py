import numpy as np
import pandas as pd
# from gensim.test.utils import common_corpus, common_dictionary
from gensim.models.coherencemodel import CoherenceModel
from gensim.corpora import Dictionary
from time import time as tm

def prepare_coherence_texts(textfile):
    with open(textfile) as f1:
        lns1 = f1.readlines()
        texts = [x[:-1].split(' ') for x in lns1]
    return texts

def prepare_coherence_input(texts,topicsfile):

    with open(topicsfile) as f2:
        lns2 = f2.readlines()
        topics = [x.split(' ')[:-1] for x in lns2]

    dict = Dictionary(texts)
    return texts,topics,dict

# def coherence(texts,topics,dict,topns= [5,10,20,40,80]):
# def coherence(texts,topics,dict,topns= [6,8,10,12,15,17,20,25]):
#     res = pd.Series()
#     for t in topns:
#         try :
#             # print(f" : {t}")
#             cm = CoherenceModel(topics=topics, texts=texts, dictionary=dict, topn = t, coherence='u_mass')
#             co = cm.get_coherence()
#             # res.append(co)
#             res.loc[t] = co
#         except:
#             res.loc[t] = None
#         print(res)
#     return res

def coherence(texts,topics,dict,topns= [5,10,15,20,40],models=['c_uci','c_v','u_mass','c_npmi']):
# def coherence(texts,topics,dict,topns= [6,8],models=['c_uci','c_v','u_mass','c_npmi']):
    # res = pd.Series()
    d = {}
    for t in topns:
        for m in models:
            if m not in d.keys():
                d[m]={}
            try :
                # print(f" : {t}")
                cm = CoherenceModel(topics=topics, texts=texts, dictionary=dict, topn = t, coherence=m,processes = 8)
                co = cm.get_coherence()
                # res.loc[t] = co
                d[m][t] = co
            except:
                # res.loc[t] = None
                d[m][t] = None
            # d[m]=res
    return d

if __name__=="__main__":

    textfile= f"../STTM-master/dataset/one_article_corpus_V02.txt"
    topicsfile= f"../report/(4.8.2020)/full_report_(4.8.2020)/WNTM/one_article/WNTM_V12.topWords"
    # textfile= f"../STTM-master/dataset/total_corpus_V02.txt"
    # topicsfile= f"../results/WNTM_V4_11_postprocessed.topWords"
    t = tm()
    texts = prepare_coherence_texts(textfile)
    texts,topics,dict = prepare_coherence_input(texts,topicsfile)
    d = coherence(texts,topics,dict)
    print(d)
    print(tm()-t)

    # cm = CoherenceModel(topics=topics, texts=texts, coherence='u_mass')
