from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout
urlpatterns = [
    url(r'^index/$',views.index,name='art_index'),
    url(r'^article/(?P<article_id>[0-9]+)$', views.article_page,name='article_page'),
    url(r'^edit/(?P<article_id>[0-9]+)$',views.edit_page,name='edit_page'),
    url(r'^edit/action/$',views.edit_action,name='edit_action'),
    url(r'^edit_email/$',views.requires_login(views.edit_email),name='edit_email'),
    url(r'^send_email/$',views.send_email,name='send_email'),
    url(r'^version/$',views.requires_login(views.version),name='version'),
    url(r'^edit_version/(?P<version_id>[0-9]+)$',views.requires_login(views.edit_version),name='edit_version'),
    url(r'^version_action/$',views.version_action,name='version_action'),
    url(r'^tenant_list/$',views.tenant_list,name='tenant_list'),
	url(r'^login_action/$',views.login_action,name='login_action'),    
	url(r'^regist/$',views.regist,name='regist'),
	url(r'^change/$',views.change_pass,name='change'),
	url(r'^login/$',views.login,name='login'),
	url(r'^logout/$',views.loginout,name='logout'),
	url(r'^tenant_list/(?P<page>[0-9]+)/$',views.tenant_list,name='tenant_list'),
	url(r'^tenant_search/$',views.tenant_search,name='tenant_search'),
] 
urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)