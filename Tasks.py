from numpy import *
import xml.etree.ElementTree as ET  
import time


tree = ET.parse('dblp20888.xml')  
root = tree.getroot()

#Dataset
Coauthors= []
for elem in root:
    authors=[]  
    for subelem in elem:
        if subelem.tag=='author':
            authors.append(subelem.text)
    Coauthors.append(authors)

#Values
min_support=12
min_Conf=0.0

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
print("--- %s seconds took for frequent item set generation ---" % (time.time() - start_time))

# Print Frequent Itemset
L_new =[]
for M in L:
    M_new=[]
    for x in M:
        M_new.append(list(x))
    L_new.append(M_new)
print(L_new)
print("\n")


def generateRules(L, supportData, min_Conf, method):
    association_rules = []
    for i in range(1, len(L)):
        for frequentSet in L[i]:
            fset = [frozenset([item]) for item in frequentSet]
            if (i > 1):
                rules_data(frequentSet, fset, supportData, association_rules, min_Conf)
            else:
                Confidence(frequentSet, fset, supportData, association_rules, min_Conf, method)
    return association_rules         


# Method 1 - Simple Confidence
# Method 2 - Lift
# Method 3 - Max Confidence
# Method 4 - Kulczynski Confidence Measure
def Confidence(frequentSet, C, supportData, association_rules, min_Conf, method):
    C_new = []
    for item in C:
        if method==1:
            conf = supportData[frequentSet]/supportData[frequentSet-item]
        elif method==2:
            conf = supportData[frequentSet]/(supportData[frequentSet-item]*supportData[item])
        elif method==3:
            conf = max(supportData[frequentSet]/supportData[frequentSet-item], supportData[frequentSet]/supportData[item])
        else:
            conf = (supportData[frequentSet]/supportData[frequentSet-item] + supportData[frequentSet]/supportData[item])/2
        if conf >= min_Conf: 
                print (list(frequentSet-item),'==>',list(item),'Max Confidence:',conf)
                association_rules.append((frequentSet-item, item, conf))
                C_new.append(item)
            
    return C_new
    
    
def rules_data(frequentSet, C, supportData, association_rules, min_Conf):
    k = len(C[0])
    if (len(frequentSet) > (k + 1)):
        Ck = create_ck(C, k+1)
        Ck = Confidence(frequentSet, Ck, supportData, association_rules, min_Conf, method)
        if (len(Ck) > 1):   
            rules_data(frequentSet, Ck, supportData, association_rules, min_Conf)

# Method 1 - Simple Confidence
# Method 2 - Lift
# Method 3 - Max Confidence
# Method 4 - Kulczynski Confidence Measure
rules= generateRules(L,suppData, min_Conf, method=1)


