
import sys
from django.shortcuts import render

def index(request):
    # sys.stderr.write(request)
    context = {}
    return render(request, 'index.html', context)