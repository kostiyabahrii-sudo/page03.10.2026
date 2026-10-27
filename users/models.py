from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
# Create your models here.


class Subscriber(models.Model):
    class Source(models.TextChoices):
        NONE = "none", "No answer"
        FRIEND = "friend", "From a friend"
        SOCIAL = "social", "From social media"
        AI = "ai", "From an AI assistant"
        OTHER = "other", "Other"

    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # "How did you hear about us?" — "none" until the person answers, so
    # people who close the survey stay on the list.
    heard_from = models.CharField(
        max_length=10, choices=Source.choices, default=Source.NONE
    )
    # Free text, only used when heard_from == "other".
    heard_from_other = models.CharField(max_length=200, blank=True)
