from django.contrib.auth.models import User

from django.db import models

# Mood choices
MOOD_CHOICES = [
    ("hopeful", "😊 Hopeful"),
    ("struggling", "😔 Struggling"),
    ("grateful", "❤️ Grateful"),
    ("celebrating", "🎉 Celebrating"),
    ("reflecting", "🤔 Reflecting"),
    ("frustrated", "😡 Frustrated"),
    ("motivated", "💪 Motivated"),
    ("healing", "🌱 Healing"),
]

# Category choices
CATEGORY_CHOICES = [
    ("storytelling", "📖 Storytelling"),
    ("personal_growth", "🌱 Personal Growth"),
    ("relationships", "❤️ Relationships"),
    ("school", "🎓 School"),
    ("career", "💼 Career"),
    ("family", "👨‍👩‍👧 Family"),
    ("mental_health", "🧠 Mental Health"),
    ("travel", "🌍 Travel"),
    ("success", "🎉 Success"),
    ("loss", "💔 Loss"),
    ("hobbies", "🎮 Hobbies"),
]

class Post(models.Model):
    author = models.CharField(max_length=50, default="Anonymous")
    title = models.CharField(max_length=200)

    # 👇 Add this inside the Post model
    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default="storytelling"
    )

    mood = models.CharField(
        max_length=20,
        choices=MOOD_CHOICES,
        default="reflecting"
    )

    content = models.TextField()
    upvotes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    author = models.CharField(max_length=50)

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.content[:30]}"    