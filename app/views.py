from django.shortcuts import render, redirect, get_object_or_404
from .form import PostForm, ProfileForm
from .models import Addposts, Profile, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q


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
            return render(request, 'combined_auth.html', {'register_error': 'Passwords do not match'})

        if User.objects.filter(username=uname).exists():
            return render(request, 'combined_auth.html', {'register_error': 'Username already taken'})

        user = User.objects.create_user(username=uname, email=email, password=pw1)
        user.save()

        return render(request, 'combined_auth.html', {'login_error': 'Account created successfully. Please login.'})

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


# ---------- PROFILE ----------
@login_required(login_url='auth_page')
def profile_view(request, username):
    user_profile = get_object_or_404(User, username=username)
    profile = Profile.objects.filter(user=user_profile).first()
    user_posts = Addposts.objects.filter(user=user_profile).order_by('-created_at')

    for post in user_posts:
        post.like_count = post.liked_by.count()

    return render(request, "profile.html", {
        "user_profile": user_profile,
        "profile": profile,
        "user_posts": user_posts,
    })


# ---------- EDIT PROFILE ----------
@login_required(login_url='auth_page')
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)

    form = ProfileForm(instance=profile)
    return render(request, 'editprofile.html', {'form': form})


# ---------- ADD POSTS ----------
@login_required(login_url='auth_page')
def addposts(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('view_posts')
    else:
        form = PostForm()

    return render(request, 'addposts.html', {'form': form})


# ---------- VIEW POSTS ----------
@login_required(login_url='auth_page')
def view_posts(request):
    posts = Addposts.objects.all().order_by('-created_at')

    # Handle adding comments directly from this page
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        comment_text = request.POST.get("comment_text")
        post = get_object_or_404(Addposts, id=post_id)

        if comment_text.strip():
            Comment.objects.create(post=post, user=request.user, text=comment_text)

        return redirect('view_posts')

    return render(request, "viewposts.html", {"posts": posts})


# ---------- ADD COMMENT (OPTIONAL EXTRA ENDPOINT) ----------
@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Addposts, id=post_id)
        text = request.POST.get("comment_text")

        if text.strip():
            Comment.objects.create(post=post, user=request.user, text=text)

    return redirect("view_posts")


# ---------- DELETE COMMENT ----------
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Only allow comment owner to delete
    if comment.user == request.user:
        comment.delete()

    return redirect('view_posts')


# ---------- LIKE POST ----------
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Addposts, id=post_id)

    if request.user in post.liked_by.all():
        post.liked_by.remove(request.user)
    else:
        post.liked_by.add(request.user)

    return redirect('view_posts')


# ---------- DELETE POST ----------
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Addposts, id=post_id)

    if request.user == post.user:
        post.delete()
        messages.success(request, "Post deleted successfully.")
    else:
        messages.error(request, "You are not allowed to delete this post.")

    return redirect('view_posts')


# ---------- SEARCH ----------
@login_required(login_url='auth_page')
def search_view(request):
    query = request.GET.get("q")

    user_results = []
    if query:
        users = User.objects.filter(username__icontains=query)

        for user in users:
            posts = Addposts.objects.filter(user=user).order_by('-created_at')
            user_results.append({
                "user": user,
                "profile": Profile.objects.filter(user=user).first(),
                "posts": posts
            })

    return render(request, "search.html", {
        "query": query,
        "user_results": user_results,
    })


# ---------- ABOUT ----------
@login_required(login_url='auth_page')
def about(request):
    return render(request, 'about.html')
