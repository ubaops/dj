from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from . import models
import logging
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import auth
from django import forms
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from django.db.models import Q

logger=logging.getLogger('ubablog2.views')


class UserForm(forms.Form):
	username=forms.CharField(label='用户名')
	password=forms.CharField(label='密 码',widget=forms.PasswordInput())


class ChangeForm(forms.Form):
	username=forms.CharField(label='用户名')
	old_password=forms.CharField(label='原密码',widget=forms.PasswordInput())
	new_password=forms.CharField(label='新密码',widget=forms.PasswordInput())
def global_setting(request):
	return {'SITE_NAME':settings.SITE_NAME,
			'SITE_DESC':settings.SITE_DESC,
			}


def index(request):
	#return HttpResponse('this is uba first page' )
	is_login=request.session.get('username')
	if is_login:
		articles=models.Article.objects.all()
		return render(request,'ubablog2/index.html',{'arts':articles,'username':is_login})
	else:
		#print('##############################')
		#print('you are not loging')
		#print('#############################')
		return HttpResponseRedirect("/blog2/login")
		#uf = UserForm() 
		#return render(request,"registration/login.html",{'uf': uf})
def article_page(request,article_id):
	article=models.Article.objects.get(pk=article_id)
	return render(request,'ubablog2/ArtPage.html',{'article':article})


def edit_page(request,article_id):
	if article_id=='0':
		return render(request,'ubablog2/edit_page.html')
	article=models.Article.objects.get(pk=article_id)
	return render(request,'ubablog2/edit_page.html',{'article':article})

def edit_action(request):
	title=request.POST.get('title')
	content=request.POST.get('content')
	article_id=request.POST.get('article_id')
	if article_id=='0':
		models.Article.objects.create(title=title,content=content)
		articles=models.Article.objects.all()
		return render(request,'ubablog2/index.html',{'arts':articles})
	else:
		article=models.Article.objects.get(pk=article_id)
		article.title=title
		article.content=content
		article.save()
		return render(request,'ubablog2/ArtPage.html',{'article':article})

def edit_email(request):
	username=request.COOKIES.get('username','')
	versions=models.Version.objects.all()
	return render(request,'ubablog2/send_email.html',{'versions':versions,'username':username})

def send_email(request):
	subject=request.POST.get('subject')
	content=request.POST.get('content')
	to=request.POST.get('to')
	send_mail(subject,content,'hongyihui@clickplus.cn',[to],fail_silently=False)
	return render(request,'ubablog2/send_email.html')

def version(request):
	versions=models.Version.objects.all()
	return render(request,'ubablog2/version.html',{'versions':versions})

def edit_version(request,version_id):
	if version_id=='0':
		return render(request,'ubablog2/edit_version.html')
	version=models.Version.objects.get(pk=version_id)
	return render(request,'ubablog2/edit_version.html',{'version':version})

def version_action(request):
	version_name=request.POST.get('version_name')
	version_id=request.POST.get('version_id')
	select1=request.POST.get('select1')
	select2=request.POST.get('select2')
	select3=request.POST.get('select3')
	select4=request.POST.get('select4')
	select5=request.POST.get('select5')
	select6=request.POST.get('select6')
	select7=request.POST.get('select7')
	select8=request.POST.get('select8')
	select9=request.POST.get('select9')
	select10=request.POST.get('select10')
	if version_id=='0':
		models.Version.objects.create(version_name=version_name,select1=select1,select2=select2,select3=select3,select4=select4,select5=select5,select6=select6,select7=select7,select8=select8,select9=select9,select10=select10)
		versions=models.Version.objects.all()
		print(versions)
		return render(request,'ubablog2/version.html',{'versions':versions})

	else:
		version=models.Version.objects.get(pk=version_id)
		version.version_name=version_name
		version.select1=select1
		version.select2=select2
		version.select3=select3
		version.select4=select4
		version.select5=select5
		version.select6=select6
		version.select7=select7
		version.select8=select8
		version.select9=select9
		version.select10=select10
		version.save()
		return render(request,'ubablog2/edit_version.html',{'version':version})


