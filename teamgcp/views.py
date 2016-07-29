
import sys
import json
from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token

def index(request):
    # sys.stderr.write(request)
    context = {}
    return render(request, 'index.html', context)


def saveResult(request):
    data = json.loads(request.body)
    # sys.stderr.write(data['letter'])
    # sys.stderr.write(request.POST);

    sys.stderr.write(json.dumps(data))

    # return HttpResponse(json.dumps(RESULT_JSON), content_type='application/json')

    context = {}
    return render(request, 'index.html', context)

