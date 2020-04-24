import pickle
import numpy as np
import pandas as pd

if __name__=="__main__":
    modelName = f"PTM_V07"
    filepath= f"../results/{modelName}/{modelName}.theta"
    data_version="V01"
    fileIdspath = f"../STTM-master/dataset/corpusIds_{data_version}.txt"
    datapath=f"C:/Users/RAKA/Documents/Metro_dataset/data/output_data/preprocessed_data_{data_version}_(polarity_added).pkl"

    savepath = f"res_{modelName}_{data_version}.pkl"
    with open(filepath,'r') as f:
        lns = f.readlines()
    with open(fileIdspath,'r') as f:
        lns_ids = f.readlines()
    with open(datapath,"rb") as f:
        data = pickle.load(f)

    data["topic_distribution"] = None
    lenLns = len(lns)
    for i in range(lenLns):
        try:
            if i!=lenLns-1: cid = int(lns_ids[i][:-1])
            else: cid = int(lns_ids[i])
            id = data[data["commentID"]==cid]['commentID'].index[0]
            data['topic_distribution'][id] = lns[i].split(' ')[:-1]
        except:
            print(i )
            print(int(lns_ids[i][:-1]) )

        # ['topic_distribution'][0] = lns[i].split(' ')[:-1]

    lenData=len(data)
    for i in range(lenData-1,-1,-1):
        if data["topic_distribution"][i]==None:
            # print(i)
            data = data.drop(i)

    with open(savepath,"wb") as f:
        pickle.dump(data,f)
        data.to_excel(savepath[:-4]+".xlsx")

