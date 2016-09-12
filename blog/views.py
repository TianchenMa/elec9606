from django.shortcuts import render, get_object_or_404, render_to_response, Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, ListView, CreateView, DeleteView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.core.exceptions import PermissionDenied

from .models import Blog, Comment, User
from .forms import CommentForm, BlogForm, ForwardForm, LoginForm
from django.views.generic import ListView


# Create your views here.

def index(request):
    context = {
        'user_list': User.objects.all(),
    }
    if request.user.is_active:
        blog = Blog.objects.none()
        user = User.objects.get(pk=request.user.id)
        context['follow_list'] = user.follow.all()
        for user in user.follow.all():
            blog = blog | Blog.objects.filter(blog_author=user, blog_private=False)
        context['blog_list'] = blog

    return render(request, 'blog/index.html', context)


class BaseMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        if self.request.user:
            user = User.objects.get(pk=self.request.user.id)
            context['log_user'] = user
        else:
            context['log_user'] = None

        return context


class IndexView(ListView):
    template_name = 'blog/index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        blog = Blog.objects.none()

        if self.request.user.is_active:
            user = User.objects.get(pk=self.request.user.id)
            context['log_user'] = user
            context['follow_list'] = user.follow.all()

            for user in user.follow.all():
                blog = blog | Blog.objects.filter(blog_author=user, blog_private=False)

        context['blog_list'] = blog
        return context

    def get_queryset(self):
        return User.objects.all()


class UserControl(View):
    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        if slug == 'register':
            return render(request, 'blog/register.html')

        raise PermissionDenied

    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')

        if slug == 'login':
            return self.login(request)
        elif slug == 'logout':
            return self.logout(request)
        elif slug == 'register':
            return self.register(request)
        elif slug == 'registerpage':
            return self.registerpage(request)
        elif slug == 'follow':
            return

        raise PermissionDenied

    def login(self, request):
        name = self.request.POST['name']
        pwd = self.request.POST['password']
        user = authenticate(username=name, password=pwd)

        if user is not None:
            self.request.session.set_expiry(0)
            login(self.request, user)
            log_message = 'Login successfully.'
        else:
            log_message = 'Fail to login.'

        return HttpResponseRedirect(reverse('blog:index'))

    def logout(self, request):
        logout(request)
        user_list = User.objects.order_by('date_joined')
        context = {
            'user_list': user_list,
        }

        return render(self.request, 'blog/index.html', context)

    def registerpage(self, request):
        return render(request, 'blog/register.html')

    def register(self, request):
        user_name = self.request.POST['username']
        firstname = self.request.POST['firstname']
        lastname = self.request.POST['lastname']
        pwd = self.request.POST['password']
        e_mail = self.request.POST['email']
        user = User.objects.create(username=user_name, first_name=firstname, last_name=lastname, email=e_mail)
        user.set_password(pwd)
        try:
            user.save()
            user = authenticate(username=user_name, password=pwd)
            login(self.request, user)
        except Exception:
            pass
        else:
            return HttpResponseRedirect(reverse('blog:index'))


def personalinformation(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.user.is_active:
        context = {
            'User': user,
        }

    return render(request, 'blog/personalinformation.html', context)


def userlogin(request):
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
            user = authenticate(username=user_name, password=pwd)
            login(request, user)
        except Exception:
            pass
        else:
            return HttpResponseRedirect(reverse('blog:index'))

    else:
        return HttpResponseRedirect(reverse('blog:register'))


# def resetpassword(request, u_id):


def followuser(request, u_id):
    luser = User.objects.get(pk=request.user.id)

    if request.method == 'POST':
        if request.user.is_active:
            follow = User.objects.get(pk=u_id)

            if luser.follow.filter(pk=u_id).exists():
                luser.follow.remove(follow)
            else:
                luser.follow.add(follow)

    user = User.objects.get(pk=u_id)
    if u_id == str(request.user.id):
        self = True
    else:
        self = False
    context = {
        'User': user,
        'Blog_list': Blog.objects.filter(blog_author_id=u_id),
        'self': self,
        'follow': user in request.user.follow.all()
    }
    return render(request, 'blog/personalhomepage.html', context)


def personalhomepage(request, home_id):
    user = get_object_or_404(User, pk=home_id)
    log_user = User.objects.get(pk=request.user.id)
    blog_list = Blog.objects.filter(blog_author=user)

    if home_id == str(log_user.id):
        self = True
    else:
        self = False

    context = {
        'User': user,
        'Blog_list': blog_list,
        'self': self,
        'follow': user in log_user.follow.all()
    }
    return render(request, 'blog/personalhomepage.html', context)


def writeblogpage(request):
    return render(request, 'blog/writeblog.html')


def writeblog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            private = form.cleaned_data['private']
            post_date = timezone.now()
            author = request.user.id
            blog = Blog.objects.create(blog_title=title, blog_content=content, blog_postdate=post_date,
                                       blog_author_id=author, blog_private=private)
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
    blog = get_object_or_404(Blog, pk=b_id)
    if not blog.blog_private or blog.blog_author_id == request.user.id:
        user = request.user

        context = {
            'blog': blog,
            'self': blog.blog_author_id == user.id,
            'comment_list': blog.comment_set.all(),
            'liked': blog.liked_user.filter(pk=user.id).exists(),
        }
        return render(request, 'blog/viewblog.html', context)

    raise Http404


def forwardblog(request, b_id):
    user = User.objects.get(pk=request.user.id)
    blog = Blog.objects.get(pk=b_id)

    if request.method == 'POST':
        form = ForwardForm(request.POST)

        if form.is_valid():
            fwdcontent = form.cleaned_data['fwdcontent']
            fwdprivate = form.cleaned_data['fwdprivate']
            fwddate = timezone.now()
            fwdblog = Blog(
                blog_author=user,
                blog_title=fwdcontent,
                blog_postdate=fwddate,
                blog_private=fwdprivate,
                fwd_blog=blog
            )
            fwdblog.save()

    context = {
        'blog': Blog.objects.get(pk=b_id),
        'self': blog.blog_author_id == user.id,
        'comment_list': blog.comment_set.all(),
        'liked': blog.liked_user.filter(pk=user.id).exists(),
    }

    return render(request, 'blog/viewblog.html', context)


def likeblog(request, b_id):
    blog = Blog.objects.get(pk=b_id)
    user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
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


def searchblog(request):
    blog = Blog.objects.none()
    user = User.objects.none()
    if request.method == 'POST':
        keyword = request.POST['keyword']
        blog = Blog.objects.filter(blog_title__contains=keyword, blog_private=False)
        user = User.objects.filter(username__contains=keyword)

    context = {
            'result_blog': blog,
            'result_user': user,
        }

    return render(request, 'blog/searchresult.html', context)


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
    blog = Blog.objects.get(pk=b_id)

    if request.method == 'POST':
        Comment.objects.get(pk=c_id).delete()

    context = {
        'author_id': blog.blog_author_id,
        'blog': blog,
        'self': blog.blog_author_id == user.id,
        'comment_list': blog.comment_set.all()
    }

    return render(request, 'blog/viewblog.html', context)
