from django.shortcuts import render

# Create your views here.
def list(request):
    return render(request,'member/join.html')

def login(request):
    return render(request,'member/login.html')

def member(request):
    return render(request,'member/myinfo.html')