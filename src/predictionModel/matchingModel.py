from flask import Flask,request,send_file,render_template,url_for,abort
from werkzeug.utils import secure_filename

import sys,os
import pandas as pd
import numpy as np
import joblib
import datetime as dt
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder


from sklearn.cluster import KMeans

# basePath="C:/Users/shafeekar.2018/hackathon/BestDealMatcher/src/cacheGenerator"
# sys.path.append(basePath)

sys.path.insert(0, os.path.abspath("../cacheGenerator"))
import createCache 

clientsCache, dealsCache, employeesCache = createCache.generateCache()

def matchingModel(name):
    employeesPublicdf, employeesPrivatedf, clientsPublicdf, clientsPrivatedf = generateDF()
    featuresPublicEmployee,featuresPrivateEmployee,featuresPublicClient,featuresPrivateClient = selectTrainData(employeesPublicdf, employeesPrivatedf, clientsPublicdf, clientsPrivatedf )
    
    listTrainingDf=[featuresPublicEmployee,featuresPrivateEmployee,featuresPublicClient,featuresPrivateClient]
    listActualDf=[employeesPublicdf, employeesPrivatedf, clientsPublicdf, clientsPrivatedf]
    listClusterCenters=[]
    selectedClientsList=[]

    for i in range(0,len(listTrainingDf)):
        labels, clusterCenters = model(listTrainingDf[i])
        listClusterCenters.append(clusterCenters)
        listActualDf[i]['Cluster'] = labels

    for i in range(0,len(listClusterCenters)//2):
        employee=listClusterCenters[i]
        client=listClusterCenters[len(listClusterCenters)//2+i]
        bestClusterNum = computeDistance(employee, client)
        df = listActualDf[len(listClusterCenters)//2+i]
        df = df[df['Cluster']==bestClusterNum]
        selectedClientsList.append(df)

    if name in employeesPublicdf["Employee Name"]:
        return selectedClientsList[0]
    else:
        return selectedClientsList[1]
    


def generateDF():
    compiledList=[]
    for k,v in employeesCache.items():
        i=[]
        i.append(k)
        i.extend(v)
        compiledList.append(i)
        
    employeesdf = pd.DataFrame(compiledList, columns=['Employee Name','Company Department','Industry',
                                                      'Region','Client Capacity (Count)','Experience (Years)',
                                                      'Designation'])
    employeesPublicdf = employeesdf[employeesdf['Designation']=='Public']
    employeesPrivatedf = employeesdf[employeesdf['Designation']=='Private']

    compiledList.clear()
    for k,v in clientsCache.items():
        i=[]
        i.append(k)
        i.extend(v)
        compiledList.append(i)
    clientsdf = pd.DataFrame(compiledList, columns=['Client Name','Company','Industry','Region',
                                                    'Years with Bank', 'Deal Type'])
    clientsPublicdf = clientsdf[clientsdf['Deal Type']=='Public']
    clientsPrivatedf = clientsdf[clientsdf['Deal Type']=='Private']
    
    return employeesPublicdf, employeesPrivatedf, clientsPublicdf, clientsPrivatedf

def selectTrainData(employeesPublicdf, employeesPrivatedf, clientsPublicdf, clientsPrivatedf):
    featuresPublicEmployee = employeesPublicdf.loc[:, ['Industry','Region','Experience (Years)']]
    featuresPublicClient= clientsPublicdf.loc[:, ['Industry','Region','Years with Bank']]
    featuresPrivateEmployee = employeesPrivatedf.loc[:, ['Industry','Region','Experience (Years)']]
    featuresPrivateClient= clientsPrivatedf.loc[:, ['Industry','Region','Years with Bank']]

    return featuresPublicEmployee,featuresPrivateEmployee,featuresPublicClient,featuresPrivateClient

def model(df):
    # featuresPublicEmployee = employeesPublicdf.loc[:, ['Industry','Region','Experience (Years)']]
    # featuresPublicClient= clientsPublicdf.loc[:, ['Industry','Region','Years with Bank']]

    lb_style = LabelEncoder()

    for i in df:
        if df[i].dtypes=='object':
            df[i]= lb_style.fit_transform(df[i])

    # getOptimalNumberOfClusters(df)
    kmeanModel = KMeans(n_clusters=2) #change n_clusters accordingly to elbow point
    kmeanModel.fit(df)

    return kmeanModel.labels_ + 1,  kmeanModel.cluster_centers_


def getOptimalNumberOfClusters(feature):
    distortions = []
    K = range(1,10)
    for k in K:
        kmeanModel = KMeans(n_clusters=k)
        kmeanModel.fit(feature)
        distortions.append(kmeanModel.inertia_)
        
    plt.figure(figsize=(16,8))
    plt.plot(K, distortions, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Distortion')
    plt.title('Elbow Graph')
    plt.show()

def computeDistance(employee, client):
    clientCluster = 0

    for i in range(0,len(employee)):
        distSmallest = sys.maxsize
        for j in range(0,len(client)):
            dist = np.linalg.norm(employee[i] - client[j])
            if dist < distSmallest:
                distSmallest = dist
                clientCluster = j
    # print(distSmallest)
    return j

if __name__=="__main__":
    print(len(matchingModel("Richard Roberts").index))