def tenant_list(pagenum):
	pass


def login_action(request):
	username=request.POST.get('username','')
	password=request.POST.get('password','')
	user = models.User.objects.filter(username = username)  
	if user:  
		passwd = models.User.objects.filter(username = username, password = password)  
		if passwd:  
			request.session['username']=username
			return HttpResponseRedirect('/blog2/index')
		else:  
			info = '请检查密码是否正确!' 
			messages.info(request,info, extra_tags='bg-warning text-warning')
			return HttpResponseRedirect('/blog2/login')
	elif len(user) == 0:  
		info = '请检查用户名是否正确!'  
		messages.info(request,info, extra_tags='bg-warning text-warning')
		return HttpResponseRedirect('/blog2/login') 

def regist(request):
	if request.method == 'POST':
		uf=UserForm(request.POST)
		if uf.is_valid():
			username=uf.cleaned_data['username']
			password=uf.cleaned_data['password']

			user=models.User.objects.filter(username=username)
			if user:
				info='用户名已存在！'
			elif len(user)==0:
				info='注册成功~！'
				user=models.User()
				user.username=username
				user.password=password
				user.save()
			return HttpResponseRedirect('/blog2/login/')
			#return render(request,'registration/login.html')
	else:
		uf=UserForm()
	return render(request,'registration/regist.html',{'uf':uf})

def requires_login(view):
	def new_view(request,*args,**kwargs):
		if not if_login(request):
			return HttpResponseRedirect('/blog2/login/')
		return view(request,*args,**kwargs)
	return new_view

def if_login(request):
	print("#########login##########")
	is_login=request.session.get('username')
	if not is_login:
		print("###############################not login")
		return False
	else:
		print('###############################loging')
		return True

def login(request):  
    #if request.method == 'GET':
    #    request.session['login_from']=request.META.get('HTTP_REFERER','/blog2/index')
    if request.method == 'POST':  
        ##获取表单信息  
        uf = UserForm(request.POST)  
        if uf.is_valid():  
            username = uf.cleaned_data['username']  
            password = uf.cleaned_data['password']  
  
            ##判断用户密码是否匹配  
            user = models.User.objects.filter(username = username)  
            if user:  
                passwd = models.User.objects.filter(username = username, password = password)  
                if passwd:  
                    info = '登录成功！'  
                    request.session['username']=username
                    #return HttpResponseRedirect(request.session['login_from'])
                    return HttpResponseRedirect('/blog2/index')
                    #return render(request,'ubablog2/index.html')
                else:  
                    info = '请检查密码是否正确!' 
                    messages.info(request,info, extra_tags='bg-warning text-warning')
            elif len(user) == 0:  
                info = '请检查用户名是否正确!'  
                messages.info(request,info, extra_tags='bg-warning text-warning')
            return render(request,'registration/login.html')

    else:  
        uf = UserForm()  
  
    return render(request,'registration/login.html', {'uf': uf})  
  
def loginout(request):
	try: 
		del request.session['username']
	except KeyError:
		pass
	#uf = UserForm() 
	#return render(request,"registration/login.html",{'uf': uf})
	return HttpResponseRedirect("/blog2/login")
def change_pass(request):  
    if request.method == 'POST':  
        uf = ChangeForm(request.POST)  
        if uf.is_valid():  
            username = uf.cleaned_data['username']  
            old_password = uf.cleaned_data['old_password']  
            new_password = uf.cleaned_data['new_password']  
  
            ##判断用户原密码是否匹配  
            user = models.User.objects.filter(username = username)  
            if user:  
                passwd = User.objects.filter(username = username , password = old_password )  
                if passwd:  
                    User.objects.filter(username = username,password = old_password).update(password = new_password)        ##如果用户名、原密码匹配则更新密码  
                    info = '密码修改成功!'  
                else:  
                    info = '请检查原密码是否输入正确!'  
            elif len(user) == 0:  
                info = '请检查用户名是否正确!'  
  
        return HttpResponse(info)  
    else:  
        uf = ChangeForm()  
    return render(request,'registration/change.html',{'uf':uf})  

