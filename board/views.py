from django.shortcuts import render

# Create your views here.
def board(request):
    return render(request, 'board/board.html')

def view(request):
    return render(request,'board/view.html')

def write(request):
    return render(request,'board/write.html')