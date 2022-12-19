from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .forms import PostForm
from .models import Group, Post, User


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/index.html', {
        'page_obj': page_obj,
    })


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()

    paginator = Paginator(post_list, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/group_list.html', {
        'group': group,
        'page_obj': page_obj,
    })


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()

    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/profile.html', {
        'author': author,
        'page_obj': page_obj,
    })


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = post.author

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'author': author,
    })


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse_lazy(
                'posts:profile',
                kwargs={'username': request.user},
            ))
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {
        'form': form,
    })


@login_required
def post_edit(request, post_id):
    post = Post.objects.get(pk=post_id)
    if post.author != request.user:
        return redirect(reverse_lazy(
            'posts:post_detail',
            kwargs={'post_id': post_id},
        ))

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy(
                'posts:post_detail',
                kwargs={'post_id': post_id},
            ))
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/create_post.html', {
        'form': form,
        'is_edit': True,
    })
