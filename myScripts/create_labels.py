import numpy as np



if __name__=="__main__":
    modelName =f"corpusPTM"
    datapath = f"../results/{modelName}/{modelName}.theta"
    savepath = f"../results/{modelName}/{modelName}.label"

    with open(datapath,"r") as f:
        l = f.readlines()

    with open(savepath,"w") as f:
        lenL=len(l)
        for x in l:
            cl = np.argmax([float(y) for y in x.split(" ")[:-1]])+1
            if l.index(x)!=lenL-1:
                f.write(str(cl)+"\n")
            else:
                f.write(str(cl))



