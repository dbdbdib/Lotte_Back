from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from .models import Type, Company, Board
from post.forms import PostForms, CommentForms

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

# 회사 목록 추가(추가 다하면 없어도 O)
def lotte_add(request, pk):
    company = get_object_or_404(Type, pk=pk)

    if request.method == 'POST':
        subject = request.POST['subject']

        topic = Company.objects.create(
            subject=subject,
            company=company
        )

        return redirect('lotte_outer', pk=company.pk)
    return render(request, 'lotte_add.html', {'company':company})

##############################################

def board_post(request, company_pk):
    try:
        if request.method == "POST":
            myform = BoardForm(request.POST, request.FILES)
            if myform.is_valid():
                myform.save()
                return redirect('/bulletinboard_page/{}'.format(cafe_id))
        myform = BoardForm()

        all_post = Board.objects.all()
        context = {'take_all_post':all_post, 'profile':profile}
        return render(request, 'createpost.html', context)
    except:
        if request.method == "POST":
            myform = BoardForm(request.POST, request.FILES)
            if myform.is_valid():
                myform.save()
                return redirect('/bulletinboard_page/{}'.format(cafe_id))

        all_post = Board.objects.all()
        context = {'take_all_post':all_post}
        return render(request, 'createpost.html', context)
