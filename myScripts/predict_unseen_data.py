import numpy as np
import pandas as pd
from myScripts.utils import check_print



def prepare_data(datapath,ext = 'phi'):
    with open(datapath,"r") as f :
        lns = f.readlines()
    if ext == "phi":
        new_lns = [[float(y) for y in x.split(' ')[:-1]] for x in lns]
    elif ext == 'corpus':
        new_lns = [[y for y in x[:-1].split(' ')] for x in lns]
    return new_lns

def create_i2w(vocabpath):
    with open(vocabpath,"r") as f :
        lns1 = f.readlines()
    i2w = {}
    w2i = {}
    for x in lns1 :
        w,i = x[:-1].split(' ')
        i2w[int(i)] = w
        w2i[w] = int(i)

    return i2w , w2i

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

def doc2distr(corpus,outputpath,outputTokensPath,w2i,veclist):
    keys=w2i.keys()
    dim = len(veclist[0])
    f = open(outputpath,"w")
    f1 = open(outputTokensPath,"w")
    for i in range(len(corpus)):
        vec = np.zeros(dim)
        tokens = []
        for j in range(len(corpus[i])):
            w = corpus[i][j]
            if w in keys:
                vec = np.sum([vec,veclist[w2i[w]]],axis=0)
                tokens.append(w)
            # else:
                # print(f"{w} {i}")
        if len(tokens)==0:
            vec = ['ignored']
            print(f"ignore {i}")

        for k in range(len(vec)):
            f.write(f'{vec[k]} ')
        f.write('\n')

        for k in range(len(tokens)):
            f1.write(f'{tokens[k]} ')
        f1.write('\n')
    f.close()
    f1.close()





if __name__=="__main__":
    model_version = f"V4_38"
    modelName = f"WNTM"
    datapath =f"../results/{modelName}/{modelName}_{model_version}.phi"
    vocabpath =f"../results/{modelName}/{modelName}_{model_version}.vocabulary"
    unseen_datapath =f"../STTM-master/dataset/total_corpus_V02.txt"

    tagspath =f"../STTM-master/dataset/Top 300 words.xlsx"
    outputpath =f"../results/{modelName}/{modelName}_{model_version}_pred.theta"
    outputTokensPath =f"../results/{modelName}/{modelName}_{model_version}_pred.tokens"

    data = prepare_data(datapath)
    i2w, w2i = create_i2w(vocabpath)
    i2v, veclist = create_i2v(data)

    corpus = prepare_data(unseen_datapath,ext = 'corpus')
    doc2distr(corpus,outputpath,outputTokensPath,w2i,veclist)
