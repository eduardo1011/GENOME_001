
from collections import Counter, OrderedDict
import numpy as np
import re
import multiprocessing
import json
import warnings
warnings.filterwarnings("ignore")
from scipy import spatial



def time_ini():
    from datetime import datetime
    xx = datetime.now()
    return xx
def time_fin(i = 0):
    from datetime import datetime
    tim = datetime.now() - i
    print('Time: {}'.format(tim).split('.')[0])


# query
#print('Fasta1')
fas1 = {}
with open('docs/GCF_95_1000_translated_cds.faa') as fq:
    for line in fq:
        line = line.rstrip()
        if '>' in line:
            try:
                fas1[ent] = s
            except NameError:
                ent = line.replace('>', '').split(' ')[0]
            N, s, ent = 0, '', line.replace('>', '').split(' ')[0]
        else:
            g = 0
            while g < 1:
                s += re.sub('[*]', '', line)
                g += 1
            N += 1
fas1.update({ent: s})
del s
for i in list(fas1.keys()):
    if len(fas1[i]) >= 50:
        pass
    else:
        fas1.pop(i)

#print('Q_vectors')
Q_vectors = {}
for Q in fas1:
    vectores_query = {}
    for e, i in enumerate(re.findall(int(len(fas1[Q])/3)*'.', fas1[Q])):
        dicc = dict(OrderedDict(Counter(i).most_common()))
        vector1 = list(dicc.values())
        vectores_query['vec'+str(e+1)]= dict(zip(list(dicc.keys()), vector1))
    Q_vectors[Q] = vectores_query

# subject, fija
#print('Fasta2')
fas2 = {}
with open('docs/GCF_B2904_translated_cds.faa') as fq:
    for line in fq:
        line = line.rstrip()
        if '>' in line:
            try:
                fas2[ent] = s
            except NameError:
                ent = line.replace('>', '').split(' ')[0]
            N, s, ent = 0, '', line.replace('>', '').split(' ')[0]
        else:
            g = 0
            while g < 1:
                s += re.sub('[*]', '', line)
                g += 1
            N += 1
fas2.update({ent: {'len': len(s), 'seq': s}})
del s
for i in list(fas2.keys()):
    if len(fas2[i]) >= 50:
        pass
    else:
        fas2.pop(i)
#print('S_vectors')
S_vectors = {}
for S in fas2:
    vectores_subject = {}
    for e, i in enumerate(re.findall(int(len(fas2[S])/3)*'.', fas2[S])):
        dicc = dict(OrderedDict(Counter(i).most_common()))
        vector2 = list(dicc.values())
        vectores_subject['vec'+str(e+1)]= dict(zip(list(dicc.keys()), vector2))
    S_vectors[S] = vectores_subject


tam = int(len(list(Q_vectors.keys())) / 6)
ids = list(Q_vectors.keys())

listas = {}
for e, k in enumerate(range(0, len(ids), tam)):
    listas[e+1] = ids[k:k+tam]


N = 0.1
umbral = 0.9
#...........................................................................
def cos_similarity(entradas = [], num = ''):
    init = time_ini()
    print('Processing '+num+' ...')
    filtro = {}
    for e, Q in enumerate(entradas):
        vectores_query = Q_vectors[Q]
        q_len = len(fas1[Q])
        rec_s = []
        for S in list(S_vectors.keys()):
            if (q_len - (q_len*N)) < len(fas2[S]) < (q_len + (q_len*N)):
                vectores_subject = S_vectors[S]
                cos = []
                for q, s in zip(vectores_query, vectores_subject):
                    V1, V2 = [], []
                    for a in vectores_query[q]:
                        try:
                            vectores_subject[s][a]
                        except KeyError:
                            vectores_subject[s].update({a:0})
                        V1.append(vectores_query[q][a])
                        V2.append(vectores_subject[s][a])
                    cos_sim = 1 - spatial.distance.cosine(V1, V2)
                    cos.append(cos_sim)
                rec_s.append([S, cos])
        filtro[Q] = rec_s
        
    filtro2 = []
    for f in filtro:
        for co in filtro[f]:
            if len(np.array(co[1])[np.array(co[1]) >= umbral]) > 0:
                filtro2.append([f, co[0], np.prod(-np.log10(co[1]))])
    with open('data'+str(num)+'.txt', 'w') as fq:
        for e, i in enumerate(filtro2):
            if e+1 == len(filtro2):
                fq.write(i[0]+'\t'+i[1]+'\t'+str(i[2]))
            else:
                fq.write(i[0]+'\t'+i[1]+'\t'+str(i[2])+'\n')
    time_fin(i = init)


def proceso1():
    cos_similarity(entradas = listas[1], num = '1')
def proceso2():
    cos_similarity(entradas = listas[2], num = '2')
def proceso3():
    cos_similarity(entradas = listas[3], num = '3')
def proceso4():
    cos_similarity(entradas = listas[4], num = '4')
def proceso5():
    cos_similarity(entradas = listas[5], num = '5')
def proceso6():
    cos_similarity(entradas = listas[6], num = '6')



if __name__ == '__main__':
    
    p1 = multiprocessing.Process(name = 'Process 1', target=proceso1)
    p2 = multiprocessing.Process(name = 'Process 2', target=proceso2)
    p3 = multiprocessing.Process(name = 'Process 3', target=proceso3)
    p4 = multiprocessing.Process(name = 'Process 4', target=proceso4)
    p5 = multiprocessing.Process(name = 'Process 5', target=proceso5)
    p6 = multiprocessing.Process(name = 'Process 6', target=proceso6)
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()

    

