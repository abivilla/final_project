from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, formData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(formData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters."
        if str.isalpha(formData['first_name']) == False:
            errors["first"] = "First name must contain only letters."
        if len(formData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters."
        if str.isalpha(formData['last_name']) == False:
            errors["last"] = "Last name must contain only letters."
        if len(formData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters." 
        if formData["confirm_pw"] != formData["password"]:
            errors["confirm"] = "Confirm password should match password." 
        if not EMAIL_REGEX.match(formData['email']):                
            errors['email'] = ("Invalid email address!")
        check_email = self.filter(email=formData['email'])
        if check_email:
            errors['email_already_used'] = "Email has already been used!"
        return errors 
    
    def profile_validator(self, formData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(formData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters."
        if str.isalpha(formData['first_name']) == False:
            errors["first"] = "First name must contain only letters."
        if len(formData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters."
        if str.isalpha(formData['last_name']) == False:
            errors["last"] = "Last name must contain only letters."
        if len(formData['phone']) != 13:
            errors["phone"] = "Phone not valid."
        
        return errors 

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(default="(555)555-5555", max_length=255)
    city = models.CharField(null=True, max_length=255)
    password = models.CharField(max_length=255)
    profile_pic = models.ImageField(default="profile.png", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Post(models.Model):
    picture = models.ImageField(null=True, blank=True)
    desc = models.TextField(null=True)
    poster = models.ForeignKey(User, related_name='user_posts', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_posts')
    #post_comments

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_comments')