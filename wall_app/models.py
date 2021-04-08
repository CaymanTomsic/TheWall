from django.db import models
import bcrypt, re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['username_form']) < 2:
            errors["username"] = "Username should be at least 2 characters"
        if len(postData['password_form']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password_form'] != postData['confirm_password']:
            errors['confirm_password'] = "Passwords do not match"
        # Checks if a valid email format
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email_form']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        # checks if email is unique:
        for user in User.objects.all():
            if user.email == postData['email_form']:
                errors['email'] = "Invalid email address!"
        return errors
    def validate_login(self, postData):
        errors = {}
        user_list = User.objects.filter(email=postData['log_email'])
        if len(user_list) > 0 and bcrypt.checkpw(postData['log_pw'].encode(), user_list[0].password.encode()):
            print("password match")
        else:
            errors['login'] = "invalid email or password"
            print("failed login")
        return errors
    def validate_message(self, postData):
        errors = {}
        if len(postData['message_text_form']) < 1:
            errors["message_text"] = "Message should be at least 1 character long"
        return errors
    def validate_comment(self, postData):
        errors = {}
        if len(postData['comment_text_form']) < 1:
            errors["comment_text"] = "Comment should be at least 1 character long"
        return errors

class User(models.Model):
    username = models.CharField(max_length=25)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=200)
    birthday = models.DateField()
    # messages
    # comments
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class PostedMessage(models.Model):
    user = models.ForeignKey(User, related_name="messages", on_delete = models.CASCADE)
    message_text = models.CharField(max_length=255)
    # comments
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comments", on_delete = models.CASCADE)
    posted_message = models.ForeignKey(PostedMessage, related_name="comments", on_delete = models.CASCADE)
    comment_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)