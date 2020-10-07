from django.db import models
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save#user object  signal create hunxa

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
   
  
    
    
    class Meta:
        verbose_name_plural ='Profile'
        
        
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        
        
    def __str__(self):
        return self.user.username    #i use this function because i dont use null =True in user -everytime i need this
    

  
    @receiver(post_save, sender = User)
    def update_profile(sender,instance,created,*args,**kwargs):#update_profile is receiver function and User is sender
        
        if created:
            
            Profile.objects.create(user=instance)
            instance.profile.save()   #builtin profile lowercasw
