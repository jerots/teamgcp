
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
    # sys.stderr.write(data['letter'])
    # sys.stderr.write(request.POST);

    json=ast.literal_eval(data)

    inputtext=json['text'].replace(" ", "")
    user=json['id']

    if len(json['data']) > 0 :
        time=str(json['data'][0]['down']['time'])
        with open("data/"+user+"/"+inputtext+"_"+time+".txt", "w") as writefile:
            writefile.write(data)    

    sys.stderr.write(json.dumps(data))
    # return HttpResponse(json.dumps(RESULT_JSON), content_type='application/json')
    context = {}
    return render(request, 'index.html', context)

