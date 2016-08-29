from django.shortcuts import render, get_object_or_404, render_to_response, Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User

from .models import Blog, Comment, User
from .forms import CommentForm


# Create your views here.
def index(request):
    user_list = User.objects.order_by('date_joined')
    context = {
        'user_list': user_list,
    }
    return render(request, 'blog/index.html', context)


def personalinformation(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {
        'User': user,
    }
    return render(request, 'blog/personalinformation.html', context)


# def loginpage(request):
#     return render(request, 'blog/login.html')


def userlogin(request):
    log_message = None
    if request.method == 'POST':
        name = request.POST['name']
        pwd = request.POST['password']
        user = authenticate(username=name, password=pwd)
        if user is not None:
            request.session.set_expiry(0)
            login(request, user)
            log_message = 'Login successfully.'
        else:
            log_message = 'Fail to login.'
    else:
        log_message = 'Please login.'
    context = {
        'log_message': log_message
    }
    return HttpResponseRedirect(reverse('blog:index'), context)


def logoutpage(request):
    logout(request)
    user_list = User.objects.order_by('date_joined')
    context = {
        'user_list': user_list,
    }
    return render(request, 'blog/index.html', context)


def register(request):
    return render(request, 'blog/register.html')


def registerresult(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        pwd = request.POST['password']
        e_mail = request.POST['email']
        user = User.objects.create(username=user_name, first_name=firstname, last_name=lastname, email=e_mail)
        user.set_password(pwd)
        try:
            user.save()
            # request.session['user_id'] = user.id
            user = authenticate(username=user_name, password=pwd)
            login(request, user)
        except Exception:
            pass
        else:
            return HttpResponseRedirect(reverse('blog:index'))

    else:
        return HttpResponseRedirect(reverse('blog:register'))


def personalhomepage(request, home_id):
    user = get_object_or_404(User, pk=home_id)
    blog_list = Blog.objects.filter(blog_author=home_id)
    if home_id == str(request.user.id):
        self = True
    else:
        self = False
    context = {
        'User': user,
        'Blog_list': blog_list,
        'self': self,
    }
    return render(request, 'blog/personalhomepage.html', context)


def writeblogpage(request):
    # user_id = request.user.id
    # context = {
    #     'user_id': user_id,
    # }
    # # return render(request, 'blog/writeblog.html', context)
    return render(request, 'blog/writeblog.html')


def writeblog(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        prvt = request.POST['private']
        pdate = timezone.now()
        author = request.user.id
        blog = Blog.objects.create(blog_title=title, blog_content=content, blog_postdate=pdate,
                                   blog_author_id=author, blog_private=prvt)
        try:
            blog.save()
        except Exception:
            return render(reverse('blog:writeblogpage'))
        else:
            context = {
                'blog': blog,
            }
            return render(request, 'blog/viewblog.html', context)  # delete blog

    else:
        raise Http404



def deleteblog(request, b_id):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, pk=b_id)
        if blog.blog_author_id == request.user.id:
            user = get_object_or_404(User, pk=blog.blog_author_id)
            blog_list = Blog.objects.filter(blog_author=blog.blog_author_id)
            if blog.blog_author_id == request.user.id:
                self = True
            else:
                self = False

            context = {
                'User': user,
                'Blog_list': blog_list,
                'self': self,
            }
            Blog.objects.get(pk=b_id).delete()

            return render(request, 'blog/personalhomepage.html', context)

    raise Http404


def viewblog(request, b_id):
    blog = Blog.objects.get(id=b_id)
    user = request.user
    if not blog.blog_private or user == blog.blog_author_id:
        context = {
            'blog': blog,
            'self': blog.blog_author_id == user.id,
            'comment_list': blog.comment_set.all(),
            'liked': blog.liked_user.filter(pk=user.id).exists(),
        }
        return render(request, 'blog/viewblog.html', context)

    raise Http404


def likeblog(request, b_id):
    user = User.objects.get(pk=request.user.id)
    blog = Blog.objects.get(pk=b_id)
    if user.id != blog.blog_author_id:
        if blog.liked_user.filter(pk=user.id).exists():
            blog.liked_user.remove(user)
        else:
            blog.liked_user.add(user)

    context = {
        'blog': blog,
        'self': blog.blog_author_id == user.id,
        'comment_list': blog.comment_set.all(),
        'liked': blog.liked_user.filter(pk=user.id).exists(),
    }
    return render(request, 'blog/viewblog.html', context)


def commentblog(request, b_id):
    user = request.user
    blog = Blog.objects.get(pk=b_id)
    context = {
        'author_id': blog.blog_author_id,
        'blog': blog,
        'self': blog.blog_author_id == user.id,
    }
    if user.id:
        if request.method == 'POST':
            form = CommentForm(request.POST)

            if form.is_valid():
                author_id = form.cleaned_data['author_id']
                content = form.cleaned_data['content']
                date = timezone.now()
                comment = Comment(comment_author_id=author_id, comment_blog_id=b_id, comment_content=content,
                                  comment_date=date)
                try:
                    comment.save()
                except Exception:
                    raise Http404
                else:
                    context['comment_list'] = blog.comment_set.all()
                    return render(request, 'blog/viewblog.html', context)

            else:
                raise Http404
    else:
        context['comment_error'] = 'Login first.'
        context['comment_list'] = blog.comment_set.all()
        return render(request, 'blog/viewblog.html', context)


def deletecomment(request, b_id, c_id):
    user = request.user
    if request.method == 'POST':
        Comment.objects.get(pk=c_id).delete()
        blog = Blog.objects.get(pk=b_id)
        context = {
            'author_id': blog.blog_author_id,
            'blog': blog,
            'self': blog.blog_author_id == user.id,
            'comment_list': blog.comment_set.all()
        }

    return render(request, 'blog/viewblog.html', context)
