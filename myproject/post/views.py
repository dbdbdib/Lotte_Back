from django.shortcuts import render, redirect
from .models import Post, Comment
#, Photo
from .forms import PostForms, CommentForms
from django.contrib.auth import get_user_model

# Create your views here.
def index(request):

    all_post = Post.objects.all()

    context = dict()
    context['all_post'] = all_post

    return render(request, 'index.html', context)

def create(request):
    context = dict()

    if request.method == 'POST':
        temp_form = PostForms(request.POST)
        if temp_form.is_valid():
            clean_form = temp_form.save()
            # 추후에 User.id 할당해야해

            # for img in request.FILES.getlist('imgs'):
            #      # Photo 객체를 하나 생성한다.
            #     photo = Photo()
            # # 외래키로 현재 생성한 Post의 기본키를 참조한다.
            #     photo.post = clean_form
            # # imgs로부터 가져온 이미지 파일 하나를 저장한다.
            #     photo.image = img
            # # 데이터베이스에 저장
            #     clean_form = photo.save()
            clean_form.save()
            return redirect('post')
        else:
            context['write_form'] = temp_form
            return render(request, 'write.html', context)
    else:

        context['write_form'] = PostForms()
        return render(request, 'write.html', context)

def detail(request,post_id):
    context = dict()
    detail_post = Post.objects.get(id = post_id)
    context['detail_post'] = detail_post
    context['comment_form'] = CommentForms()
    context['comment_all'] = Comment.objects.filter(post= Post.objects.get(id = post_id)) # 얘가 listview역할
    return render(request,'detail.html',context)
        
def update(request,post_id):
    context = dict()
    
    if request.method == "POST":
        temp_form = PostForms(request.POST,instance=Post.objects.get(id = post_id))
        
        if temp_form.is_valid():
            temp_form.save()
            return redirect('post')
        else:
            context["write_form"] = temp_form
            return render(request,'write.html',context)
    else:
        context["write_form"] = PostForms(instance=Post.objects.get(id = post_id))
        return render(request,'write.html', context)
        
        
def delete(request,post_id):
    detail_post = Post.objects.get(id = post_id)
    detail_post.delete()
    
    # User 정보 받아올 수 있을때 사용
    # if detail_post.author == request.user:
    #     detail_post.delete()
    return redirect('post')
    
def create_comment(request,post_id):
    if request.method=="POST":
        temp_form = CommentForms(request.POST)
        if temp_form.is_valid():
            clean_form = temp_form.save(commit=False)
            clean_form.post = Post.objects.get(id = post_id )
            clean_form.save()
            temp_form.save()
        return redirect('detail', post_id)
        
def comment_delete(request,post_id, com_id):
    del_com = Comment.objects.get(id=com_id)
    del_com.delete()
    return redirect('detail', post_id)
