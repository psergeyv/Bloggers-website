from django.shortcuts import render, get_object_or_404
import datetime as dt
from .models import Post, Group, Comment, Follow
from django.shortcuts import redirect
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

def page_not_found(request, exception):
        return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
        return render(request, "misc/500.html", status=500)

def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page, 'paginator': paginator})

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "group.html", {"group": group, 'page': page, 'paginator': paginator})    
    
@login_required
def new_post(request):
    text_form = {"title": "Добавить запись", "btn": "Добавить"} 
    
    if request.method == 'POST':
        form = PostForm(request.POST or None, files=request.FILES or None)
        
        if form.is_valid():    
            group = form.cleaned_data['group']
            text = form.cleaned_data['text']
            image = form.cleaned_data['image']
                             
            new = Post.objects.create(author=request.user, group=group, text=text, image=image)
            
            return redirect('index')
        return render(request, "new.html",{"form":form,"text_form":text_form}) 
    form = PostForm()   
    
    return render(request, "new.html",{"form":form,"text_form":text_form}) 

@login_required
def post_edit(request, username, post_id):
    text_form = {"title": "Редактировать запись", "btn": "Сохранить"} 
    post = get_object_or_404(Post, id=post_id)


    if post.author != request.user:
        return redirect('post', username, post_id)
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)           
    if request.method == 'POST':
        if form.is_valid():    
            form.save()
            return redirect('post', username, post_id)
        return render(request, "new.html",{"form":form, "text_form":text_form}) 
   
    
    if post:
        group = post.group
        text = post.text        
                 
    else:
        return redirect('profile', username)      
    
    return render(request, "new.html",{"form":form, "text_form":text_form})    

def profile(request, username):
    User = get_user_model()
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author).order_by("-pub_date").all()
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)   
    following = {}
    if request.user.is_authenticated:
        following = Follow.objects.filter(author=author, user=request.user).all()


    return render(request, "profile.html", {"profile":author, 'page': page, 'paginator': paginator, 'following':following})

def post_view(request, username, post_id):
    User = get_user_model()
    author = get_object_or_404(User, username=username)

    posts = Post.objects.filter(author=author).all()
    view_post = Post.objects.get(id=post_id)
    form = CommentForm(request.POST or None, instance=view_post)

    items = Comment.objects.filter(post=view_post.id).all() 
    return render(request, 'post.html', {"profile":author, 'post': view_post, "count_posts":len(posts),"form":form, 'items':items})

@login_required
def add_comment(request, username, post_id):
    
    post = get_object_or_404(Post, id=post_id)
    post_id = post.id
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():    
            
            text = form.cleaned_data['text']
                             
            new = Comment.objects.create(author=request.user, post=post, text=text)
            
            return redirect('post', username, post_id)
        return redirect('index', username, post_id) 
    
    
    return redirect('index', username, post_id)    

@login_required
def follow_index(request):
    follow = Follow.objects.filter(user=request.user)
    user_authors = []
    for autors in follow:        
        user_authors.append(autors.author.id)
    follows = Post.objects.filter(author__in=user_authors).order_by("-pub_date").all()
    paginator = Paginator(follows, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "follow.html", {'page':page})

@login_required
def profile_follow(request, username):
    User = get_user_model()
    author = get_object_or_404(User, username=username)
    new = Follow.objects.create(user=request.user, author=author)
    return redirect('profile', username)


@login_required
def profile_unfollow(request, username):
    User = get_user_model()
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.get(author=author, user=request.user)
    follow.delete()
    return redirect('profile', username)