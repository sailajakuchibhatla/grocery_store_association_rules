'''
Sailaja Kuchibhatla
'''
import math

def isSupported(db, items, minsup, totalTrans):
    tempDict = {}
    for tid in db:
        for item in items:
            if item.issubset(db[tid]):
                if item in tempDict:
                    tempDict[item] += 1
                else:
                    tempDict[item] = 1
                    
    res = {}
    for x in tempDict:
        if (tempDict[x]/totalTrans)*100 >= minsup:
            res[x] = tempDict[x]
    return res

def printSet(tempSet,sup = 0,res = 0):
    for x in tempSet:
        if sup == 1:
            print(list(x),"is supported")
        elif res == 1:
            print(list(x))
        else:
            print(list(x),"is itemset")
    print()
    print()


def combineSet(tempSet):
    sLen = len(tempSet)
    if sLen == 1 or sLen == 0:
        return -1
    resSet = set()
    for x in tempSet:
        for y in tempSet:
            if x != y:
                if len(x) == 1:
                    resSet.add(x.union(y))
                elif len(x) > 1:
                    if len(x.intersection(y)) > 0:
                        resSet.add(x.union(y))
    if len(resSet) == sLen:
        return -1
    return resSet
        
    
def getSupportedItemsets(db, totalTrans, minsup):
    allItems = set()
    for tid in db:
        dbSet = db[tid]
        for x in dbSet:
            allItems.add(frozenset({x}))

    print("#### STARTING APRIORI ####")
    print()
    printSet(allItems)

    resultItemset = {}
    done = False
    while not done:
        validSet = isSupported(db, allItems,minsup, totalTrans)
        for x in validSet:
            resultItemset[x] = validSet[x]
        printSet(validSet,1)
        newItemset = combineSet(validSet)
        if newItemset == -1:
            break
        allItems = newItemset
        printSet(allItems)

    return resultItemset

def getAssociationRules(db, totalTrans, minconf, itemset):
    tempRules = []
    for item in itemset:
        if len(item) != 1:
            item = list(item)
            setSize = int(math.pow(2,len(item)))
            for i in range(0, setSize):
                temp = set()
                for j in range(0, len(item)): 
                    if((i & (1 << j)) > 0): 
                        temp.add(item[j])
                if len(temp) != len(item) and len(temp) != 0:
                    tempSet = set(item)
                    tempSet = tempSet.difference(temp)
                    tempRules.append({frozenset(temp):tempSet})
                    
    print("All POTENTIAL Association Rules")
    print(tempRules)
    print()

    resultRules = {}
    for x in tempRules:
        for y in x:
            temp = frozenset(set(y).union(x[y]))
            supportOfAll = itemset[temp]
            temp = frozenset(y)
            supportOfLeft = itemset[temp]
            if (supportOfAll/supportOfLeft)*100 >= minconf:
                resultRules[temp] = x[y]

    return resultRules          


def printAssociationRules(rules):
    print("############### Resulting Association Rules ###############")
    for x in rules:
        print(', '.join(list(x)), end="")
        print("  ->  ", end="")
        print(', '.join(list(rules[x])))
    print()
    
dbNum = 1

while True:
    print()
    print("------------------------------ Database ", dbNum,"------------------------------")

    minsup = input("Enter Minimum Support (%) : ")
    minconf = input("Enter Minimum Confidence (%): ")
    print()
    try:
        minsup = int(minsup)
        minconf = int(minconf)
    except:
        print("Please enter numbers only")
        print()
        continue

    # read in db file
    db = {}
    dbFileName = "DB"+str(dbNum)+".txt"
    with open(dbFileName,"r") as dbFile:
        lines = dbFile.readlines()
        for line in lines:
            line = line.rstrip()
            line = line.split(", ")
            db[int(line[0])] = set(line[1:])

    print("DataBase:\n",db)
    print()

    totalTransactions = len(db)

    validItemsets = getSupportedItemsets(db,totalTransactions,minsup)
    print("Itemsets with Minimum Support: ")
    printSet(validItemsets,0,1)
    print()
    rules = getAssociationRules(db,totalTransactions, minconf, validItemsets)
    printAssociationRules(rules)

    
    if dbNum == 5:
        print("End of Databases")
        break
    
    dbNum += 1

