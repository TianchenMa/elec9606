from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views
from .views import IndexView, UserControl

app_name = 'blog'
urlpatterns = [
    # url(r'^index/', views.index, name='index'),

    url(r'index', IndexView.as_view(), name='index'),

    url(r'^user/(?P<slug>\w+)$', UserControl.as_view(), name='usercontrol'),

    url(r'^(?P<u_id>[0-9]+)/(?P<slug>\w+)$', views.UserView.as_view(), name='user'),

    url(r'^(?P<u_id>[0-9]+)/homepage/', views.personalhomepage, name='personalhomepage'),

    url(r'^(?P<u_id>[0-9]+)/follow/', views.followuser, name='followuser'),

    url(r'^information/', views.personalinformation, name='personalinformation'),

    url(r'^search/', views.searchblog, name='searchblog'),

    url(r'^writeblog/', views.writeblogpage, name='writeblogpage'),

    url(r'^writeblog', views.writeblog, name='writeblog'),

    url(r'^blog/(?P<b_id>[0-9]+)/viewblog/', views.viewblog, name='viewblog'),

    url(r'^blog/(?P<b_id>[0-9]+)/forward/', views.forwardblog, name='forwardblog'),

    url(r'^blog/(?P<b_id>[0-9]+)/like', views.likeblog, name='likeblog'),

    url(r'^blog/(?P<b_id>[0-9]+)/deleteblog', views.deleteblog, name='deleteblog'),

    url(r'^blog/(?P<b_id>[0-9]+)/commentblog', views.commentblog, name='commentblog'),

    url(r'^blog/(?P<b_id>[0-9]+)/(?P<c_id>[0-9]+)/deletecomment', views.deletecomment, name='deletecomment'),
]
              # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
