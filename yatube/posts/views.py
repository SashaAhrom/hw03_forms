from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


def index(request):
    """Passes the last ten Post model objects and title."""
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Passes the last ten Post model objects
    filtered by group field and title."""
    group = get_object_or_404(Group, slug=slug)
    post_list = group.community.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
        'title': group.title
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """All posts author."""
    author = get_object_or_404(User, username=username)
    post_list = author.author_posts.all()
    count_posts = post_list.count()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = f'Профайл пользователя {author}'
    context = {
        'count_posts': count_posts,
        'page_obj': page_obj,
        'author': author,
        'title': title
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Post details."""
    post = get_object_or_404(Post, pk=post_id)
    post_count = Post.objects.filter(author=post.author).count()
    title = f'Пост {post.text[:30]}'
    if post.author.id == request.user.id:
        is_edit = True
    else:
        is_edit = False
    context = {
        'post': post,
        'title': title,
        'post_count': post_count,
        'is_edit': is_edit
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    """Create post."""
    if not request.user.id:
        return redirect('/auth/login/')
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author_id = request.user.id
            post.save()
            return redirect(f'/profile/{request.user.username}/')
        return render(request, 'posts/create_post.html', {'form': form})
    form = PostForm()
    context = {
        'form': form
    }
    return render(request, 'posts/create_post.html', context)


def post_edit(request, post_id):
    """Post edit."""
    post = get_object_or_404(Post, pk=post_id)
    if post.author.id != request.user.id:
        return redirect(f'/posts/{post.pk}/')
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(f'/posts/{post.pk}/')
    form = PostForm(instance=post)
    context = {
        'is_edit': True,
        'form': form,
        'post': post
    }
    return render(request, 'posts/create_post.html', context)
