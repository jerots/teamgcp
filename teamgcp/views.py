
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
    # sys.stderr.write(request)
    context = {}
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
        with open(filename, "w") as writefile:
            writefile.write(str(data))   

        sys.stderr.write("\t=== File saved: "+filename+" ===\n")

    # sys.stderr.write(obj.dumps(str(data)))
    # return HttpResponse(obj.dumps(RESULT_obj), content_type='application/obj')
    context = {}
    return render(request, 'index.html', context)

