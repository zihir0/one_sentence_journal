from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, LikePosts, Comment
from .forms import PostForm, UserRegistrationForm, CommentForm
from rest_framework import viewsets
from .serializer import PostSerializer

def blog_list(request):
    blog_list = Post.objects.all().order_by('-created_at')

    # Add "liked" status for each post
    for post in blog_list:
        post.is_liked = (
            request.user.is_authenticated 
            and LikePosts.objects.filter(post=post, user=request.user).exists()
        )

    return render(request, 'blog/blog_list.html', {'blog_list': blog_list})

def blog_detail(request, id):
    each_post = get_object_or_404(Post, id=id)
    comments = each_post.comment_set.all().order_by('-created_at')
    
    # Handle comment submission
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = each_post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('blog_detail', id=id)
    else:
        comment_form = CommentForm()

    context = {
        'blog_detail': each_post,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, "blog/blog_detail.html", context)

@login_required
def blog_delete(request, id):
    each_post = get_object_or_404(Post, id=id)
    
    # Ensure only the author can delete the post
    if request.user != each_post.author:
        messages.error(request, "You are not authorized to delete this post.")
        return redirect('blog_list')
    
    each_post.delete()
    messages.success(request, "Post deleted successfully.")
    return HttpResponseRedirect('/posts/')

@login_required
def blog_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user  # Set the current user as the author
        post.save()
        messages.success(request, 'Post created successfully!')
        return HttpResponseRedirect('/posts/')
    
    context = {
        'form': form,
        'form_type': 'Create'
    }
    return render(request, "blog/blog_create.html", context)

@login_required
def blog_update(request, id):
    each_post = get_object_or_404(Post, id=id)
    
    # Ensure only the author can update the post
    if request.user != each_post.author:
        messages.error(request, "You are not authorized to update this post.")
        return redirect('blog_list')
    
    form = PostForm(request.POST or None, request.FILES or None, instance=each_post)
    if form.is_valid():
        form.save()
        messages.success(request, 'Post updated successfully!')
        return HttpResponseRedirect('/posts/')
    
    context = {
        'form': form,
        'form_type': 'Update'
    }
    return render(request, "blog/blog_create.html", context)

class PostSerializerViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = LikePosts.objects.get_or_create(post=post, user=request.user)

    if not created:
        # Unlike the post if the user already liked it
        like.delete()
        liked = False
    else:
        # Like the post
        liked = True

    # Return a JSON response if using AJAX (optional)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'likes_count': post.likeposts_set.count()})

    return redirect('blog_list')

# Authentication Views
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('blog_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('blog_list')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'blog/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')