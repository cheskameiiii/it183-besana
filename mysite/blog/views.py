from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm

def post_list(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new post
            return redirect('post_list')  # Redirect to the post list after saving
    else:
        form = PostForm()  # Create an empty form

    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts, 'form': form})
# View to display a single post
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        if 'update' in request.POST:
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('post_detail', post_id=post.id)
        elif 'delete' in request.POST:
            post.delete()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)  # Pre-fill the form with current post data

    return render(request, 'post_detail.html', {'post': post, 'form': form})
