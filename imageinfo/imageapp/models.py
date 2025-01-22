from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE) 

    class Meta:
        unique_together = ('user', 'image') 