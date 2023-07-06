
from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
from .helpers import *
from django.utils.timezone import now



# Create your models here.
class BlogModel(models.Model):
    user = models.ForeignKey(User, blank=True, null= True, on_delete=models.CASCADE)
    title = models.CharField(max_length=2000)
    content = FroalaField()
    slug = models.SlugField(max_length=1000, null=True , blank= True)
    image = models.ImageField(upload_to='blog')
    created_at = models.DateTimeField(auto_now=True)
    upload_to = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    
    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(BlogModel, self).save(*args, **kwargs)
        
        
#Creating a comment section

class BlogComment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogModel, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null= True)
    time = models.DateTimeField(default=now)
    

    
    