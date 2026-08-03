import random

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .models import Post
from .forms import PostForm, CommentForm

ANIMALS = [
    "Fox",
    "Wolf",
    "Owl",
    "Panda",
    "Lion",
    "Tiger",
    "Eagle",
    "Dolphin",
    "Butterfly",
    "Raven",
    "Falcon",
    "Bear",
    "Koala",
    "Deer",
    "Rabbit",
]

def home(request):
    query = request.GET.get("q")

    posts = Post.objects.all().order_by("-created_at")

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__icontains=query) |
            Q(category__icontains=query)
        )

    return render(request, "home.html", {
        "posts": posts,
        "query": query,
    })



def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = f"Anonymous {random.choice(ANIMALS)}"
            post.save()
            return redirect("home")
    else:
        form = PostForm()

    return render(request, "create_post.html", {"form": form})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = f"Anonymous {random.choice(ANIMALS)}"
            comment.save()

            return redirect("post_detail", post_id=post.id)

    else:
        form = CommentForm()

    return render(request, "post_detail.html", {
        "post": post,
        "form": form,
        "comments": post.comments.all().order_by("-created_at"),
    })


def upvote_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.upvotes += 1
    post.save()
    return redirect("post_detail", post_id=post.id)


def categories(request):
    categories = [
        {
            "slug": "storytelling",
            "icon": "📖",
            "name": "Storytelling",
            "description": "Share unforgettable memories, adventures and life experiences."
        },
        {
            "slug": "mental_health",
            "icon": "🧠",
            "name": "Mental Health",
            "description": "A safe place to express how you're feeling."
        },
        {
            "slug": "relationships",
            "icon": "❤️",
            "name": "Relationships",
            "description": "Love, friendships and everything in between."
        },
        {
            "slug": "school",
            "icon": "🎓",
            "name": "School",
            "description": "School, university and student life."
        },
        {
            "slug": "career",
            "icon": "💼",
            "name": "Career",
            "description": "Jobs, internships and professional growth."
        },
        {
            "slug": "family",
            "icon": "👨‍👩‍👧",
            "name": "Family",
            "description": "Stories about parents, siblings and relatives."
        },
        {
            "slug": "personal_growth",
            "icon": "🌱",
            "name": "Personal Growth",
            "description": "Learning, healing and becoming your best self."
        },
        {
            "slug": "travel",
            "icon": "🌍",
            "name": "Travel",
            "description": "Trips, adventures and places you've explored."
        },
        {
            "slug": "success",
            "icon": "🎉",
            "name": "Success",
            "description": "Celebrate achievements and milestones."
        },
        {
            "slug": "loss",
            "icon": "💔",
            "name": "Loss",
            "description": "Share difficult moments and remember loved ones."
        },
        {
            "slug": "hobbies",
            "icon": "🎮",
            "name": "Hobbies",
            "description": "Gaming, music, sports, art and more."
        },
    ]

    return render(request, "categories.html", {
        "categories": categories
    })

def category_posts(request, category):
    posts = Post.objects.filter(category=category).order_by("-created_at")

    category_names = {
        "storytelling": "📖 Storytelling",
        "personal_growth": "🌱 Personal Growth",
        "relationships": "❤️ Relationships",
        "school": "🎓 School",
        "career": "💼 Career",
        "family": "👨‍👩‍👧 Family",
        "mental_health": "🧠 Mental Health",
        "travel": "🌍 Travel",
        "success": "🎉 Success",
        "loss": "💔 Loss",
        "hobbies": "🎮 Hobbies",
    }

    return render(request, "category_posts.html", {
        "posts": posts,
        "category": category_names.get(category, category),
    })