from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.





def index(request):
	#return HttpResponse('this is uba first page' )
	return render(request,'uba_blog/index.html',{'hello':'second Page'})