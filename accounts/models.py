from django.db import models
# we need to import the abstract user class 
from django.contrib.auth.models import AbstractUser 
# Create your models here.

class User(AbstractUser):
    
    pass
