from django.db import models
import re, bcrypt
# from __future__ import unicode_literals
# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['fn']) < 2:
            errors['fn'] = "First name too short"
        
        if postData['pw'] != postData['confirmpw']:
            errors['pw'] = "Passwords do not match"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        if len(User.objects.filter(email= postData['email'])):
            errors['email-non-unique'] = ("Email is already used, try logging in!")
        if len(postData["pw"]) < 8:
            errors["password-length"] = "Password must be at least 8 characters long"
        if len(postData["pw"]) > 16:
            errors["password-length"] = "no longer than 15 characters"
        if postData["pw"] != postData['confirmpw']:
            errors["passwords-match"] = "Your passwords did not match"

        return errors

    def log_validator(self, postData):
        errors = {}
        matched_user = User.objects.filter(email = postData['email_log'])
        print('matched_user', matched_user)
        if len(matched_user) < 1:
            print('no user')
            errors['no-user'] = 'Email or Password was not found'

        elif bcrypt.checkpw(postData['pwlog'].encode(), matched_user[0].password.encode()):
            print('passwords match!')
        else:
            print('password incorrect')
            errors['password-non-match'] = 'incorrect password'

        return errors
# class WishManager(models.Manager):
#     def wish_validator(self, postData):
#         errors = {}

#         if len(postData['item']) < 5:
#             errors['title-length'] = "Thought should at least be 5 characters"
        
#         if len(postData['item']) > 50:
#             errors['title-max-length'] = "Please no more than 50 characters for the title"

#         if len(postData['desc']) < 5:
#             errors['desc-length'] = "Thought should at least be 5 characters"

#         if len(postData['desc']) > 150:
#             errors['title-max-length'] = "Please no more than 150 characters for the description"

#         return errors

class ThoughtManager(models.Manager):
    def thought_validator(self, postData):
        errors = {}

        if len(postData['desc']) <5:
            errors['thought-length'] = "Thought should be at least 5 characters"

        return errors




            

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

# class Wish(models.Model):
#     item = models.CharField(max_length=255)
#     desc = models.CharField(max_length=255)
#     location = models.CharField(max_length=255)
#     uploaded_by = models.ForeignKey(User, related_name="wishes_uploaded")
#     users_who_like = models.ManyToManyField(User, related_name="liked_wishes")
#     granted = models.BooleanField(default = False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     objects = WishManager()

class Thought(models.Model):
    desc = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, related_name="thoughts_uploaded")
    users_who_like = models.ManyToManyField(User, related_name='liked_thoughts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ThoughtManager()
