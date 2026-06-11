from django.contrib.auth.models import User
from django.db import models


# =========================
# 👤 USER PROFILE
# =========================
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.TextField(blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    role = models.CharField(max_length=20, default="user")

    def __str__(self):
        return self.user.username


# =========================
# 💻 CODE HISTORY (RUN CODE)
class CodeHistory(models.Model):
    code = models.TextField()
    output = models.TextField()
    language = models.CharField(max_length=20, default="python")  # ← ye hona chahiye
    created_at = models.DateTimeField(auto_now_add=True)

# =========================
# 💬 AI CHAT HISTORY
# =========================
class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - Chat"


# =========================
# 🧠 PRACTICE ATTEMPTS (LEETCODE)
# =========================
class Practice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    question_title = models.CharField(max_length=255)
    question = models.TextField()
    answer = models.TextField()
    result = models.CharField(max_length=50, default="pending")
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.question_title}"


# =========================
# 📊 PERFORMANCE TRACKING
# =========================
from django.contrib.auth.models import User
from django.db import models


class Performance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    solved = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0)
    score = models.IntegerField(default=0)

    streak = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


# =========================
# 🧪 AI GENERATED TEST
# =========================
class AI_Test(models.Model):
    title = models.CharField(max_length=255)
    time_limit = models.IntegerField(default=60)
    questions = models.JSONField()  # store full LeetCode test
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title