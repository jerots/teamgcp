import numpy as np
import pandas as pd

import ast
import glob
import re

def makeCSV(mode,user,text):

	filenames=glob.glob("data/"+mode+"/"+user+"/*.txt")
	# print 'FILENAMES:', filenames

	for filename in filenames:
	    cols=['letter','username','down_time','down_x','down_y','up_time','up_x','up_y']
	    datarows=[]

	    with open(filename) as f: 
	        for submit in f:
	            json=ast.literal_eval(submit)

	            inputtext=json['text'].replace(" ", "")
	            username=user

	            isGenuine=username==inputtext
	            # print isGenuine, ",", username, ",", inputtext


	            for i in range(len(json['data'])):
	                key=json['data'][i]
	                datarow={}

	                datarow['letter']=key['letter']
	                datarow['username']=username
	                datarow['down_time']=key['down']['time']
	                datarow['down_x']=key['down']['x']
	                datarow['down_y']=key['down']['y']
	                datarow['up_time']=key['up']['time']
	                datarow['up_x']=key['up']['x']
	                datarow['up_y']=key['up']['y']

	                datarows.append(datarow)
	    df = pd.DataFrame(datarows, columns=cols)
	    
	    outputfile = filename[:filename.rfind('.')] + ".csv"
	    df.sort_values(by=['up_time']).to_csv(path_or_buf=outputfile,index=False)








