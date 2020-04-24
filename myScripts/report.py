import os
from myScripts.utils import *
import numpy as np
import pandas as pd
import re

if __name__=="__main__":

    # datapath = f"C:/Users/RAKA/Documents/Metro_dataset/data/output_data/preprocessed_data_tagged_V02_(polarity_added).pkl"
    datapath = f"C:/Users/RAKA/Documents/Metro_dataset/data/output_data/total/V04/preprocessed_data_V04_total.pkl"
    dataIdpath = f"../STTM-master/dataset/total_corpusIds_V04.txt"
    savepath = f"../report/(4._.2020)/report"
    tagspath = f"C:/Users/RAKA/Documents/Metro_dataset/data/source_data/Tags.xlsx"
    df = load_data(datapath,article='total')[0]
    # l = []
    # for i in os.listdir("../report"):
    #     for j in os.listdir(os.path.join("../report",i)):
    #         l.append(j.split("_postprocessed")[0])
    # l = ['WNTM_V04','WNTM_V06']
    l = ['WNTM_V4_38','WNTM_V6_18','WNTM_V8_43','WNTM_V10_24','WNTM_V15_30','WNTM_V17_51','WNTM_V20_36']
    # df['updated_tokens']=None
    for p in l:
        print(p)
        f = open(os.path.join("../results",p.split('_V')[0],f"{p}",f"{p}.theta"))
        # f = open(os.path.join("../results",p.split('_V')[0],f"{p}_pred.theta"))
        lns = f.readlines()
        f1 = open(dataIdpath)
        lns1 = f1.readlines()
        # f2 = open(os.path.join("../results",p.split('_V')[0],f"{p}_pred.tokens"))
        # lns2 = f2.readlines()

        lns1 = [int(x[:-1]) for x in lns1]
        if p not in list(df.keys()):
            df[p]=None
            df[f"topical_rep_{p}"] = None
        for i in range(len(lns)):
            # df['updated_tokens'][df["commentID"]==lns1[i]] = str(lns2[i].split(" ")[:-1])
            # if lns[i] == 'ignored \n':
            #     df[p][df["commentID"]==lns1[i]]='ignored'
            #     continue
            topic = np.argmax([float(x) for x in lns[i].split(" ")[:-1] ])
            ind = df[f"topical_rep_{p}"][df["commentID"]==lns1[i]].index[0]
            # df[p][df["commentID"]==lns1[i]]=topic
            df[p][ind]=topic
            # df[f"topical_rep_{p}"][df["commentID"]==lns1[i]][0]= [float(x) for x in lns[i].split(" ")[:-1] ]
            df[f"topical_rep_{p}"][ind]= [float(x) for x in lns[i].split(" ")[:-1] ]
            # break
        # break

    df["commentBody"] = df["commentBody"].apply(lambda x : re.sub('\r','',x))
    df['Class'] = None
    tags = pd.read_excel(tagspath)
    for i in range(len(tags)):
        try:
            ind = df[df['commentBody']==tags['Comment'][i]].index[0]
            df['Class'][ind] = tags['Class'][i]
        except:
            print(i)

    save_data(savepath+".pkl",df)
    df.to_excel(savepath+".xlsx")
