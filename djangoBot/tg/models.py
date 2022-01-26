from django.db import models

# Create your models here.
class CategoryModel(models.Model):
	name=models.CharField(max_length=250 )
	slug=models.CharField(max_length=250 )
	def save(self,*args,**kwargs):
		if not self.slug :
			self.slug=slugify(self.name)
		super(CategoryModel ,self ).save(*args,**kwargs)
	def __str__(self):
		return self.name
		
class ProductModel(models.Model):
	title=models.CharField(max_length=250 , null=False)
	text=models.TextField()
	ctg=models.ForeignKey(CategoryModel , on_delete=models.CASCADE)	
	rasm=models.ImageField(upload_to='image/' , blank=True)
	time=models.DateTimeField(auto_now_add=True)
	is_chanal=models.BooleanField(default=False)
	price=models.IntegerField()
	zapas=models.IntegerField()
	def __str__(self):
		return self.title

class KorzinkaModel(models.Model):
	haridor=models.CharField(max_length=250 )
	is_deliver=models.BooleanField(default=False)
	product=models.CharField(max_length=250 )
	soni=models.IntegerField(default=1)
	total=models.IntegerField(default=0)
	address=models.CharField(max_length=250 , null=True ,blank=True)
	telefon=models.CharField(max_length=250 , null=True,blank=True)
	user_p=models.CharField(max_length=250 , null=True ,blank=True)
	def __str__(self):
		return self.haridor






