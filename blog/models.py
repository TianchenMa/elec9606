from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser


GENDER = {
    0: u'Male',
    1: u'Female'
}


DEFAULT_PROFILE_PHOTO = '/static/blog/profile/default.jpg'


def user_directory_path(instance, filename):
    return '/static/blog/profile/user_{0}_{1}'.format(instance.user.id, filename)


def music_directory_path():
    return '/static/blog/music'


class User(AbstractUser):
    gender = models.IntegerField(default=0, choices=GENDER.items())
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL)
    profile_photo = models.ImageField(upload_to=user_directory_path, default=DEFAULT_PROFILE_PHOTO)

    class Meta:
        ordering = ['date_joined']


class Blog(models.Model):
    """docstring for Blog"""
    blog_title = models.CharField(max_length=100)
    blog_content = models.TextField(blank=True, null=True)
    blog_postdate = models.DateTimeField("Date posted")
    blog_private = models.BooleanField(default=False)
    liked_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_user"
    )
    blog_author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blog_author"
    )
    fwd_blog = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name="forward_blog",
        null=True
    )

    class Meta:
        ordering = ['-blog_postdate']

    def __str__(self):
        return "Title: " + self.blog_title + "; Author: " + User.objects.get(pk=self.blog_author_id).__str__()


class Music(models.Model):
    singer = models.CharField(max_length=50, null=True)
    song_name = models.CharField(max_length=100, null=True)
    music = models.FileField(upload_to=music_directory_path, null=True)
    music_blog = models.ForeignKey(Blog, null=True, on_delete=models.CASCADE)


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

