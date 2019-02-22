from numpy import *
import xml.etree.ElementTree as ET  
import time

tree = ET.parse('dblp20888.xml')  
root = tree.getroot()

Authors= []
Articles=[]
counter=0
for elem in root: 
    counter += 1 
    for subelem in elem:
        if subelem.tag=='author':
            if subelem.text in Authors:
                 ind = Authors.index(subelem.text)
                 Articles[ind].append(counter)
            else:
                 Authors.append(subelem.text)
                 Articles.append([counter])

min_support = 12

def frequency(D, L):
    global Authors
    common_transac=D[Authors.index(L[0])]
    for i in range(1, len(L)):
        ind = Authors.index(L[i])
        common_transac= list(set(common_transac) & set(D[ind])) 
    return len(common_transac)

def support(item):
    if item[1] >= min_support:
       return True
    else:
       return False
         

frequent_items =[]
def eclat(prefix, items, D):
    if not items: return
    candidates = [(prefix | {i}, frequency(D, list(prefix | {i})), i)
                  for i in items if i not in prefix]
    frequent = filter(support, candidates)

    for new_prefix, freq, i in frequent:
        frequent_items.append(new_prefix)
        items = items - {i}
        eclat(new_prefix, items, D)
        
        
start_time = time.time()
eclat(set(), set(Authors), Articles)
print("--- %s seconds ---" % (time.time() - start_time))
print(frequent_items)


