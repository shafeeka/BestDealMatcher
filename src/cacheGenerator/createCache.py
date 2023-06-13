import csv
import traceback

basePath="C:/Users/shafeekar.2018/hackathon/BestDealMatcher/resource"
clientsCache = {}
dealsCache = {}
employeesCache = {}

def generateCache():
    try:
        generateClientCache()
        generateEmployeesCache()
        generateDealsCache()
    
    except Exception as e:
        print("Exception occured during cache creation")
        traceback.print_exc()
    
    return clientsCache, dealsCache, employeesCache

def generateClientCache():
    try:
        clientFilename = basePath+'/clients.csv'
        with open(clientFilename, 'r') as csvfile:
            datareader = csv.reader(csvfile)
            next(datareader)
            for row in datareader:
                k=row[0]
                v=row[1:]
                clientsCache[k] = v
    except Exception as e:
        print("Exception occured during CLIENT cache creation")
        traceback.print_exc()
        raise e
    finally:
        csvfile.close()

def generateEmployeesCache():
    employeesFilename = basePath+'/employees.csv'
    try:
        with open(employeesFilename, 'r') as csvfile:
            datareader = csv.reader(csvfile)
            next(datareader)
            for row in datareader:
                k=row[0]
                v=row[1:]
                employeesCache[k] = v
    except Exception as e:
        print("Exception occured during EMPLOYEES cache creation")
        traceback.print_exc()
        raise e
    finally:
        csvfile.close()

def generateDealsCache():
    employeeDealTypeDict={}
    try:
        dealsFilename = basePath+'/deals.csv'
        with open(dealsFilename, 'r') as csvfile:
            datareader = csv.reader(csvfile)
            next(datareader)
            for row in datareader:
                k=row[0]
                v=row[1:]
                dealsCache[k] = v

                if row[3] in employeeDealTypeDict.keys():

                    employeeDealTypeDict[row[3]].append(row[len(row)-1])
                else:
                    employeeDealTypeDict[row[3]] = [row[len(row)-1]]

        addDealTypeToEmployeesCache(employeeDealTypeDict)
    except Exception as e:
        print("Exception occured during DEAL cache creation")
        traceback.print_exc()
        raise e
    finally:
        csvfile.close()

def addDealTypeToEmployeesCache(employeeDealTypeDict):
    for k,v in employeeDealTypeDict.items():
        if 'Private' in v:
            clientsCache[k].append('Private')
        else:
            clientsCache[k].append('Public')


if __name__ == "__main__":
    clientsCache, dealsCache, employeesCache = generateCache()
    # print(clientsCache)
    # print("=======")
    # print(dealsCache)
    # print("=======")
    # print(employeesCache)