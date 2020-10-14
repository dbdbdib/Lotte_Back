from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from .models import Type, Company

# 메인페이지 뷰
class MainPageView(TemplateView):
    template_name = 'mainpage.html'
    
    # context 뿌리는 메소드
    def get_context_data(self, **kwargs):

        user = self.request.user
        outer = Type.objects.all()

        context = {'user': user, 'outer':outer}
        return context
        
# 큰 계열 4개
def lotte_outer(request, pk):
    company = Type.objects.get(pk=pk)
    return render(request, 'lotte_outer.html', {'company':company})

def lotte_inner(request, pk):
    company = get_object_or_404(Type, pk=pk)

    if request.method == 'POST':
        subject = request.POST['subject']

        topic = Company.objects.create(
            subject=subject,
            company=company
        )

        return redirect('lotte_outer', pk=company.pk)
    return render(request, 'lotte_inner.html', {'company':company})