from __future__ import unicode_literals
from django.db import models
import re  # import python regex module
import bcrypt


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
DATE_REGEX = re.compile(r'^((?:19|20)\d\d)[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$')
class UserManager(models.Manager):

        def registration(self, data):
            errors = []
            print data['date_birth']
            if len(data['name']) < 3:
                errors.append("first name is empty or needs more 2 chars")
            if len(data['email']) < 3:
                errors.append(" no email?")
            if not EMAIL_REGEX.match(data['email']):
                errors.append(" email is not valid")
            if not DATE_REGEX.match(data['date_birth']):
                errors.append(" date is not valid")
            if len(data['password']) < 8:
                errors.append("password is empty  or needs more 8 chars")
            if len(data['confirm_ps']) < 8:
                errors.append("confirm password is empty or needs more than 8 characters")

            if data['confirm_ps'] != data['password'] :
                errors.append("password and confirm password are not same")
            if len(errors) == 0:
                user = self.filter(email=data['email'])
                if user :
                    errors.append("user alraedy exist")

            response = {}

            if len(errors) > 0:
                response['status'] = False
                response['errors'] = errors
            else :
                hashed_password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
                user = self.create(name=data['name'],

                            email=data['email'],
                            password=hashed_password)
                response['status'] = True
                response['user'] = user

            return response

        def login(self, data):

            response = {}
            errors = []

            if len(data['email']) < 1:
                errors.append(" email is empty")
            if not EMAIL_REGEX.match(data['email']):
                errors.append(" email is not valid")
            if len(data['password']) < 8:
                errors.append("password is empty  or needs more 8 chars")

            if len(errors) == 0:
                user = self.filter(email=data['email'])
                if user :
                    if bcrypt.checkpw(data['password'].encode(), user[0].password.encode()):
                        response['status'] = True
                        response['user'] = user[0]
                    else :
                        errors.append("Invalid password try again")
                        response['status'] = False
                        response['errors'] = errors
                else :
                    errors.append("Invalid user try again")
                    response['status'] = False
                    response['errors'] = errors
            else :
                response['status'] = False
                response['errors'] = errors
            return response

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=34)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=256)
    created_at =  models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
