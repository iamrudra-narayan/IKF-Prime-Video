
# Create your views here.
from http.client import HTTPResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth import login as auth_login 
from django.contrib.auth import authenticate,logout
from django.contrib.auth.decorators import login_required
from .forms import PostForm



# Create your views here.
def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts':posts})

def show_videos(request, slug):
    post = Post.objects.get(slug=slug)
    posts = Post.objects.all()
    return render(request, 'show_video.html', {'post':post, 'posts':posts})

def register(request):
    if request.user.is_authenticated:
      return redirect("/")
    if request.method == "POST":
        try:
            email = request.POST['email']
            User.objects.get(username = request.POST['email'])
            messages.error(request, f"The Email {email} is already taken. Try a unique Email.")
            return redirect ('/register/')
        except User.DoesNotExist:
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = User(username=email, first_name=fname, last_name=lname)
            user.set_password(password)
            user.save()
            messages.success(request, f"Registration Successful. Welcome {fname} {lname}. Please Login to Proceed.")
            return redirect('/login/') 
    else:
        return render(request,'register.html')
       

def login(request):
    if request.user.is_authenticated:
      return redirect("/")
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request,user)
            messages.success(request, f"Welcome back {user.username}.")
            return redirect('/profile/')
        else:
            messages.error(request, f"Invalid Credentials. Login again.")
            return redirect('/login/')
    else:               
        return render(request, "login.html") 

@login_required(login_url='login')
def logout_user(request):
	logout(request)
	return redirect('/login/')

@login_required(login_url='login')
def profile(request):
    user_id = request.user.id
    user_details = User.objects.get(id=request.user.id)
    user_posts = Post.objects.filter(user = user_id)
    return render(request, "profile.html", {'user':user_details, 'user_posts':user_posts})       

@login_required(login_url='login')
def create(request):
    login_user= User.objects.get(id=request.user.id)
    if request.method == "POST":
        match_id = request.POST.get('match_id') 
        title = request.POST.get('title')
        venue = request.POST.get('venue')
        desc = request.POST.get('desc')
        video_file = request.FILES['video_file']

        post = Post(user=login_user,match_id=match_id, title=title, venue=venue, desc=desc, slug=title, video_file=video_file) 
        post.save()
        messages.success(request, f"Your post Uploaded Successfully.")
        return redirect('/profile/')
    
    return render(request, "create.html") 

@login_required(login_url='login')
def editpost(request, id):
    user = User.objects.get(id = request.user.id)
    user_posts = Post.objects.get(id=id)
    if request.method == "POST":
        match_id = request.POST.get('match_id') 
        title = request.POST.get('title')
        venue = request.POST.get('venue')
        desc = request.POST.get('desc')
        slug = request.POST.get('slug')
        
        user_posts.match_id = match_id
        user_posts.title = title
        user_posts.venue = venue
        user_posts.desc = desc
        user_posts.save()

        messages.success(request, f"Your Post Edited Successfully.")
        return redirect('/profile/')
    
    return render(request, "editpost.html", {'post':user_posts})   

@login_required(login_url='login')
def deletepost(request, id):
    user = User.objects.get(id = request.user.id)
    user_posts = Post.objects.filter(id=id)
    user_posts.delete()  
    messages.success(request, f"Your Post Deleted Successfully.")
    return redirect('/profile/')

@login_required(login_url='login')
def userprofile(request, id):
    user = User.objects.get(id=id)
    user_details = User.objects.get(id=request.user.id)
    user_posts = Post.objects.filter(user = user)
    for posts in user_posts:
        post = posts
    return render(request, "show-user-profiles.html", {'user':user, 'user_posts':user_posts,'post_count':post}) 

def search(request):

    results = []

    if request.method == "GET":

        query = request.GET.get('search')

        if query == '':

            query = 'None'
            return redirect("/")

        #results = FoodProduct.objects.filter(Q(prod_name__icontains=query) | Q(prod_desc__icontains=query))
        results = Post.objects.filter(title__icontains=query)
        profile_results = User.objects.filter(username__icontains=query)

    return render(request, 'search_results.html', {'query': query, 'results': results, 'profile_results': profile_results})   
