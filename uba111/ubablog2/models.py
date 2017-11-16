from django.db import models

# Create your models here.

class Article(models.Model):
	title=models.CharField(max_length=32,default='uba Title')
	content=models.TextField(null=True)
	pubtime=models.DateTimeField(auto_now=True)
	#在admin后台应用中展示title，代替默认的article.object
	def __str__(self):
		return self.title

class Version(models.Model):
	version_name=models.CharField(max_length=32)
	select1=models.CharField(max_length=32)
	select2=models.CharField(max_length=32)
	select3=models.CharField(max_length=32)
	select4=models.CharField(max_length=32)
	select5=models.CharField(max_length=32)
	select6=models.CharField(max_length=32)
	select7=models.CharField(max_length=32)
	select8=models.CharField(max_length=32)
	select9=models.CharField(max_length=32)
	select10=models.CharField(max_length=32)

	def __str__(self):
		return self.version_name


class Tenant(models.Model):
	
	tenant_id=models.IntegerField(max_length=25)
	tenant_name=models.CharField(max_length=255)
	email=models.CharField(max_length=255)
	contact=models.CharField(max_length=255)
	contact_number=models.CharField(max_length=25)
	start_time=models.DateTimeField()
	end_time=models.DateTimeField()
	status=models.IntegerField()
	is_default=models.IntegerField()
	is_abutment=models.IntegerField()
	version_id=models.CharField(max_length=255)

	def __str__(self):
		return self.tenant_name

class User(models.Model):
	username=models.CharField(max_length=30)
	password=models.CharField(max_length=50)


	def __str__(self):
		return self.username