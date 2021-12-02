
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


tam = int(len(list(Q_vectors.keys())) / 4)

#print('Size:', tam)
Lista1 = list(Q_vectors.keys())[:tam]
Lista2 = list(Q_vectors.keys())[tam:tam*2]
Lista3 = list(Q_vectors.keys())[tam*2:tam*3]
Lista4 = list(Q_vectors.keys())[tam*3:]

#print('Lista1:', len(Lista1), 'Lista2:', len(Lista2), 'Lista3:', len(Lista3), 'Lista4:', len(Lista4))

N = 0.1
#...........................................................................
def proceso1():
    print('Processing...')
    init = time_ini()
    #----------------
    filtro = []
    for e, Q in enumerate(Lista1):
        vectores_query = Q_vectors[Q]
        q_len = len(fas1[Q])
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
                filtro.append([Q, S, cos])
    
    filtro2 = []
    for co in filtro:
        if len(np.array(co[2])[np.array(co[2]) > 0.95]) > 0:
            filtro2.append(co)
    print(len(filtro), '>>>', len(filtro2))
    #-----------------
    time_fin(i = init)

#...........................................................................
def proceso2():
    print('Processing...')
    init = time_ini()
    #----------------
    filtro = []
    for e, Q in enumerate(Lista2):
        vectores_query = Q_vectors[Q]
        q_len = len(fas1[Q])
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
                filtro.append([Q, S, cos])
                        
    filtro2 = []
    for co in filtro:
        if len(np.array(co[2])[np.array(co[2]) > 0.95]) > 0:
            filtro2.append(co)
    print(len(filtro), '>>>', len(filtro2))
    #-----------------
    time_fin(i = init)

#...........................................................................
def proceso3():
    print('Processing...')
    init = time_ini()
    #----------------
    filtro = []
    for e, Q in enumerate(Lista3):
        vectores_query = Q_vectors[Q]
        q_len = len(fas1[Q])
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
                filtro.append([Q, S, cos])
                        
    filtro2 = []
    for co in filtro:
        if len(np.array(co[2])[np.array(co[2]) > 0.95]) > 0:
            filtro2.append(co)
    print(len(filtro), '>>>', len(filtro2))
    #-----------------
    time_fin(i = init)

#...........................................................................
def proceso4():
    print('Processing...')
    init = time_ini()
    #----------------
    filtro = []
    for e, Q in enumerate(Lista4):
        vectores_query = Q_vectors[Q]
        q_len = len(fas1[Q])
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
                filtro.append([Q, S, cos])
                        
    filtro2 = []
    for co in filtro:
        if len(np.array(co[2])[np.array(co[2]) > 0.95]) > 0:
            filtro2.append(co)
    print(len(filtro), '>>>', len(filtro2))
    #-----------------
    time_fin(i = init)


if __name__ == '__main__':
    
    p1 = multiprocessing.Process(name = 'Process 1', target=proceso1)
    p1.start()
    p2 = multiprocessing.Process(name = 'Process 2', target=proceso2)
    p2.start()
    p3 = multiprocessing.Process(name = 'Process 3', target=proceso3)
    p3.start()
    p4 = multiprocessing.Process(name = 'Process 4', target=proceso4)
    p4.start()


