import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from myScripts.utils import check_print



def prepare_data(datapath):
    with open(datapath,"r") as f :
        lns = f.readlines()
    new_lns = [[float(y) for y in x.split(' ')[:-1]] for x in lns]
    return new_lns

def create_i2w(vocabpath):
    with open(vocabpath,"r") as f :
        lns1 = f.readlines()
    i2w = {}
    for x in lns1 :
        w,i = x[:-1].split(' ')
        i2w[int(i)] = w
    return i2w

def create_i2v(data):
    i2v = {}
    veclist = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            if j not in i2v.keys(): i2v[j] = [data[i][j]]
            else: i2v[j].append(data[i][j])
            if len(i2v[j]) == len(data):
                veclist.append(i2v[j])
    return i2v , veclist

def compute_cosine_similarities(emb_data):
    sims = cosine_similarity(emb_data,emb_data)
    return sims

def create_output(veclist,i2w,tags_df):
    tags = tags_df['WORD'].values
    sims = compute_cosine_similarities(veclist)
    df = pd.DataFrame(columns=i2w.values(),index=i2w.values())
    for i in range(len(df)):
        check_print(i)
        if i2w[i] not in tags: continue
        df.iloc[i] = sims[i]
    tags = [ x for x in tags if x in df.keys()]
    new_df = pd.DataFrame(df , columns = tags,index = tags)
    return new_df

if __name__=="__main__":
    model_version = f"V19"
    modelName = f"WNTM"
    datapath =f"../results/{modelName}/{modelName}_{model_version}.phi"
    vocabpath =f"../results/{modelName}/{modelName}_{model_version}.vocabulary"
    tagspath =f"../STTM-master/dataset/Top 300 words.xlsx"
    outputpath =f"../results/{modelName}/{modelName}_{model_version}_words_association.xlsx"

    data = prepare_data(datapath)
    i2w = create_i2w(vocabpath)
    i2v, veclist = create_i2v(data)

    tags_df = pd.read_excel(tagspath)
    df = create_output(veclist,i2w,tags_df)
    df.to_excel(outputpath)




