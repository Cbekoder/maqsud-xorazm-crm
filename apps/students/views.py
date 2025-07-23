from daff import View
from django.shortcuts import render

def BaseView(request):
    return render(request, "base.html")