import os.path,subprocess
from subprocess import STDOUT,PIPE


def execute_java(cmd):
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate()
    if stderr != None :
        print(f"model name {cmd[-1]} did not run ")
    return stdout,stderr

def run_model(params_dic):
    cmd = [ 'java',
            '-jar',params_dic['jarFile'],
            '-model', params_dic['model'],
            '-corpus', params_dic['corpus'],
            '-ntopics', params_dic['ntopics'],
            '-alpha', params_dic['alpha'],
            '-beta', params_dic['beta'],
            '-niters', params_dic['niters'],
            '-twords', params_dic['twords'],
            '-name', params_dic['name']
            ]
    stdout,stderr = execute_java(cmd)
    return stdout,stderr

def run_Coherence(params_dic):
    cmd = [ 'java',
            '-jar',params_dic['jarFile'],
            '-model', 'CoherenceEval',
            '-label', params_dic['label'],
            '-dir', params_dic['dir'],
            '-topWords', params_dic['topWords']
            ]
    stdout,stderr = execute_java(cmd)
    if stderr != None :
        print(f"model Coherence {cmd[-1]} did not run ")
    return stdout,stderr

def predict(params_dic):
    cmd = [ 'java',
            '-jar',params_dic['jarFile'],
            '-model', params_dic['model'],
            '-paras', params_dic['paras'],
            '-corpus', params_dic['corpus'],
            '-niters', params_dic['niters'],
            '-twords', params_dic['twords'],
            '-name', params_dic['name'],
            '-sstep', params_dic['sstep']
            ]
    stdout,stderr = execute_java(cmd)
    if stderr != None :
        print(f"model Coherence {cmd[-1]} did not run ")
    return stdout,stderr

if __name__ =="__main__":
    model_params_dic = {
        'jarFile':'../STTM-master/jar/STTM.jar',
        'model': 'LDA',
        'corpus': '../STTM-master/dataset/total_corpus_oneArticle_V02.txt ',
        'ntopics': '6',
        'alpha': '10',
        'beta':'0.01',
        'niters': '500',
        'twords': '300',
        'name': 'LDA_V6_023'
    }
    stdout,stderr = run_model(model_params_dic)
    Coherence_params_dic = {
        'jarFile':'../STTM-master/jar/STTM.jar',
        'model':'CoherenceEval',
        'label': '../wiki.en.text',
        'dir': 'results',
        'topWords': 'LDA_V6_023.topWords'
    }
    stdout,stderr = run_Coherence(Coherence_params_dic)

