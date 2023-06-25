from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout
from .models import Post
from .forms import PostForm, SignUpForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Post, Comment
from .forms import CommentForm


def comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('weblog:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'weblog/comment.html', {'post': post, 'comments': comments, 'form': form})


def index(request):
    post_list = Post.objects.order_by('-created_at')
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {'post_list': page_obj, 'page_obj': page_obj}
    if not post_list.exists():
        context = {'post_list': None, 'page_obj': page_obj}
        return render(request, 'weblog/index.html', context)
    return render(request, 'weblog/index.html', context)


def new_post(request):
    if not request.user.is_authenticated:
        return render(request, '404.html')
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('weblog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'weblog/new_post.html', {'form': form})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.delete()
        messages.success(request, 'The post was deleted successfully!')
    else:
        messages.error(request, 'You are not authorized to delete this post!')
    return redirect('weblog:index')


def edit_post(request, pk):
    if not request.user.is_authenticated:
        return render(request, '404.html')
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('weblog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'weblog/edit_post.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment = Comment.objects.filter(post=post)
    return render(request, 'weblog/post_detail.html', {'post': post, 'comments': comment})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            return redirect('weblog:login')
    else:
        form = SignUpForm()
    return render(request, 'weblog/signup.html', {'form': form})


def handler404(request, exception=None):
    return render(request, '404.html', status=404)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(email=username).first()
        if user is not None and user.check_password(password):
            login(request, user)
            return redirect('weblog:index')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'weblog/login.html')


def logout_view(request):
    if not request.user.is_authenticated:
        return render(request, '404.html')
    logout(request)
    return redirect('weblog:index')


def fetch_users(request):
    user_count = User.objects.count()
    data = {
        'user_count': user_count
    }
    return JsonResponse(data)
