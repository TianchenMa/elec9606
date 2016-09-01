from django.conf.urls import url

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^index/', views.index, name='index'),

    # url(r'^login/', views.loginpage, name='login'),

    url(r'^login', views.userlogin, name='login'),

    url(r'^logout/', views.logoutpage, name='logoutpage'),

    url(r'^register/', views.register, name='register'),

    url(r'^registerresult', views.registerresult, name='registerresult'),

    url(r'^(?P<home_id>[0-9]+)/homepage/', views.personalhomepage, name='personalhomepage'),

    url(r'^(?P<u_id>[0-9]+)/follow/', views.followuser, name='followuser'),

    url(r'^information/', views.personalinformation, name='personalinformation'),

    url(r'^writeblog/', views.writeblogpage, name='writeblogpage'),

    url(r'^writeblog', views.writeblog, name='writeblog'),

    url(r'^blog/(?P<b_id>[0-9]+)/viewblog/', views.viewblog, name='viewblog'),

    url(r'^blog/(?P<b_id>[0-9]+)/forward/', views.forwardblog, name='forwardblog'),

    url(r'^blog/(?P<b_id>[0-9]+)/like', views.likeblog, name='likeblog'),

    url(r'^blog/(?P<b_id>[0-9]+)/deleteblog', views.deleteblog, name='deleteblog'),

    url(r'^blog/(?P<b_id>[0-9]+)/commentblog', views.commentblog, name='commentblog'),

    url(r'^blog/(?P<b_id>[0-9]+)/(?P<c_id>[0-9]+)/deletecomment', views.deletecomment, name='deletecomment'),
]