def tenant_list(request,page):
	is_login=request.session.get('username')
	if is_login:
		if page=='0':
			print("############delete session")
			try:
				del request.session['tenants_list']
			except:
				pass
			page=1
			is_tenants=None
		else:
			is_tenants=request.session.get('tenants_list')
		if page=="9494":
			jump_page=request.GET.get('page')
			page=int(jump_page)
			print("######")
			print(jump_page)
		if not is_tenants:
			tenant_info=models.Tenant.objects.all()

			print("########get_tenants")
		else:
			tenant_info=is_tenants
		tenants_num=tenant_info.count()
		tenants=Paginator(tenant_info,3)	
		last_page=tenants.num_pages
		print("###################")
		print(last_page)
		print("###################")
		#if page=='0':
			#return render(request,'ubablog2/tenant_list.html',{'tenant_info':tenants.page(tenants.num_pages).object_list,'tenants':tenants.page(tenants.num_pages),'pagenum':tenants.num_pages,'username':is_login})
		#print("############"+str(tenant_info.count()))
		
		return render(request,'ubablog2/tenant_list.html',{'tenants_num':tenants_num,'last_page':last_page,'tenant_info':tenants.page(page).object_list,'tenants':tenants.page(page),'pagenum':page,'username':is_login})
	else:
		return HttpResponseRedirect("/blog2/login")

def tenant_search(request):
	is_login=request.session.get('username')
	if is_login:
		tenant_name=request.POST.get('tenant_name')
		sale=request.POST.get('sale')
		account_status=request.POST.get('account_status')
		page=1
		print('#######')
		print(type(tenant_name),tenant_name)
		print('#########')
		print(type(sale),sale)
		print('#######')
		print(type(account_status),account_status)
		if tenant_name != '' and sale != '' and account_status != '': 
			tenant_info=models.Tenant.objects.filter(Q(tenant_name=tenant_name)&Q(contact=sale)&Q(is_default=account_status))
			request.session['tenants_list']=tenant_info
		elif tenant_name != '' and sale != '' and account_status == '':
			tenant_info=models.Tenant.objects.filter(Q(tenant_name=tenant_name)&Q(contact=sale))
			request.session['tenants_list']=tenant_info
		elif tenant_name != '' and sale == '' and account_status != '':
			tenant_info=models.Tenant.objects.filter(Q(tenant_name=tenant_name)&Q(is_default=account_status))
			request.session['tenants_list']=tenant_info
		elif tenant_name == '' and sale != '' and account_status != '':
			tenant_info=models.Tenant.objects.filter(Q(is_default=account_status)&Q(contact=sale))
			request.session['tenants_list']=tenant_info
		elif tenant_name != '' and sale == '' and account_status == '':
			tenant_info=models.Tenant.objects.filter(Q(tenant_name=tenant_name))
			request.session['tenants_list']=tenant_info
		elif tenant_name == '' and sale != '' and account_status == '':
			tenant_info=models.Tenant.objects.filter(Q(contact=sale))
			request.session['tenants_list']=tenant_info
		elif tenant_name == '' and sale == '' and account_status != '':
			tenant_info=models.Tenant.objects.filter(Q(is_default=account_status))
			request.session['tenants_list']=tenant_info
		else:
			tenant_info=models.Tenant.objects.all()
			
			request.session['tenants_list']=tenant_info
		tenants_num=tenant_info.count()
		tenants=Paginator(tenant_info,3)
		last_page=tenants.num_pages
		print("###########")
		print(last_page)
		return render(request,'ubablog2/tenant_list.html',{'tenants_list':tenant_info,'tenants_num':tenants_num,'tenant_info':tenants.page(page).object_list,'tenants':tenants.page(page),'last_page':last_page,'pagenum':page,'username':is_login})
	else:
		return HttpResponseRedirect("/blog2/login")