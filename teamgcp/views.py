
import sys
import json
import ast
import glob
import os, os.path

from process import makeCSV
from test import getProbs, predict

from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token

def index(request):
    # sys.stderr.write(request)
    context = {}
    return render(request, 'index.html', context)

def registration(request):

    context = {}
    id = request.POST.get('id', 'Guest')
    context['id'] = id

    return render(request, 'registration.html', context)


def xindex(request):
    # sys.stderr.write(request)
    context = {}
    return render(request, 'xindex.html', context)

def xtrain(request):
    # sys.stderr.write(request)
    context = {}

    context = {}
    id = request.POST.get('id', 'Guest')
    context['id'] = id

    return render(request, 'xtrain.html', context)


def saveResult(request):
    data = json.loads(request.body)
    
    obj=ast.literal_eval(str(data))

    inputtext=obj['text'].replace(" ", "")
    user=obj['id'].replace(" ", "").lower()

    directory="teamgcp/data/train/"+user+"/"
    sys.stderr.write(user+","+inputtext+"\n")

    if len(obj['data']) > 0 :
        count=len(glob.glob(directory+inputtext+"_*.txt"))+1
        sys.stderr.write(str(count)+"\n")
        time=str(obj['data'][0]['down']['time'])

        filename=directory+inputtext+"_"+str(count)+".txt"
        with safe_open(filename, "w") as writefile:
            writefile.write(str(data))   

        sys.stderr.write("\t=== File saved: "+filename+" ===\n")

    makeCSV("train",user,inputtext)
    # sys.stderr.write(obj.dumps(str(data)))
    # return HttpResponse(obj.dumps(RESULT_obj), content_type='application/obj')
    context = {}
    return render(request, 'index.html', context)


def xsubmit(request):
    data = json.loads(request.body)
    
    obj=ast.literal_eval(str(data))

    inputtext=obj['text'].replace(" ", "")
    user=obj['id'].replace(" ", "").lower()

    directory="teamgcp/data/test/"+user+"/"
    sys.stderr.write(user+","+inputtext+"\n")

    if len(obj['data']) > 0 :
        count=len(glob.glob(directory+inputtext+"_*.txt"))+1
        sys.stderr.write(str(count)+"\n")
        time=str(obj['data'][0]['down']['time'])

        filename=directory+inputtext+"_"+str(count)+".txt"
        with safe_open(filename, "w") as writefile:
            writefile.write(str(data))   

        sys.stderr.write("\t=== File saved: "+filename+" ===\n")

    makeCSV("test",user,inputtext)
    probabilities = getProbs(filepath,inputtext)

    result = predict(probabilities)

    output = ('{0} >>> {1}').format(result, probabilities)

    sys.stderr.write(output)

    RESULT_JSON = {}
    RESULT_JSON['user'] = result
    RESULT_JSON['status'] = 200

    return HttpResponse(json.dumps(RESULT_JSON), content_type='application/json')


# Taken from http://stackoverflow.com/a/600612/119527
def safe_open(path, string):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    directory=os.path.dirname(path)
    try:
        os.makedirs(directory)
    except OSError as exc: # Python >2.5
        # if exc.errno == errno.EEXIST and os.path.isdir(directory):
        if os.path.isdir(directory):
            pass
        else: raise
    return open(path, string)
