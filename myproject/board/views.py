from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
# 메인페이지 뷰
class MainPageView(TemplateView):
    template_name = 'mainpage.html'
    
    # context 뿌리는 메소드
    def get_context_data(self, **kwargs):

        user = self.request.user
        context = {'user': user}
        return context

def food(request):
    return render(request, 'food.html')

def retail(request):
    return render(request, 'retail.html')

def chem(request):
    return render(request, 'chem.html')

def tour(request):
    return render(request, 'tour.html')
