import os
import numpy as np
import pandas as pd

def read_data(path):
    data_dic = []
    for i in os.listdir(path):
        if i not in ["LDA"] : continue
        if i.endswith(('.py','.vocabulary','.theta','.topWords',".xlsx")):continue
        dic = {}
        name = None
        for j in os.listdir(os.path.join(path,i)):
            if j.endswith('.paras'):
                dic = {}
                name = j.split('.')[0]
                print(name)
                with open(os.path.join(path,i,j),'r') as f:
                    lns = f.readlines()
                for l in lns:
                    t = l.split('\t')
                    dic[t[0][1:]] = t[1][:-1]

            elif j.endswith('.Coherence') and name == j.split('.')[0]:
                with open(os.path.join(path,i,j),'r') as f:
                    lns = f.readlines()
                T = lns[-1].split(", ")
                for t in T:
                    tt = t.split(": ")
                    dic[tt[0]] = tt[1]
                data_dic.append(dic)
            else:
                continue
        # data.append(dic)
    return data_dic

def modif_data(data,keys):
    df = pd.DataFrame(columns=keys,index=range(len(data)))
    for d in data:
        for k in keys:
            try:
                df[k][data.index(d)] = d[k]
            except:
                df[k][data.index(d)] = None
                print(d)
    return df

if __name__=="__main__":
    keys = ['model', 'corpus', 'ntopics', 'alpha', 'beta', 'niters', 'twords', 'name', 'initiation time', 'one iteration time', 'total time', 'Mean Coherence', 'standard deviation']
    path = "../results"
    data = read_data(path)
    df = modif_data(data,keys)
    df.to_excel("../results/report.xlsx")
