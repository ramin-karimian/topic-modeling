import pandas as pd
# from myfiles.src.utils import *

def post_process(topwordspath,read_path,save_path, sheetName = 'total'):
    top_words= (pd.read_excel(topwordspath,sheet_name=sheetName,header=None)[0])
    with open(read_path) as f:
        l = f.readlines()
        for i in range(len(l)-1,-1,-1):
            if l[i]=="\n":
                del l[i]


    old_l = []
    new_l = []
    for i in range(len(l)):
        # if l[i]=="\n":continue
        new_l.append(l[i].split(" "))
        old_l.append(l[i].split(" "))
        new_l[i][0] = new_l[i][0][0:-1]
        new_l[i][-1] = new_l[i][-1][0:-1]
        old_l[i][0] = old_l[i][0][0:-1]
        old_l[i][-1] = old_l[i][-1][0:-1]
        for j in range(len(new_l[i])-1,-1,-1):
            if new_l[i][j]  not in top_words.values:
                del new_l[i][j]
    df = pd.DataFrame(old_l)
    df.to_excel(read_path + ".xlsx")

    df = pd.DataFrame(new_l)
    df.to_excel(save_path)

    with open(save_path[:-5],"w") as f :
        for i in range(len(new_l)):
            f.write(" ".join(new_l[i]))
            f.write(" \n")


if __name__=="__main__":
    # modelName= f"model_v3"
    modelName= f"WNTM"
    model_version = f"V6_1"
    # read_path=f"../results/{modelName}/{modelName}_{model_version}.topWords"
    # save_path=f"../results/{modelName}/{modelName}_{model_version}_postprocessed.topWords.xlsx"
    read_path=f"../results/{modelName}_{model_version}.topWords"
    save_path=f"../results/{modelName}_{model_version}_postprocessed.topWords.xlsx"
    topwordspath = f"C:/Users/RAKA/Documents/Metro_dataset/data/source_data/Top 300 words.xlsx"
    post_process(topwordspath,read_path,save_path)
    # top_words= (pd.read_excel(topwordspath,sheet_name="top 300 words",header=None)[0])
    #
    # with open(read_path) as f:
    #     l = f.readlines()
    #     for i in range(len(l)-1,-1,-1):
    #         if l[i]=="\n":
    #             del l[i]
    #
    # new_l = []
    # for i in range(len(l)):
    #     # if l[i]=="\n":continue
    #     new_l.append(l[i].split(" "))
    #     new_l[i][0] = new_l[i][0][0:-1]
    #     new_l[i][-1] = new_l[i][-1][0:-1]
    #     for j in range(len(new_l[i])-1,-1,-1):
    #         if new_l[i][j]  not in top_words.values:
    #             del new_l[i][j]
    # df = pd.DataFrame(new_l)
    # df.to_excel(save_path)


