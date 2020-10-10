from django.shortcuts import render
from django.views.generic import TemplateView
from .models import CompanyType, Company

# 메인페이지 뷰
class MainPageView(TemplateView):
    template_name = 'mainpage.html'
    
    # context 뿌리는 메소드
    def get_context_data(self, **kwargs):
        companytype = CompanyType.objects.all()

        user = self.request.user
        context = {'user': user, 'companytype':companytype}
        return context

# 계열사 안에 회사들
def company(request, pk):
    try:
        # ct : 계열 분류
        ct = CompanyType.objects.get(pk=pk)
        company = Company.objects.all()
    except CompanyType.DoesNotExist:
        raise Http404
    return render(request, 'company.html', {'ct': ct, 'company':company})

def board(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'boardpost.html', {'board': board})