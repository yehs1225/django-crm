from distutils.command.upload import upload
from unicodedata import category
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import AbstractUser
# create database table
class User(AbstractUser):
    is_organizor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField("User",on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    organization = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent",related_name='leads',null=True,blank=True,on_delete = models.SET_NULL)
    category = models.ForeignKey("Category",related_name='leads',null=True,blank=True,on_delete = models.SET_NULL)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    profile_picture = models.ImageField(null=True,blank=True,upload_to='profile_pictures')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

#return the assigned file name
def handle_upload_follow_ups(instance,filename):#instance = model FollowUp
    return f"lead_followups/lead_{instance.lead.pk}/{filename}"

class FollowUp(models.Model):
    lead = models.ForeignKey(Lead,related_name="followups",on_delete=models.CASCADE)
    data_added = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True,null=True)
    file = models.FileField(null=True,blank=True,upload_to=handle_upload_follow_ups)

    def __str__(self):
        return f"{self.lead.first_name} {self.lead.last_name}"

class Agent(models.Model):
    user = models.OneToOneField("User",on_delete=models.CASCADE)
    organization = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.email

#category of leads : New(initial), contacted, Converted, Unconverted
class Category(models.Model):
    name = models.CharField(max_length=30)
    organization = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

# a signal once the post_save is set
def post_user_created_signal(sender,instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal,sender=User)