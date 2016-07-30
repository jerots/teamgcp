import numpy as np
import pandas as pd

import glob
import re

# Recursive Feature Elimination
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

# Ensemble Feature Importance
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier

def getTrainUsers():
	users=[]
	folders=glob.glob("data/train/*") #PLS EDIT

	for fd in folders:
	    users.append(fd[fd.rfind('/')+1:])
	    
	return users

def unique (seq, idfun=None): # order preserving
    if idfun is None:
        def idfun(x): 
            return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        if marker in seen: 
            continue
        seen[marker] = 1
        result.append(item)
    return result

def extractDurations(table):
    letters=table.letter
    DTs=table.down_time
    UTs=table.up_time

    HDlist=[]
    UDDlist=[]
    DDDlist=[]

    start = int(input.head(1)['down_time'].tolist()[0])        

    for i in range(len(input)):
        holddur=UTs[i]-DTs[i]
        HDlist.append(holddur)

        if(i == len(input)-1 or letters[i+1] == 'return'):
            end=UTs[i]
            UDDlist.append(0)
            DDDlist.append(0)
            break

        updowndur=DTs[i+1]-UTs[i]
        UDDlist.append(updowndur)
        DDDlist.append(holddur+updowndur)

    duration = end - start
    return letters, duration, HDlist, UDDlist, DDDlist

def selectFeatures(combined,cols):
	traindata=combined.drop(['text','user','cat'], axis=1).as_matrix(columns=None)
	labels=combined['cat'].tolist()

	### RECURSIVE FEATURE ELIMINATION
	model = LogisticRegression()
	rfe = RFE(model, 3)
	rfe = rfe.fit(traindata, labels)

	# summarize the selection of the attributes
	shortlist1=pd.DataFrame({'feature': cols[2:], 'importance':rfe.ranking_}).sort_values(by=['importance'],ascending=True)
	shortlist1=shortlist1.head(10)['feature'].tolist()
	# print(rfe.support_)
	# print(rfe.ranking_)

	### ENSEMBLE FEATURE IMPORTANCE
	model = RandomForestClassifier()
	model.fit(traindata, labels)
	# display the relative importance of each attribute
	shortlist2=pd.DataFrame({'feature':train_features, 'importance':model.feature_importances_}).sort_values(by=['importance'],ascending=False)
	# print(model.feature_importances_)

	## MERGE SHORTLISTS
	shortlist=unique(shortlist1 + shortlist2)
	return shortlist

def getTimeRecords(txt):
	users=getTrainUsers()
	df_rows = []
	cols=["text","user","duration"]
	letters=""

	for user in users:
	    filenames=glob.glob("data/train/"+user+"/"+txt+"*.csv")
	    # print 'FILENAMES:', filenames
	    
	    for filename in filenames:

	        input = pd.read_csv(filename)
	        letters, duration, HDlist, UDDlist, DDDlist = extractDurations(input)

	        userrow={}
	        userrow['text'] = txt
	        userrow['user'] = user
	        userrow['duration']=duration
	        
	        for i in range(len(letters)):
	            if(letters[i] == 'return'):
	                break
	            userrow['hd'+str(i)+'_'+letters[i]]=HDlist[i]
	            userrow['udd'+str(i)+'_'+letters[i]]=UDDlist[i]
	            userrow['ddd'+str(i)+'_'+letters[i]]=DDDlist[i]
	            userrow['hperc'+str(i)+'_'+letters[i]]=HDlist[i]*100.0/duration
	            userrow['uperc'+str(i)+'_'+letters[i]]=UDDlist[i]*100.0/duration
	            userrow['dperc'+str(i)+'_'+letters[i]]=DDDlist[i]*100.0/duration
	        df_rows.append(userrow)
	    
	for i in range(len(letters)):
        if(letters[i] == 'return'):
            break
        cols.append('hperc'+str(i)+'_'+letters[i])
        cols.append('uperc'+str(i)+'_'+letters[i])
        cols.append('dperc'+str(i)+'_'+letters[i])

    combined = pd.DataFrame(df_rows,columns=cols)
    cats=combined['user'].tolist()

	catlist=unique(cats)
	combined['cat'] = [catlist.index(x) for x in combined.user]

	return combined, cols

def getTrainRecords(txt):

	combined, cols = getTimeRecords(txt)
	shortlist=selectFeatures(combined,cols)

	dataset=combined[shortlist].drop('user', axis=1).as_matrix(columns=None)
	labels=combined['user']

	return dataset, labels

def getPxRecords(txt):

