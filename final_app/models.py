from django.db import models
import re
import bcrypt


# Create your models here.
class UserManager(models.Manager):
    def validatorRe(self,postData):
            passregex=re.compile(r'^[a-zA-Z0-9]+$')
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            errors={}
        
            #checking first name & last name:
            if len(postData['First_Name'])<2:
                errors['First_Name']=" first name should be more than 2 chars"
            if len(postData['Last_Name'])<2:
                errors['Last_Name']="last name must be more than 2 chars"

            #checking password:
            if len(postData['Password']) < 8:
                errors['Password'] = "Password should be at least 8 characters"
            if not passregex.match(postData['Password']):
                errors['pw_match'] = "Passwords must have mor than 1 char "
            if postData['Password'] != postData['Password2']:
                errors['pw_match'] = "Passwords don't match "

            
            #checking email: 
            if not EMAIL_REGEX.match(postData['Email']):    # test whether a field matches the pattern            
                errors['Email'] = "Invalid email address!"
            return errors

                
    def validatorLo(self,postData):
            errors = {}
            #fetching for the email in db.
            user = Users.objects.filter(Email=postData['Email'])

            #checking email (if user=none -> error , if user exist -> else)
            if not(user):
                errors ['Email'] = 'Email is not correct'
            elif not(bcrypt.checkpw(postData['Password'].encode(), user[0].Password.encode())):
                errors ['Password'] = 'Not correct password'
            
            return errors


class ArticleManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['title'])==0:
                errors['title']=" Article title is required"
        if len(postData['title'])<3:
                errors['title']=" item title must be at least 3 chars"
        return errors


class Users(models.Model):
    First_Name=models.CharField(max_length=255)
    Last_Name=models.CharField(max_length=255)
    Email=models.EmailField(max_length=255)
    Password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

class Articles(models.Model):
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=255)
    user = models.ForeignKey(Users, related_name='article', on_delete=models.CASCADE)
    tag=models.CharField(max_length=255,default="coding")
    liked =models.ManyToManyField(Users,related_name='liked', default=None,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    objects=ArticleManager()

    def __str__(self):
        return str(self.title)
    @property
    def num_likes(self):
        return self.liked.all().cont()




LIKE_CHOICES=(
('Like','Like'),
('Unlike','Unlike')
)
class Like(models.Model):
    user=models.ForeignKey(Users, on_delete=models.CASCADE)
    article=models.ForeignKey(Articles, on_delete=models.CASCADE)
    value=models.CharField(choices=LIKE_CHOICES,default="Like" ,max_length=10)
    
    def __str__(self):
        return str(self.article)


class Tags(models.Model):
    tag_name= models.CharField(max_length=55)
    articles = models.ManyToManyField(Articles, related_name="tags")

class Comment(models.Model):
    message_id =models.ForeignKey(Articles, related_name = "comments", blank=True, null=True, on_delete=models.CASCADE)
    user_id =models.ForeignKey(Users, related_name = "comments", blank=True, null=True, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)