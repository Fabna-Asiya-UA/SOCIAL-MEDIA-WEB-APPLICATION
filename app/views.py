from django.shortcuts import render, redirect , get_object_or_404
from .form import PostForm, ProfileForm
from .models import Addposts, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
# ---------- AUTH PAGE ----------
def auth_page(request):
    return render(request, 'combined_auth.html')


# ---------- REGISTER ----------
def register_user(request):
    if request.method == "POST":
        uname = request.POST.get('user_name')
        email = request.POST.get('email')
        pw1 = request.POST.get('password1')
        pw2 = request.POST.get('password2')

        if pw1 != pw2:
            return render(request, 'combined_auth.html', {
                'register_error': 'Passwords do not match'
            })

        if User.objects.filter(username=uname).exists():
            return render(request, 'combined_auth.html', {
                'register_error': 'Username already taken'
            })

        user = User.objects.create_user(username=uname, email=email, password=pw1)
        user.save()  # Profile auto-created by signal

        return render(request, 'combined_auth.html', {
            'login_error': 'Account created successfully. Please login.'
        })

    return redirect('auth_page')


# ---------- LOGIN ----------
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("user_name")   
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Wrong username or password")

    return render(request, "combined_auth.html")


# ---------- LOGOUT ----------
def logout_view(request):
    logout(request)
    return redirect('auth_page')


# ---------- HOME ----------
@login_required(login_url='auth_page')
def home(request):
    return render(request, 'home.html')


# ---------- PROFILE VIEW ----------
@login_required(login_url='auth_page')
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile})


# ---------- EDIT PROFILE ----------
@login_required(login_url='auth_page')
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    form = ProfileForm(instance=profile)
    return render(request, 'editprofile.html', {'form': form})


# ---------- ADD POSTS ----------
@login_required(login_url='auth_page')
def addposts(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user   # FIXED HERE
            post.save()
            return redirect('viewposts')
    else:
        form = PostForm()

    return render(request, 'addposts.html', {'form': form})


# ---------- VIEW POSTS ----------
@login_required(login_url='auth_page')
def viewposts(request):
    posts = Addposts.objects.all().order_by('-created_at')
    return render(request, 'viewposts.html', {'posts': posts})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Addposts, id=post_id)

    if post.user == request.user:
        post.delete()

    return redirect('viewposts')


# ---------- SEARCH ----------
@login_required(login_url='auth_page')
def search_view(request):
    query = request.GET.get('q')

    if query is None or query.strip() == "":
        return render(request, 'search.html', {'results': []})

    results = Addposts.objects.filter(caption__icontains=query)

    return render(request, 'search.html', {
        'results': results,
        'query': query
    })
@login_required(login_url='auth_page')
def about(request):
    return render(request, 'about.html')

