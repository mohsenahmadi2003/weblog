from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Post
from .forms import PostForm, SignUpForm


def index(request):
    post_list = Post.objects.order_by('-created_at')[:5]
    paginator = Paginator(Post.objects.order_by('-created_at'), 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'post_list': post_list, 'page_obj': page_obj}
    return render(request, 'weblog/index.html', context)


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'weblog/new_post.html', {'form': form})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'weblog/edit_post.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'weblog/post_detail.html', {'post': post})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.bio = form.cleaned_data.get('bio')
            user.profile.avatar = form.cleaned_data.get('avatar')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('blog:index')
    else:
        form = SignUpForm()
    return render(request, 'weblog/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog:index')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'weblog/login.html')


def logout_view(request):
    logout(request)
    return redirect('blog:index')
