from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'main.html')

def food(request):
    return render(request, 'food.html')

def retail(request):
    return render(request, 'retail.html')

def chem(request):
    return render(request, 'chem.html')

def tour(request):
    return render(request, 'tour.html')
