from django.contrib import admin


from .models import User, Blog, Comment


# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    fields = [
        'blog_title',
        'blog_postdate',
        'blog_content',
        'from_user',
    ]

    list_display = ('blog_title', 'from_user', 'blog_postdate')


class CommentAdmin(admin.ModelAdmin):
    fields = [
        'comment_content',
        'comment_date',
        'from_user_id',
        'comment_blog_id',
    ]

    list_display = ('comment_blog', 'from_user_id', 'comment_content', 'comment_date')


admin.site.register(User)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)