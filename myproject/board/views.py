from django.shortcuts import render
from django.views.generic import TemplateView
from .models import CompanyType, Company

# from .models import Food, Chem, Retail, Tour

# # 메인페이지 뷰
class MainPageView(TemplateView):
    template_name = 'mainpage.html'
    # context 뿌리는 메소드
    def get_context_data(self, **kwargs):
        companytype = CompanyType.objects.all()

        user = self.request.user
        context = {'user': user,
        'companytype': companytype}
        
        return context
def foodcompany(request):
    company = Company.objects.all()
    context = {'company': company}
    return render(request, 'food.html', context)
# def food(request):
#     all_food = Food.objects.all()
#     context = {'all_food':all_food}
#     return render(request, 'food.html', context)

# def food_board(request, board_id):
#     food_num = Food.objects.get(id=board_id)
#     context['food_num'] = food_num
#     return render(request, 'post/index.html', context)

# def retail(request):
#     all_retail = Retail.objects.all()
#     context = {'all_retail':all_retail}
#     return render(request, 'retail.html', context)

# def retail_board(request, board_id):
#     retail_num = Retail.objects.get(id=board_id)
#     context['retail_num'] = retail_num
#     return render(request, 'post/index.html', context)
    
# def chem(request):
#     all_chem = Chem.objects.all()
#     context = {'all_chem':all_chem}
#     return render(request, 'chem.html', context)

# def chem_board(request, board_id):
#     chem_num = Chem.objects.get(id=board_id)
#     context['chem_num'] = chem_num
#     return render(request, 'post/index.html', context)

# def tour(request):
#     all_tour = Tour.objects.all()
#     context = {'all_tour':all_tour}
#     return render(request, 'tour.html', context)

# def tour_board(request, board_id):
#     tour_num = Tour.objects.get(id=board_id)
#     context['tour_num'] = tour_num
#     return render(request, 'post/index.html', context)