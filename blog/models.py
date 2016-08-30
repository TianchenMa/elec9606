from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser


class User(AbstractUser):
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL)


class Blog(models.Model):
    """docstring for Blog"""
    blog_title = models.CharField(max_length=100)
    blog_content = models.TextField(blank=True, null=True);
    blog_postdate = models.DateTimeField("Date posted")
    blog_author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blog_author"
    )
    blog_private = models.BooleanField(default=False)
    liked_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_user")

    class Meta:
        ordering = ['-blog_postdate']

    def __str__(self):
        return "Title: " + self.blog_title + "; Author: " + User.objects.get(pk=self.blog_author_id).__str__()


class Comment(models.Model):
    """docstring for Comment"""
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment_content = models.TextField(blank=True, null=False)
    comment_date = models.DateTimeField("Date commented.", auto_now_add=True)

    class Meta:
        ordering = ['-comment_date']

    def __str__(self):
        return "User: " + User.objects.get(
            pk=self.comment_author_id).user_name + "; " + "Comment on blog: " + Blog.objects.get(
            pk=self.comment_blog_id).blog_title + "."

