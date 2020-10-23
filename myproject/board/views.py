from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from .models import Type, Company, Post, Comment
from .forms import PostForms, CommentForms

User = get_user_model()

# 메인페이지 뷰


class MainPageView(TemplateView):
    template_name = 'mainpage.html'

    # context 뿌리는 메소드
    def get_context_data(self, **kwargs):

        user = self.request.user
        outer = Type.objects.all()

        context = {'user': user, 'outer': outer}
        return context

# 큰 계열 4개


def lotte_outer(request, pk):
    # company 값이 lotte_outer에 같이 넘어감
    company = Type.objects.get(pk=pk)
    outer = Type.objects.get(pk=pk)

    return render(request, 'lotte_outer.html', {'company': company, 'outer': outer})

# 회사 목록 추가(추가 다하면 없어도 O)


def lotte_add(request, pk):
    company = get_object_or_404(Type, pk=pk)

    if request.method == 'POST':
        subject = request.POST['subject']

        topic = Company.objects.create(
            subject=subject,
            company_type=company
        )

        return redirect('lotte_outer', pk=company.pk)
    return render(request, 'lotte_add.html', {'company': company})

####### post/views.py 합치기 #######


def index(request, pk):
    # company_type = Company.objects.get(pk=pk)
    # company_type = Company.objects.all()
    specific_company_type = Company.objects.get(pk=pk)
    company_post = Post.objects.filter(boards_number=specific_company_type)

    all_post = Post.objects.all()

    context = dict()
    #####
    company = Company.objects.get(pk=pk)
    context['company'] = company
    context['all_post'] = all_post
    context['specific_company_type'] = specific_company_type
    context['company_post'] = company_post

# company = Type.objects.get(pk=pk)
# outer = Type.objects.get(pk=pk)

# context = {'outer': outer}

# company = Type.objects.get(pk=pk)
# outer = Type.objects.get(pk=pk)
# context['company'] = company
# context['outer'] = outer
    return render(request, 'index.html', context)


def create(request, pk):
    context = dict()

    company_chk = Company.objects.get(pk=pk)

    context['company_chk'] = company_chk

    if request.method == 'POST':
        # media 파일 올려주려면, request.FILES 추가해주어야한다.
        temp_form = PostForms(request.POST, request.FILES)
        # temp_form.photo = request.FILES['image']

        if temp_form.is_valid():
            clean_form = temp_form.save(commit=False)
            clean_form.author = User.objects.get(id=request.user.id)
            # 추후에 User.id 할당해야해
            clean_form.save()

            return redirect('index', pk)
        else:
            context['write_form'] = PostForms()
            return render(request, 'write.html', context)
    else:
        context['write_form'] = PostForms()
        return render(request, 'write.html', context)


def detail(request, pk, post_id):
    context = dict()

    detail_post = Post.objects.get(id=post_id)
    
    company_chk = Company.objects.get(pk=pk)

    context['detail_post'] = detail_post
    context['comment_form'] = CommentForms()
    context['comment_all'] = Comment.objects.filter(
        post=Post.objects.get(id=post_id))  # 얘가 listview역할
    context['company_chk'] = company_chk

    return render(request, 'detail.html', context)


def update(request, pk, post_id):
    context = dict()
    company_chk = Company.objects.get(pk=pk)
    
    context['company_chk'] = company_chk
    
    if request.method == "POST":
        temp_form = PostForms(request.POST, request.FILES,
                              instance=Post.objects.get(id=post_id))

        if temp_form.is_valid():
            temp_form.save()
            return redirect('index', pk)
        else:
            context["write_form"] = temp_form
            return render(request, 'write.html', context)
    else:
        context["write_form"] = PostForms(
            instance=Post.objects.get(id=post_id))
        return render(request, 'write.html', context)


def delete(request, pk, post_id):
    detail_post = Post.objects.get(id=post_id)
    detail_post.delete()

    # User 정보 받아올 수 있을때 사용
    # if detail_post.author == request.user:
    #     detail_post.delete()
    return redirect('index', pk)


def create_comment(request, pk, post_id):
    company_index = Company.objects.get(pk=pk)
    context = {'company_index': company_index}

    if request.method == "POST":
        temp_form = CommentForms(request.POST)
        if temp_form.is_valid():
            clean_form = temp_form.save(commit=False)

            clean_form.post = Post.objects.get(id=post_id)
            clean_form.author = User.objects.get(id=request.user.id)

            clean_form.save()
            temp_form.save()
        return redirect('detail', pk, post_id)


def comment_delete(request, pk, post_id, com_id):
    del_com = Comment.objects.get(id=com_id)
    del_com.delete()
    return redirect('detail', pk, post_id)


def scrap(request, post_id):
    context = dict()
    target_post = Post.objects.get(id=post_id)
    if target_post.scrap.filter(id=request.user.id):
        target_post.scrap.remove(request.user)
        print("유저가 있다가 제거되었습니다.")
        context["flag"] = "None"
    else:
        target_post.scrap.add(request.user)
        print("user가 없다가 추가되었습니다")
        context["flag"] = "Exist"

    print(target_post.scrap.all())
    context["len"] = len(target_post.scrap.all())

    return HttpResponse(json.dumps(context), content_type='application/json')
