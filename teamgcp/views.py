
import sys
import json
import ast
import glob
from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token

def index(request):
    # sys.stderr.write(request)
    context = {}
    return render(request, 'index.html', context)

def registration(request):

    context = {}
    id = request.POST.get('id', False)
    context['id'] = id

    return render(request, 'registration.html', context)


def saveResult(request):
    data = json.loads(request.body)
    

    obj=ast.literal_eval(str(data))

    inputtext=obj['text'].replace(" ", "")
    user=obj['id'].replace(" ", "").lower()

    directory="teamgcp/data/"+user+"/"
    sys.stderr.write(user+","+inputtext+"\n")

    if len(obj['data']) > 0 :
        count=len(glob.glob(directory+inputtext+"_*.txt"))+1
        sys.stderr.write(str(count)+"\n")
        time=str(obj['data'][0]['down']['time'])

        filename=directory+inputtext+"_"+str(count)+".txt"
        with safe_open(filename, "w") as writefile:
            writefile.write(str(data))   

        sys.stderr.write("\t=== File saved: "+filename+" ===\n")

    # sys.stderr.write(obj.dumps(str(data)))
    # return HttpResponse(obj.dumps(RESULT_obj), content_type='application/obj')
    context = {}
    return render(request, 'index.html', context)

import os, os.path

# Taken from http://stackoverflow.com/a/600612/119527
def safe_open(path, string):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    directory=os.path.dirname(path)
    try:
        os.makedirs(directory)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(directory):
            pass
        else: raise
    return open(path, string)
