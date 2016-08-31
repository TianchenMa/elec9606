from django.contrib import admin


from .models import User, Blog, Comment

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    fields = [
        'blog_title',
        'blog_postdate',
        'blog_content',
        'blog_author',
    ]


class CommentAdmin(admin.ModelAdmin):
    fields = [
        'comment_content',
        'comment_date',
        'comment_author_id',
        'comment_blog_id',
    ]


admin.site.register(User)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)