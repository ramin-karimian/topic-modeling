
data_version="V01"
datapath1 = f"../STTM-master/dataset/corpus_V01_.txt"
datapath2=f"../results/DMM_V01/DMM_V01.topicAssignments"

f1 = open(datapath1,'r')
f2 = open(datapath2,'r')
lns1=f1.readlines()
lns2=f2.readlines()
for i in range(len(lns1)):
    if len(lns2[i].split()) != len(lns1[i].split()):
        print(i)
