from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import  *
import smtplib
import secrets
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

      

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        print(username)
        try:
            user = UserRegistration.objects.get(username=username)
        except UserRegistration.DoesNotExist:
            return redirect('register')

        otp = secrets.randbelow(10000)
        print(otp)
        user.otp = otp
        user.otp_timestamp = timezone.now()  # Set the timestamp
        user.save()

        # Send OTP via email
        subject = 'OTP for login'
        message = f'OTP for login: {otp}'
        from_email = 'shalug.brainerhub@gmail.com'
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)
        print("going for verification")
        request.session['user_id'] = user.id
        return render(request, 'verify_otp.html', {'show_otp_input': True, 'username': username})

    return render(request, "login.html", {'show_otp_input': False})



@login_required
def verify_otp_view(request):
    if request.method == 'POST':
        print(request.POST) 
        entered_otp = request.POST['otp']
        username = request.POST['username']
        print(username,"==========================================")
        try:
            user_registration = UserRegistration.objects.get(username=username)
            print(user_registration)
            
            current_time = timezone.now()
            print(current_time)
            if (current_time - user_registration.otp_timestamp) <= timedelta(minutes=5):
                if user_registration.otp == int(entered_otp):
                    print("verified")
                    # Correct OTP, redirect to the appropriate view
                    return redirect('dashboard')  
                else:
                    # Invalid OTP
                    return redirect('login')
            else:
                # OTP has expired
                return redirect('login')
        except UserRegistration.DoesNotExist:
            # Handle case if user registration does not exist
            print("wrong")
            return redirect('login')
                
    return render(request, 'verify_otp.html')




def dashboard_view(request):
    user_id = request.session.get('user_id')
    user_registration = None  # Initialize user_registration

    if user_id:
        try:
            user_registration = UserRegistration.objects.get(id=user_id)
        except UserRegistration.DoesNotExist:
            pass  # Handle the case where the user doesn't exist

    # Rest of your code using user_registration...
    # posts = Post.objects.filter(author=user_registration).order_by('-pub_date')
    posts=Post.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = user_registration  # Assign the UserRegistration instance
            post.save()
            return redirect('dashboard')
    else:
        form = PostForm()

    context = {'posts': posts, 'form': form}
    return render(request, 'dashboard.html', context)





# def blog_view(request):
#     # return render(request, "blog.html")
#     posts = Post.objects.all()
#     return render(request, 'blog.html', {'posts': posts})



def blog_view(request):
    posts = Post.objects.all()
    return render(request, 'blog.html', {'posts': posts})

def post_detail_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post).order_by('created_at')
    if request.method == 'POST':
        content = request.POST.get('content')
        author = UserRegistration.objects.get(id=request.session.get('user_id'))
        Comment.objects.create(post=post, author=author, content=content)
        return redirect('post_detail', post_id=post.id)
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})



def register_view(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            new_user=UserRegistration(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email']
            )
            new_user.save()
            return redirect('login')
    else:
        form=RegistrationForm()

    return render(request, 'register.html', {'form':form})





def update_post_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    session_user_id = request.session.get('user_id')
    
    if session_user_id == post.author_id:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        else:
            form = PostForm(instance=post)
        return render(request, 'update_post.html', {'form': form})
    else:
        return HttpResponseForbidden("You don't have permission to edit this post.")





# def update_post_view(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     print(request.user,"==========",post.author)
#     if request.user == post.author:
#         if request.method == 'POST':
#             form = PostForm(request.POST, instance=post)
#             if form.is_valid():
#                 form.save()
#                 return redirect('dashboard')
#         else:
#             form = PostForm(instance=post)
#         return render(request, 'update_post.html', {'form': form})
#     else:
#         return HttpResponseForbidden("You don't have permission to edit this post.")



def delete_post_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    session_user_id = request.session.get('user_id')
    
    if session_user_id == post.author_id:
        if request.method == 'POST':
            post.delete()
            return redirect('dashboard')
        return render(request, 'delete_post.html', {'post': post})
    else:
        return HttpResponseForbidden("You don't have permission to delete this post.")

