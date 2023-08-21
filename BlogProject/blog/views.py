from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import PostForm

# Create your views here.


# list all the post
def post_list(request):
    posts=Post.objects.all()
    return render(request, "post_list.html",{"posts":posts})


def post_detail(request, pk):
    post=get_object_or_404(Post, pk=pk)
    return render(request,"post_detail.html", {'post':post} )


def category_view(request, slug):
    category=get_object_or_404(Category, slug=slug)
    posts=Post.objects.filter(categories=category)
    return render(request, "category_view.html", {'category':category, 'posts':posts})


def create_post(request):
    if request.method=='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            post=form.save()
            return redirect('post_detail', pk=post.pk)
        

    else:
        form=PostForm()
    return render(request, 'post_form.html', {'form':form})
        