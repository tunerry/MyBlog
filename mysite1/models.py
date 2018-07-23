from django.db import models
from PyCharm.settings import MEDIA_URL

# Create your models here.

class User(models.Model):
    userid = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 32)
    pwd = models.CharField( max_length = 32)
    gender = models.CharField(max_length = 8)
    email = models.CharField(max_length= 32,default='')
    admin = models.BooleanField(default=False)

def ariticleImg(instance, filename):
    return instance.title+'/'+filename

class Article(models.Model):
    title = models.CharField(max_length = 100)
    time = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('User',related_name='user_article',on_delete=models.CASCADE,)
    cover = models.ImageField(upload_to = ariticleImg,default=None)
    test = models.TextField(max_length=1500)

