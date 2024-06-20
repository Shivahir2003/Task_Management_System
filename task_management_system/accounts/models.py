from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
        User Profile model
        
        Create user's extra details
    """
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobile_number=models.CharField(max_length=10,unique=True)
    user_image=models.ImageField(upload_to='accounts/',null=True,default=None)

    def __str__(self) -> str:
        return self.user.username
