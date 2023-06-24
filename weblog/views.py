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
    return render(request, 'blog/index.html', context)
