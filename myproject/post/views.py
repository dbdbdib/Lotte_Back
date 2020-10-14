from django.shortcuts import render, redirect
from .models import Post, Comment
from django.http import HttpResponse
import json

from .forms import PostForms, CommentForms
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def index(request):
    all_post = Post.objects.all()

    context = dict()
    context['all_post'] = all_post

    return render(request, 'index.html', context)

def create(request):
    context = dict()
    if request.method == 'POST':
        # media 파일 올려주려면, request.FILES 추가해주어야한다.
        temp_form = PostForms(request.POST, request.FILES)
        # temp_form.photo = request.FILES['image']

        if temp_form.is_valid():
            clean_form = temp_form.save()
            clean_form.author = User.objects.get(id = request.user.id)
            # 추후에 User.id 할당해야해
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
        temp_form = PostForms(request.POST,request.FILES, instance=Post.objects.get(id = post_id))
        
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
            clean_form.author = User.objects.get(id = request.user.id)

            clean_form.save()
            temp_form.save()
        return redirect('detail', post_id)
        
def comment_delete(request,post_id, com_id):
    del_com = Comment.objects.get(id=com_id)
    del_com.delete()
    return redirect('detail', post_id)


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