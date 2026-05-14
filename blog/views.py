from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category, Comment
from django.shortcuts import redirect
from .forms import CommentForm   # we'll create this next
from django.contrib.auth.models import User

def post_list(request):
    search_query = request.GET.get('q', '')
    
    posts = Post.objects.filter(status='published').order_by('-published_at')
    
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    featured_post = Post.objects.filter(status='published', is_featured=True).first()
    
    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    popular_posts = Post.objects.filter(status='published').order_by('-views')[:5]
    categories = Category.objects.all()

    context = {
        'posts': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'featured_post': featured_post,
        'popular_posts': popular_posts,
        'categories': categories,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Increment views
    post.views += 1
    post.save(update_fields=['views'])

    # Get top-level comments
    comments = post.comments.filter(parent=None)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            
            # Handle Reply
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    new_comment.parent = Comment.objects.get(id=parent_id)
                except Comment.DoesNotExist:
                    pass  # fallback if invalid parent
            
            new_comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()

    popular_posts = Post.objects.filter(status='published').order_by('-views')[:5]
    categories = Category.objects.all()
    related_posts = Post.objects.filter(category=post.category, status='published').exclude(id=post.id)[:3]

    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'popular_posts': popular_posts,
        'categories': categories,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published').order_by('-published_at')
    
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    popular_posts = Post.objects.filter(status='published').order_by('-views')[:5]
    categories = Category.objects.all()

    context = {
        'category': category,
        'posts': page_obj,
        'page_obj': page_obj,
        'popular_posts': popular_posts,
        'categories': categories,
    }
    return render(request, 'blog/category_detail.html', context)


def category_list(request):
    categories = Category.objects.all()
    popular_posts = Post.objects.filter(status='published').order_by('-views')[:5]
    
    context = {
        'categories': categories,
        'popular_posts': popular_posts,
    }
    return render(request, 'blog/category_list.html', context)

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')


def author_profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author, status='published').order_by('-published_at')
    
    context = {
        'author': author,
        'profile': author.profile if hasattr(author, 'profile') else None,
        'posts': posts,
    }
    return render(request, 'blog/author_profile.html', context)


def authors_list(request):
    # Get all users who have written at least one published post
    authors = User.objects.filter(blog_posts__status='published').distinct().order_by('username')
    
    context = {
        'authors': authors,
    }
    return render(request, 'blog/authors_list.html', context)


        