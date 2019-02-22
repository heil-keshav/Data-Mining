from numpy import *
import xml.etree.ElementTree as ET  
import time


tree = ET.parse('dblp20888.xml')  
root = tree.getroot()

# Coauthors - Dataset
Coauthors= []
for elem in root:
    authors=[]  
    for subelem in elem:
        if subelem.tag=='author':
            authors.append(subelem.text)
    Coauthors.append(authors)


min_support=12

def create_C1(D):
    C1 = []
    for tid in D:
        for item in tid:
            if not [item] in C1:
                C1.append([item])         
    C1.sort()
    return list(map(frozenset, C1))

def create_Lk(D, Ck, min_support):
    L={}
    for tid in D:
        for c in Ck:
            if c.issubset(tid):
                if not c in L: 
                    L[c]=1
                else: 
                    L[c] += 1
    retList = []
    supportData = {}
    
    for key in L:
        support = L[key]
        if support >= min_support:
            retList.insert(0,key)
        supportData[key] = support
    return retList, supportData

def create_ck(Lk, k): 
    retList = []
    for i in range(len(Lk)):
        for j in range(i+1, len(Lk)): 
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1==L2: 
                retList.append(Lk[i] | Lk[j])
    return retList
    

def apriori(D):
    global min_support
    C1 = create_C1(D)
    L1, supportData = create_Lk(D, C1, min_support)
    L = [L1]
    k = 2
    
    while (len(L[k-2]) > 0):
        Ck = create_ck(L[k-2], k)
        Lk, supK = create_Lk(D, Ck, min_support)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData


start_time = time.time()
L,suppData = apriori(Coauthors)
print("--- %s seconds ---" % (time.time() - start_time))

# Print Frequent Itemset
L_new =[]
for M in L:
    M_new=[]
    for x in M:
        M_new.append(list(x))
    L_new.append(M_new)
print(L_new)
