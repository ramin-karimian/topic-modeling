import numpy as np
import pandas as pd
import pickle
from time import time as tm
from multiprocessing import Process, Manager
from myScripts.run_java import run_model , run_Coherence, predict
import os
from myScripts.coherence_measure import *
from myScripts.postprocess import *

def create_folders(model_params_dic,params_df,i):
    if f"{model_params_dic['model']}" not in os.listdir(str(params_df['dir'][i])):
        os.mkdir(str(params_df['dir'][i])+"/"+f"{model_params_dic['model']}")
    if  f"{model_params_dic['name']}" not in os.listdir(str(params_df['dir'][i])+"/"+f"{model_params_dic['model']}"):
        dr = str(params_df['dir'][i])+"/"+f"{model_params_dic['model']}"+"/"+f"{model_params_dic['name']}"
        os.mkdir(dr)

def train_model(params_df,i):
    model_params_dic = {
        'jarFile':str(params_df['jarFile'][i]),
        'model': str(params_df['model'][i]),
        'corpus': str(params_df['corpus'][i]),
        'ntopics': str(params_df['ntopics'][i]),
        'alpha': str(params_df['alpha'][i]),
        'beta': str(params_df['beta'][i]),
        'niters': str(params_df['niters'][i]),
        'twords': str(params_df['twords'][i]),
        # 'name': str(params_df['name'][i])
        'name': f"{str(params_df['model'][i])}_V{str(params_df['ntopics'][i])}_{str(params_df['version'][i])}"
    }
    stdout,stderr = run_model(model_params_dic)
    """create folders"""
    create_folders(model_params_dic,params_df,i)

    return stdout,stderr

def calculate_coherence(texts,params_df,i,topicsfile, sheetName = None , post = False):
    if post :name = f"_{sheetName}"
    else: name = f""
    res = None
    try:
        # print(f"inp")
        texts,topics,dict = prepare_coherence_input(texts,topicsfile)
        # print(f"coh")
        d = coherence(texts,topics,dict)
        for m,res in d.items():
            # for k in range(len(res)):
            for k,v in res.items():
                col = f"T{k}{name}_{m}"
                if col not in params_df.keys(): params_df[col] = None
                params_df[col][i] = v
    except:
        print(f"{name} not wordked for i {i} ")
    return params_df,d


def modif_topWords(path,dr):
    with open(f"{dr}/"+path) as f:
        lns = f.readlines()
        lns = [x.split(" ")[:40] for x in lns]
        lns = [" ".join(x) for x in lns]
        lns = " \n".join(lns) + " \n"
    new_pat = path+"_coh"
    with open(f"{dr}/"+new_pat,'w') as f:
        f.write(lns)
    return new_pat

def prediction(new_corpus,params_df,i):
    predict_params_dic = {
        'jarFile':str(params_df['jarFile'][i]),
        'model': str(params_df['model'][i])+"inf",
        'corpus': new_corpus,
        'paras':f"{str(params_df['dir'][i])}/{str(params_df['model'][i])}_V{str(params_df['ntopics'][i])}_{str(params_df['version'][i])}.paras",
        # 'niters': str(params_df['niters'][i]),
        'niters': str(50),
        'twords': str(params_df['twords'][i]),
        'name': f"{str(params_df['model'][i])}_V{str(params_df['ntopics'][i])}_{str(params_df['version'][i])}_pred",
        'sstep': str(0)
    }
    stdout,stderr = predict(predict_params_dic)
    return stdout,stderr

if __name__=="__main__":
    conf ={
        'params':'params.xlsx',
        'params_result':f'params_result_{str(tm())[-3:]}.xlsx',
        # 'topwordspath' : f"C:/Users/RAKA/Documents/Metro_dataset/data/source_data/Top 300 words.xlsx",
        'topwordspath' : f"wordlist.xlsx",
        "sheetName":['top1000','top2000','top8000'],
        'prediction':False,
        'train':True,
    }

    params_df = pd.read_excel(conf['params'])

    for i in range(len(params_df)):
        t = tm()
        print(i )
        texts = prepare_coherence_texts(str(params_df['corpus'][i]))
        if conf['train'] :

            """train model"""
            print("train model")
            stdout,stderr = train_model(params_df,i)

            """calculate coherence"""
            print("calculate coherence")
            topicsfile = f"{str(params_df['dir'][i])}/{str(params_df['model'][i])}_V{str(params_df['ntopics'][i])}_{str(params_df['version'][i])}.topWords"
            params_df,d = calculate_coherence(texts,params_df,i,topicsfile)

            for sh in conf['sheetName']:
                """post process topWords"""
                # print("post process topWords")
                postprocessed_topWordspath = f"{str(params_df['dir'][i])}/{str(params_df['model'][i])}_V{str(params_df['ntopics'][i])}_{str(params_df['version'][i])}_postprocessed_{sh}.topWords.xlsx"
                post_process(conf['topwordspath'],topicsfile,postprocessed_topWordspath, sheetName = sh)

                """calculate post coherence"""
                print(f"calculate post coherence {sh}")
                params_df,d = calculate_coherence(texts,params_df,i,postprocessed_topWordspath[:-5], sheetName = sh , post = True)

        if conf['prediction']:
            new_corpus = 'STTM-master/dataset/one_article_corpus_V02.txt'
            stdout,stderr = prediction(new_corpus,params_df,i)
        print(f"for i {i} took : {tm()-t}")
        params_df.to_excel(conf['params_result'])



